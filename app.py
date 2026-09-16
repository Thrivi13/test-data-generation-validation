import os

import pandas as pd
import streamlit as st

from src.ai_explainer import explain_validation_results
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

        # Remove accidental index columns.
        input_df = input_df.loc[
            :,
            ~input_df.columns.str.startswith("Unnamed:"),
        ]

        st.dataframe(
            input_df,
            use_container_width=True,
        )

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

        test_cases = generate_test_cases(
            normalized_rules
        )

        validation_results = validate_test_cases(
            test_cases,
            normalized_rules,
        )

        summary = summarize_results(
            validation_results
        )

        # Store results so they remain available after reruns.
        st.session_state["validation_results"] = (
            validation_results
        )

        st.session_state["summary"] = summary

        # Remove previous AI explanations when new results
        # are generated.
        st.session_state.pop(
            "ai_explanations",
            None,
        )

    # ---------------------------------------------------------
    # 4. Display results
    # ---------------------------------------------------------
    if "validation_results" in st.session_state:

        validation_results = (
            st.session_state["validation_results"]
        )

        summary = st.session_state["summary"]

        # -----------------------------------------------------
        # Validation Summary
        # -----------------------------------------------------
        st.subheader("Validation Summary")

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        col1.metric(
            "Total Cases",
            summary["total_cases"],
        )

        col2.metric(
            "Valid Cases",
            summary["valid_cases"],
        )

        col3.metric(
            "Invalid Cases",
            summary["invalid_cases"],
        )

        col4.metric(
            "Boundary Cases",
            summary["boundary_cases"],
        )

        col5.metric(
            "Expectation Matches",
            summary["expectation_matches"],
        )

        col6.metric(
            "Expectation Mismatches",
            summary["expectation_mismatches"],
        )

        # -----------------------------------------------------
        # Generated Test Data
        # -----------------------------------------------------
        st.subheader("Generated Test Data")

        table_rows = []

        for index, result in enumerate(
            validation_results,
            start=1,
        ):
            row = {
                "case_id": index,
                "case_type": result["case_type"],
                "field_name": result.get("field_name"),
                "test_reason": result.get("test_reason"),
                "expected": (
                    "VALID"
                    if result["expected_valid"] is True
                    else "INVALID"
                    if result["expected_valid"] is False
                    else "N/A"
                ),
                "actual": (
                    "VALID"
                    if result["actual_valid"]
                    else "INVALID"
                ),
                "match": (
                    "YES"
                    if result["matches_expectation"] is True
                    else "NO"
                    if result["matches_expectation"] is False
                    else "N/A"
                ),
            }

            row.update(result["data"])
            table_rows.append(row)

        results_df = pd.DataFrame(table_rows)

        # Remove any accidental index columns.
        results_df = results_df.loc[
            :,
            ~results_df.columns.str.startswith("Unnamed:"),
        ]

        st.dataframe(
            results_df,
            use_container_width=True,
        )

        # -----------------------------------------------------
        # Download Results
        # -----------------------------------------------------
        csv_data = results_df.to_csv(
            index=False
        )

        st.download_button(
            label="Download Test Results as CSV",
            data=csv_data,
            file_name="test_data_results.csv",
            mime="text/csv",
        )

        # -----------------------------------------------------
        # 5. Detailed Validation Results
        # -----------------------------------------------------
        st.subheader("Validation Details")

        for index, result in enumerate(
            validation_results,
            start=1,
        ):

            status = (
                "VALID"
                if result["actual_valid"]
                else "INVALID"
            )

            with st.expander(
                f"Case {index} — "
                f"{result['case_type'].upper()} — "
                f"{status}"
            ):

                st.write(
                    f"**Expected:** "
                    f"{'VALID' if result['expected_valid'] is True else 'INVALID' if result['expected_valid'] is False else 'N/A'}"
                )

                st.write(
                    f"**Actual:** "
                    f"{'VALID' if result['actual_valid'] else 'INVALID'}"
                )

                st.write(
                    f"**Expectation Match:** "
                    f"{'YES' if result['matches_expectation'] is True else 'NO' if result['matches_expectation'] is False else 'N/A'}"
                )

                for (
                    field_name,
                    field_result,
                ) in result["field_results"].items():

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
        # 6. AI Case Summaries
        # -----------------------------------------------------
        st.subheader("AI Case Summaries")

        api_configured = bool(
            os.getenv("GEMINI_API_KEY")
        )

        if not api_configured:

            st.info(
                "AI explanations are unavailable because "
                "GEMINI_API_KEY is not configured."
            )

        else:

            if st.button("Generate AI Summaries"):

                with st.spinner(
                    "Generating AI summaries..."
                ):

                    explanations = (
                        explain_validation_results(
                            validation_results
                        )
                    )

                st.session_state["ai_explanations"] = (
                    explanations
                )

            # -------------------------------------------------
            # Display AI summaries inside the result table
            # -------------------------------------------------
            if "ai_explanations" in st.session_state:

                explanations = (
                    st.session_state["ai_explanations"]
                )

                results_with_summary = results_df.copy()

                results_with_summary["Summary"] = (
                    explanations
                )

                st.subheader(
                    "Test Results with AI Summary"
                )

                st.dataframe(
                    results_with_summary,
                    use_container_width=True,
                )

                # -------------------------------------------------
                # Download results including AI summaries
                # -------------------------------------------------
                summary_csv = (
                    results_with_summary.to_csv(
                        index=False
                    )
                )

                st.download_button(
                    label="Download Results with AI Summary",
                    data=summary_csv,
                    file_name=(
                        "test_data_results_with_summary.csv"
                    ),
                    mime="text/csv",
                )