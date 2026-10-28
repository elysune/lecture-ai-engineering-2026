from types import SimpleNamespace

from app.ask import ask


def test_ask_prints_token_usage(monkeypatch, capsys):
    fake_response = SimpleNamespace(
        text="回答です",
        usage_metadata=SimpleNamespace(
            prompt_token_count=123,
            candidates_token_count=45,
        ),
    )

    class FakeModels:
        def generate_content(self, model, contents):
            assert model is not None
            assert contents == "質問"
            return fake_response

    class FakeClient:
        def __init__(self, api_key):
            assert api_key == "dummy-key"
            self.models = FakeModels()

    monkeypatch.setattr("app.ask.genai.Client", FakeClient)
    monkeypatch.setattr("app.ask.get_api_key", lambda: "dummy-key")

    result = ask("質問")

    assert result == "回答です"
    captured = capsys.readouterr()
    assert "[入力トークン数] 123" in captured.out
    assert "[出力トークン数] 45" in captured.out
