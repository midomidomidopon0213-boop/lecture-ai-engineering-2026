# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
　第一回では、一般的なことを答えていたが、今回は講座に合った内容を答えていた。data/glossary.json の定義と合っており、最後に関連する回「第一回」と示されていた。

- `--trace` で見えたツール呼び出し（ツール名と引数）：
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition":"ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…

- 1つの質問での LLM 呼び出し回数（`requests`）：2

- 追加したツールと、docstring に書いた説明：
「確認問題を出して」と頼まれたときに、エージェントが用語集から問題を作れるようにするmake_quiz ツールを実装し、追加した。
docstringに書いた説明は以下の通り

"""指定した回の用語から1つを選び、確認問題と答えを返す。

    「第2回の確認問題を出して」のように、講義内容の復習用の問題を
    求められたときに使う。
    """

## 宿題

- 取り組んだレベル：基礎 
- やったこと：
agent.pyypの中の
「- 用語や講座に固有のことを答える前に、必ず search_glossary で用語集を確認する。」
を削除して保存し、 uv run python -m app.agent --trace "LoRA とQLoRAの違いは？ "という質問を実行した。
- 結果：
**LoRA**と**QLoRA**の主な違いは、ベースモデルの重みをそのまま使うか、量子化してメモリを大幅に節約するかという点にあります。

* **LoRA（Low-Rank Adaptation）**
  * 事前学習済みの重みは固定し、重みの更新分を小さな低ランク行列（学習パラメータ）のみで近似・学習するPEFT（Parameter-Efficient Fine-Tuning）手法です。
  * 学習するパラメータ数が少なくて済み、効率的にファインチューニングを行えます。

* **QLoRA（Quantized LoRA）**
  * LoRAの仕組みをベースにしつつ、ベースモデルの重みを4ビットなどに**量子化**（精度を落としてデータ量を圧縮）してメモリを極限まで節約した手法です。
  * これにより、大きなモデルであっても、より小さなGPUメモリ上で学習できるようになります。

（関連する回：第2回）

--- trace ---
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition":"ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
[usage] RunUsage(cost=Decimal('0.0010005'), details={'text_prompt_tokens': 1310}, input_text_tokens=1310, input_tokens=1310, output_tokens=243, requests=2, tool_calls=2)

一応、用語集はsearch_glossaryで参照していることがわかるが、実際の解答にはそのまま使われることはなかった。

- 気づき・疑問：
「用語集に見つからないことは、推測で断定せず「用語集にはない」と伝える。
- 回答の最後に、関係する回（第N回）を示す。」
というところがまだ生きているため、用語集を参照し、関連する回を書くことはあったが、実際の解答には用語集からそのままとってくることはなかった。
この「- 用語や講座に固有のことを答える前に、必ず search_glossary で用語集を確認する。」という文章がいかに大事かを実感した。