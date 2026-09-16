from src.ai_explainer import explain_validation_results


def test_ai_explanation_without_api_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    results = [
        {
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
    ]

    explanations = explain_validation_results(results)

    assert len(explanations) == 1
    assert "AI explanation unavailable" in explanations[0]
    assert "GEMINI_API_KEY" in explanations[0]