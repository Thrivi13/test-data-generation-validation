import os

import pandas as pd
import streamlit as st

from src.ai_explainer import explain_validation_result
from src.generator import generate_test_cases
from src.rule_normalizer import normalize_rule
from src.rule_parser import parse_rule_table
from src.summary import summarize_results
from src.validator import validate_test_cases


st.set_page_config(
    page_title="Test Data Generation & Validation",
    layout="wide",
)

st.title("Test Data Generation and Validation")

st.write(
    "Upload a field-rule table to generate valid, boundary, "
    "and invalid test data and validate the generated cases."
)

uploaded_file = st.file_uploader(
    "Upload CSV rule table",
    type=["csv"],
)

if uploaded_file is not None:

    # ---------------------------------------------------------
    # 1. Read and preview input
    # ---------------------------------------------------------
    st.subheader("Input Rule Table")

    try:
        uploaded_file.seek(0)
        input_df = pd.read_csv(uploaded_file)

        st.dataframe(input_df, use_container_width=True)

    except Exception as exc:
        st.error(f"Unable to read the CSV file: {exc}")
        st.stop()

    # ---------------------------------------------------------
    # 2. Parse and normalize rules
    # ---------------------------------------------------------
    try:
        uploaded_file.seek(0)

        raw_rules = parse_rule_table(uploaded_file)

        normalized_rules = [
            normalize_rule(rule)
            for rule in raw_rules
        ]

    except ValueError as exc:
        st.error(f"Invalid rule table: {exc}")
        st.stop()

    st.success(
        f"Successfully loaded {len(normalized_rules)} field rule(s)."
    )

    # ---------------------------------------------------------
    # 3. Generate and validate
    # ---------------------------------------------------------
    if st.button("Generate and Validate Test Data"):

        test_cases = generate_test_cases(normalized_rules)

        validation_results = validate_test_cases(
            test_cases,
            normalized_rules,
        )

        summary = summarize_results(validation_results)

        # Store results so they remain available after reruns.
        st.session_state["validation_results"] = validation_results
        st.session_state["summary"] = summary

    # ---------------------------------------------------------
    # 4. Display results
    # ---------------------------------------------------------
    if "validation_results" in st.session_state:

        validation_results = st.session_state["validation_results"]
        summary = st.session_state["summary"]

        st.subheader("Validation Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Cases", summary["total_cases"])
        col2.metric("Valid Cases", summary["valid_cases"])
        col3.metric("Invalid Cases", summary["invalid_cases"])
        col4.metric("Boundary Cases", summary["boundary_cases"])

        st.subheader("Generated Test Data")

        table_rows = []

        for index, result in enumerate(validation_results, start=1):
            row = {
                "case_id": index,
                "case_type": result["case_type"],
                "valid": result["valid"],
            }

            row.update(result["data"])
            table_rows.append(row)

        results_df = pd.DataFrame(table_rows)

        st.dataframe(
            results_df,
            use_container_width=True,
        )

        # -----------------------------------------------------
        # 5. Detailed validation results
        # -----------------------------------------------------
        st.subheader("Validation Details")

        for index, result in enumerate(
            validation_results,
            start=1,
        ):

            status = "VALID" if result["valid"] else "INVALID"

            with st.expander(
                f"Case {index} — {result['case_type'].upper()} — {status}"
            ):

                for field_name, field_result in result[
                    "field_results"
                ].items():

                    field_status = (
                        "✓ Valid"
                        if field_result["valid"]
                        else "✗ Invalid"
                    )

                    st.write(
                        f"**{field_name}** — "
                        f"{field_status} — "
                        f"{field_result['message']}"
                    )

        # -----------------------------------------------------
        # 6. AI explanations
        # -----------------------------------------------------
        st.subheader("AI Explanations")

        api_configured = bool(os.getenv("OPENAI_API_KEY"))

        if not api_configured:
            st.info(
                "AI explanations are unavailable because "
                "OPENAI_API_KEY is not configured."
            )
        else:
            if st.button("Generate AI Explanations"):

                for index, result in enumerate(
                    validation_results,
                    start=1,
                ):

                    explanation = explain_validation_result(result)

                    with st.expander(
                        f"Case {index} — {result['case_type'].upper()}"
                    ):
                        st.write(explanation)
