import os

from google import genai


def explain_validation_results(results: list[dict]) -> list[str]:
    """
    Generate one short AI explanation for each validation result.

    Python determines validity.
    Gemini only explains the already-determined results.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return [
            "AI explanation unavailable: GEMINI_API_KEY is not configured."
            for _ in results
        ]

    client = genai.Client(api_key=api_key)

    cases = []

    for index, result in enumerate(results, start=1):
        cases.append(
            {
                "case_id": index,
                "case_type": result.get("case_type"),
                "valid": result.get("valid"),
                "field_results": result.get("field_results"),
            }
        )

    prompt = f"""
You are explaining test-data validation results.

Python has ALREADY determined whether each test case is valid or invalid.
Your job is ONLY to provide a short explanation for each case.

Do not change, reinterpret, or recalculate the Python validation result.

For every case, return exactly one short explanation.
The explanations must be returned in the same order as the cases.

Rules:
- For a valid case, briefly explain why the data satisfies the rules.
- For an invalid case, identify the field and rule that was violated.
- For a boundary case, mention the relevant boundary value or just-outside value.
- Keep each explanation to 1-2 sentences.
- Do not add numbering.
- Do not add headings.
- Return one explanation per line.

Validation results:
{cases}
"""

    try:
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt,
        )

        explanations = [
            line.strip()
            for line in interaction.output_text.splitlines()
            if line.strip()
        ]

        # Ensure exactly one explanation is available for every case.
        if len(explanations) < len(results):
            explanations.extend(
                [
                    "AI explanation was not generated for this case."
                    for _ in range(len(results) - len(explanations))
                ]
            )

        return explanations[:len(results)]

    except Exception as exc:
        return [
            f"AI explanation unavailable: {exc}"
            for _ in results
        ]