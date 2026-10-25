from google.genai import types

import app.ask as ask_module


class FakeModels:
    def __init__(self):
        self.requests = []
        self.answers = iter(["first answer", "second answer"])

    def generate_content(self, *, model, contents):
        self.requests.append((model, contents))
        return type("Response", (), {"text": next(self.answers), "usage_metadata": None})()


class FakeClient:
    def __init__(self):
        self.models = FakeModels()


def test_main_sends_prior_user_and_model_messages(monkeypatch):
    client = FakeClient()

    def fake_client(*, api_key):
        assert api_key == "test-key"
        return client

    def fake_input(prompt):
        assert "次の質問" in prompt
        return next(questions)

    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(ask_module.genai, "Client", fake_client)
    monkeypatch.setattr("sys.argv", ["app.ask", "first question"])
    questions = iter(["second question", ""])
    monkeypatch.setattr("builtins.input", fake_input)

    ask_module.main()

    first_request = client.models.requests[0][1]
    second_request = client.models.requests[1][1]
    assert [message.role for message in first_request] == ["user"]
    assert [message.role for message in second_request] == [
        "user",
        "model",
        "user",
    ]
    assert [message.parts[0].text for message in second_request] == [
        "first question",
        "first answer",
        "second question",
    ]
    assert isinstance(second_request[0], types.Content)
