import random
import string
from datetime import date, timedelta
from typing import Any

from src.models import FieldRule


# ============================================================
# Realistic synthetic data pools
# ============================================================

FIRST_NAMES = [
    "Aarav", "Aditya", "Aisha", "Akash", "Akhil", "Aman",
    "Amrita", "Ananya", "Arjun", "Arnav", "Bhavana", "Charan",
    "Chetan", "Deepak", "Deepika", "Divya", "Gaurav", "Harish",
    "Ishita", "Karthik", "Kavya", "Kiran", "Lakshmi", "Manish",
    "Meera", "Mohit", "Nandini", "Neha", "Nikhil", "Pooja",
    "Pranav", "Priya", "Rahul", "Rakesh", "Ravi", "Riya",
    "Rohan", "Sanjay", "Shreya", "Sneha", "Srinivas", "Swathi",
    "Tanvi", "Varun", "Vikas", "Vikram"
]

LAST_NAMES = [
    "Sharma", "Patel", "Reddy", "Kumar", "Rao", "Nair",
    "Verma", "Iyer", "Joshi", "Gupta", "Mehta", "Singh",
    "Das", "Kapoor", "Menon", "Chowdhury", "Mishra", "Bhat",
    "Naidu", "Pillai", "Desai", "Kulkarni", "Malhotra",
    "Saxena", "Agarwal", "Krishnan", "Shetty", "Chandra",
    "Pandey", "Sinha"
]

CITIES = [
    "Bengaluru", "Hyderabad", "Chennai", "Mumbai", "Pune",
    "Delhi", "Kolkata", "Kochi", "Mysuru", "Vijayawada",
    "Visakhapatnam", "Coimbatore", "Ahmedabad", "Jaipur",
    "Indore", "Bhubaneswar", "Mangaluru", "Noida",
    "Gurugram", "Nagpur"
]

PRODUCTS = [
    "Wireless Mouse",
    "Mechanical Keyboard",
    "USB-C Hub",
    "Laptop Stand",
    "Bluetooth Speaker",
    "Webcam",
    "Power Bank",
    "Desk Lamp",
    "External SSD",
    "Wireless Headphones",
    "Smart Watch",
    "Portable Charger",
    "Gaming Keyboard",
    "Monitor Stand",
    "HDMI Adapter",
    "Fitness Band",
    "Tablet Stand",
    "Bluetooth Earbuds",
    "Laptop Backpack",
    "USB Flash Drive"
]

COMPANIES = [
    "TechNova",
    "DataWorks",
    "CloudBridge",
    "NextGen Systems",
    "Vertex Labs",
    "BlueOrbit",
    "SmartCore",
    "InnoTech",
    "BrightPath",
    "CodeCraft",
    "DigitalEdge",
    "Nexora Technologies",
    "QuantumWorks",
    "SkyLine Systems",
    "PrimeLogic"
]

DOMAINS = [
    "example.com",
    "example.test",
    "demo.example"
]


# ============================================================
# Random realistic values
# ============================================================

def _random_name() -> str:
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def _random_username() -> str:
    first = random.choice(FIRST_NAMES).lower()
    number = random.randint(100, 9999)
    return f"{first}{number}"


def _random_email() -> str:
    first = random.choice(FIRST_NAMES).lower()
    last = random.choice(LAST_NAMES).lower()
    number = random.randint(100, 9999)
    domain = random.choice(DOMAINS)

    return f"{first}.{last}{number}@{domain}"


def _random_phone() -> str:
    first_digit = random.choice("6789")
    remaining = "".join(
        random.choices(string.digits, k=9)
    )

    return first_digit + remaining


def _random_url() -> str:
    subdomain = random.choice(
        ["www", "app", "shop", "portal", "demo", "test"]
    )

    domain = random.choice(DOMAINS)

    return f"https://{subdomain}.{domain}"


def _random_date() -> str:
    start_date = date(2020, 1, 1)
    end_date = date(2026, 12, 31)

    random_days = random.randint(
        0,
        (end_date - start_date).days
    )

    generated_date = start_date + timedelta(
        days=random_days
    )

    return generated_date.strftime("%Y-%m-%d")


def _random_integer(
    minimum=None,
    maximum=None
) -> int:

    if minimum is None:
        minimum = 1

    if maximum is None:
        maximum = minimum + 100

    return random.randint(
        int(minimum),
        int(maximum)
    )


def _random_float(
    minimum=None,
    maximum=None
) -> float:

    if minimum is None:
        minimum = 0.0

    if maximum is None:
        maximum = minimum + 100.0

    return round(
        random.uniform(
            float(minimum),
            float(maximum)
        ),
        2
    )


# ============================================================
# String helper
# ============================================================

def _fit_string_to_rule(
    value: str,
    rule: FieldRule
) -> str:

    if rule.minimum is not None:
        if len(value) < rule.minimum:
            value += "x" * (
                int(rule.minimum) - len(value)
            )

    if rule.maximum is not None:
        if len(value) > rule.maximum:
            value = value[:int(rule.maximum)]

    return value


# ============================================================
# Generate valid value
# ============================================================

def _generate_valid_value(rule: FieldRule) -> Any:

    # --------------------------------------------------------
    # Allowed values
    # --------------------------------------------------------

    if rule.allowed_values:
        return random.choice(rule.allowed_values)

    # --------------------------------------------------------
    # String
    # --------------------------------------------------------

    if rule.data_type == "string":

        if rule.format_rule:

            if rule.format_rule == "email":
                return _random_email()

            if rule.format_rule == "phone":
                return _random_phone()

            if rule.format_rule == "url":
                return _random_url()

            if rule.format_rule.startswith("date:"):
                return _random_date()

            if rule.format_rule.startswith("regex:"):
                return _fit_string_to_rule(
                    "Valid1@",
                    rule
                )

        field_name = rule.field_name.lower()

        if "username" in field_name:
            value = _random_username()

        elif field_name in {
            "name",
            "full_name",
            "fullname"
        }:
            value = _random_name()

        elif "first_name" in field_name:
            value = random.choice(FIRST_NAMES)

        elif "last_name" in field_name:
            value = random.choice(LAST_NAMES)

        elif "city" in field_name:
            value = random.choice(CITIES)

        elif "product" in field_name:
            value = random.choice(PRODUCTS)

        elif "company" in field_name:
            value = random.choice(COMPANIES)

        elif "phone" in field_name:
            value = _random_phone()

        elif "email" in field_name:
            value = _random_email()

        elif "website" in field_name or "url" in field_name:
            value = _random_url()

        elif "date" in field_name:
            value = _random_date()

        else:
            value = random.choice([
                "SampleData",
                "TestValue",
                "DemoUser",
                "ExampleText",
                "SampleRecord",
                "TestInput",
                "DemoValue",
                "ValidData"
            ])

        return _fit_string_to_rule(value, rule)

    # --------------------------------------------------------
    # Integer
    # --------------------------------------------------------

    if rule.data_type == "integer":

        return _random_integer(
            rule.minimum,
            rule.maximum
        )

    # --------------------------------------------------------
    # Float
    # --------------------------------------------------------

    if rule.data_type == "float":

        return _random_float(
            rule.minimum,
            rule.maximum
        )

    # --------------------------------------------------------
    # Boolean
    # --------------------------------------------------------

    if rule.data_type == "boolean":

        return random.choice([
            True,
            False
        ])

    return None


# ============================================================
# Boundary values
# ============================================================

def _generate_boundary_value(
    rule: FieldRule,
    boundary_type: str
) -> Any:

    minimum = rule.minimum
    maximum = rule.maximum

    # --------------------------------------------------------
    # String length boundaries
    # --------------------------------------------------------

    if rule.data_type == "string":

        if minimum is not None:

            if boundary_type == "min":
                return "a" * int(minimum)

            if boundary_type == "below_min":
                return "a" * max(
                    0,
                    int(minimum) - 1
                )

        if maximum is not None:

            if boundary_type == "max":
                return "a" * int(maximum)

            if boundary_type == "above_max":
                return "a" * (
                    int(maximum) + 1
                )

    # --------------------------------------------------------
    # Integer boundaries
    # --------------------------------------------------------

    if rule.data_type == "integer":

        if boundary_type == "min":
            if minimum is not None:
                return int(minimum)

        if boundary_type == "below_min":
            if minimum is not None:
                return int(minimum) - 1

        if boundary_type == "max":
            if maximum is not None:
                return int(maximum)

        if boundary_type == "above_max":
            if maximum is not None:
                return int(maximum) + 1

    # --------------------------------------------------------
    # Float boundaries
    # --------------------------------------------------------

    if rule.data_type == "float":

        if boundary_type == "min":
            if minimum is not None:
                return float(minimum)

        if boundary_type == "below_min":
            if minimum is not None:
                return float(minimum) - 0.01

        if boundary_type == "max":
            if maximum is not None:
                return float(maximum)

        if boundary_type == "above_max":
            if maximum is not None:
                return float(maximum) + 0.01

    return None


# ============================================================
# Invalid value
# ============================================================

def _generate_invalid_value(
    rule: FieldRule
) -> Any:

    # --------------------------------------------------------
    # Allowed values
    # --------------------------------------------------------

    if rule.allowed_values:
        return "InvalidValue"

    # --------------------------------------------------------
    # Format rules
    # --------------------------------------------------------

    if rule.format_rule:

        if rule.format_rule == "email":
            return "invalid-email"

        if rule.format_rule == "phone":
            return "12345"

        if rule.format_rule == "url":
            return "not-a-url"

        if rule.format_rule.startswith("date:"):
            return "31-99-9999"

        if rule.format_rule.startswith("regex:"):
            return "invalid@value"

    # --------------------------------------------------------
    # Integer
    # --------------------------------------------------------

    if rule.data_type == "integer":

        if rule.maximum is not None:
            return int(rule.maximum) + 1

        if rule.minimum is not None:
            return int(rule.minimum) - 1

        return -999999

    # --------------------------------------------------------
    # Float
    # --------------------------------------------------------

    if rule.data_type == "float":

        if rule.maximum is not None:
            return float(rule.maximum) + 0.01

        if rule.minimum is not None:
            return float(rule.minimum) - 0.01

        return -999999.99

    # --------------------------------------------------------
    # String
    # --------------------------------------------------------

    if rule.data_type == "string":

        if rule.minimum is not None:
            return "x" * max(
                0,
                int(rule.minimum) - 1
            )

        if rule.maximum is not None:
            return "x" * (
                int(rule.maximum) + 1
            )

        return ""

    # --------------------------------------------------------
    # Boolean
    # --------------------------------------------------------

    if rule.data_type == "boolean":
        return "not_boolean"

    return None


# ============================================================
# Wrong type
# ============================================================

def _generate_wrong_type(
    rule: FieldRule
) -> Any:

    if rule.data_type == "string":
        return 12345

    if rule.data_type == "integer":
        return "not_an_integer"

    if rule.data_type == "float":
        return "not_a_float"

    if rule.data_type == "boolean":
        return "not_a_boolean"

    return None


# ============================================================
# Generate test cases
# ============================================================

def generate_test_cases(
    rules: list[FieldRule]
) -> list[dict]:

    test_cases = []

    if not rules:
        return test_cases

    # ========================================================
    # 1. ONE VALID CASE
    # ========================================================

    valid_data = {}

    for rule in rules:
        valid_data[rule.field_name] = (
            _generate_valid_value(rule)
        )

    test_cases.append(
        {
            "case_type": "valid",
            "field_name": None,
            "test_reason": "Valid test data",
            "expected_valid": True,
            "data": valid_data,
        }
    )

    # ========================================================
    # 2. FIELD-SPECIFIC TEST CASES
    # ========================================================

    for rule in rules:

        # ----------------------------------------------------
        # Create a FRESH valid dataset for every case.
        # ----------------------------------------------------

        def fresh_data():

            data = {}

            for current_rule in rules:
                data[current_rule.field_name] = (
                    _generate_valid_value(current_rule)
                )

            return data

        # ----------------------------------------------------
        # Minimum boundary
        # ----------------------------------------------------

        if rule.minimum is not None:

            value = _generate_boundary_value(
                rule,
                "min"
            )

            data = fresh_data()
            data[rule.field_name] = value

            test_cases.append(
                {
                    "case_type": "boundary",
                    "field_name": rule.field_name,
                    "test_reason": "At minimum boundary",
                    "expected_valid": True,
                    "data": data,
                }
            )

            # Below minimum

            value = _generate_boundary_value(
                rule,
                "below_min"
            )

            data = fresh_data()
            data[rule.field_name] = value

            test_cases.append(
                {
                    "case_type": "boundary",
                    "field_name": rule.field_name,
                    "test_reason": "Below minimum boundary",
                    "expected_valid": False,
                    "data": data,
                }
            )

        # ----------------------------------------------------
        # Maximum boundary
        # ----------------------------------------------------

        if rule.maximum is not None:

            value = _generate_boundary_value(
                rule,
                "max"
            )

            data = fresh_data()
            data[rule.field_name] = value

            test_cases.append(
                {
                    "case_type": "boundary",
                    "field_name": rule.field_name,
                    "test_reason": "At maximum boundary",
                    "expected_valid": True,
                    "data": data,
                }
            )

            # Above maximum

            value = _generate_boundary_value(
                rule,
                "above_max"
            )

            data = fresh_data()
            data[rule.field_name] = value

            test_cases.append(
                {
                    "case_type": "boundary",
                    "field_name": rule.field_name,
                    "test_reason": "Above maximum boundary",
                    "expected_valid": False,
                    "data": data,
                }
            )

        # ----------------------------------------------------
        # Invalid value
        # ----------------------------------------------------

        invalid_value = _generate_invalid_value(rule)

        if rule.allowed_values:

            reason = "Invalid allowed value"

        elif rule.format_rule == "email":

            reason = "Invalid email format"

        elif rule.format_rule == "phone":

            reason = "Invalid phone format"

        elif rule.format_rule == "url":

            reason = "Invalid URL format"

        elif rule.format_rule and rule.format_rule.startswith(
            "date:"
        ):

            reason = "Invalid date format"

        elif rule.format_rule and rule.format_rule.startswith(
            "regex:"
        ):

            reason = "Invalid regex format"

        else:

            reason = "Invalid value"

        data = fresh_data()
        data[rule.field_name] = invalid_value

        test_cases.append(
            {
                "case_type": "invalid",
                "field_name": rule.field_name,
                "test_reason": reason,
                "expected_valid": False,
                "data": data,
            }
        )

        # ----------------------------------------------------
        # Missing required
        # ----------------------------------------------------

        if rule.required:

            data = fresh_data()
            data[rule.field_name] = None

            test_cases.append(
                {
                    "case_type": "missing_required",
                    "field_name": rule.field_name,
                    "test_reason": "Missing required field",
                    "expected_valid": False,
                    "data": data,
                }
            )

        # ----------------------------------------------------
        # Wrong type
        # ----------------------------------------------------

        wrong_type_value = _generate_wrong_type(rule)

        data = fresh_data()
        data[rule.field_name] = wrong_type_value

        test_cases.append(
            {
                "case_type": "wrong_type",
                "field_name": rule.field_name,
                "test_reason": "Wrong data type",
                "expected_valid": False,
                "data": data,
            }
        )

    return test_cases