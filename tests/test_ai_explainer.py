from src.ai_explainer import explain_validation_result


def test_ai_explanation_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    result = {
        "case_type": "invalid",
        "valid": False,
        "field_results": {
            "age": {
                "value": 17,
                "valid": False,
                "message": "Value is below the minimum.",
            }
        },
    }

    explanation = explain_validation_result(result)

    assert "AI explanation unavailable" in explanation
    assert "OPENAI_API_KEY" in explanation
