import pandas as pd

from src.models import FieldRule


REQUIRED_COLUMNS = {
    "field_name",
    "type",
    "required",
}

OPTIONAL_COLUMNS = {
    "min",
    "max",
    "allowed_values",
    "format_rule",
    "description",
}


def parse_rule_table(file) -> list[FieldRule]:
    """
    Read a CSV rule table and convert each row into a FieldRule object.
    """

    df = pd.read_csv(file)

    if df.empty:
        raise ValueError("The rule table is empty.")

    # Remove accidental CSV index columns
    df = df.loc[:, ~df.columns.str.startswith("Unnamed:")]

    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")

    # Check for empty field names
    field_names = df["field_name"].astype(str).str.strip()

    if field_names.eq("").any():
        raise ValueError("Field name cannot be empty.")

    # Check for duplicate field names
    duplicates = field_names[field_names.duplicated()].unique()

    if len(duplicates) > 0:
        duplicate_names = ", ".join(duplicates)
        raise ValueError(
            f"Duplicate field name(s) found: {duplicate_names}"
        )

    # Add optional columns if they are not present.
    for column in OPTIONAL_COLUMNS:
        if column not in df.columns:
            df[column] = None

    rules = []

    for _, row in df.iterrows():

        rule = FieldRule(
            field_name=str(row["field_name"]).strip(),
            data_type=str(row["type"]).strip().lower(),
            required=row["required"],
            minimum=row["min"],
            maximum=row["max"],
            allowed_values=row["allowed_values"],
            format_rule=row["format_rule"],
            description=row["description"],
        )

        rules.append(rule)

    return rules
