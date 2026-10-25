"""第1回: 素のLLMに質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 既定の質問のあと、続けて質問できる

続けて入力した質問と回答は会話履歴として次のリクエストに含める。
空行を入力すると終了する。ツールは使わない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai import errors
from google.genai import types

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(question: str, history: list[types.Content], client: genai.Client) -> str:
    user_message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=question)],
    )
    response = client.models.generate_content(
        model=MODEL,
        contents=[*history, user_message],
    )

    answer = response.text
    if answer is None:
        raise RuntimeError("モデルからテキスト応答がありません。")

    history.extend(
        [
            user_message,
            types.Content(
                role="model",
                parts=[types.Part.from_text(text=answer)],
            ),
        ]
    )

    usage = response.usage_metadata
    if usage is not None:
        print(f"[トークン] 入力: {usage.prompt_token_count} / 出力: {usage.candidates_token_count}")

    return answer


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    history: list[types.Content] = []
    question = args.question

    try:
        client = genai.Client(api_key=get_api_key())
        while question:
            print(f"[質問] {question}\n")
            print(ask(question, history, client))
            try:
                question = input("\n次の質問 (終了するには空行): ")
            except EOFError:
                break
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
