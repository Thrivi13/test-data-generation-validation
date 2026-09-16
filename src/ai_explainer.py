import os

from openai import OpenAI


def explain_validation_result(result: dict) -> str:
    """
    Generate a short explanation of an already-determined
    validation result.

    The validation decision is made entirely by Python.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return "AI explanation unavailable: OPENAI_API_KEY is not configured."

    client = OpenAI(api_key=api_key)

    prompt = f"""
Explain the following test-data validation result briefly and clearly.

Case type: {result.get("case_type")}
Python validation result: {"VALID" if result.get("valid") else "INVALID"}

Field validation details:
{result.get("field_results")}

Important:
- Do not change or reinterpret the Python validation result.
- Do not perform validation yourself.
- Explain why the provided result occurred.
- Mention relevant boundary or rule violations when applicable.
- Keep the explanation to 2-4 sentences.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
    )

    return response.output_text.strip()
