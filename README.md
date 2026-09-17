# Test Data Generation and Validation

A Python-based tool that generates and validates test data from a user-defined field-rule table.

The application automatically creates valid, invalid, boundary, missing-required, and wrong-data-type test cases and validates them against the provided rules.

AI is used only to explain the validation results. The actual validation decision is made by Python.

---

## 1. Project Overview

Testing forms and API payloads manually can be time-consuming, especially when many fields have different validation rules.

This project provides a simple tool where a user uploads a CSV file containing field rules. The application reads those rules, generates different test scenarios, validates the generated data, and presents the results through a Streamlit interface.

The goal is to make basic test-data generation and validation faster, more systematic, and easier to inspect.

---

## 2. Problem Statement

When testing a form or API payload, testers need to consider:

- Valid input
- Invalid input
- Minimum and maximum boundaries
- Missing required fields
- Incorrect data types
- Format violations
- Allowed-value violations

Creating these cases manually can result in repetitive work and missed edge cases.

This project automates the generation of these test cases based on user-provided field rules.

---

## 3. Objectives

The main objectives are to:

- Accept a user-defined field-rule table.
- Parse and normalize the provided rules.
- Generate realistic synthetic test data.
- Generate valid, invalid, and boundary test cases.
- Validate every generated test case using Python.
- Compare expected and actual validation results.
- Provide a summary of the generated test cases.
- Use AI only to explain validation results.
- Provide an easy-to-use Streamlit interface.
- Allow users to download the generated results as a CSV file.

---

## 4. Key Features

### Rule-Based Test Data Generation

The application reads field rules provided by the user and generates test data automatically.

### Valid Test Cases

Generates data that satisfies all defined field rules.

### Boundary Test Cases

Tests values:

- At the minimum
- Just below the minimum
- At the maximum
- Just above the maximum

### Invalid Test Cases

Generates values that violate rules such as:

- Email format
- Phone format
- URL format
- Date format
- Numeric ranges
- Allowed values
- Regular expressions

### Missing Required Fields

Generates test cases where required fields are intentionally left empty.

### Wrong Data Types

Generates values with an incorrect data type to verify type validation.

### Validation Results

Each generated case is validated and the expected and actual results are compared.

### AI Explanations

AI provides a short explanation of the already-determined Python validation result.

AI does not decide whether a test case is valid or invalid.

### CSV Export

Generated results can be downloaded for further testing or analysis.

---

## 5. How the Application Works

The overall workflow is:


User uploads Rule CSV
          ↓
Parse Rules
          ↓
Normalize Rules
          ↓
Generate Test Cases
          ↓
Validate Test Cases
          ↓
Generate Validation Summary
          ↓
Optional AI Explanation
          ↓
Display Results
          ↓
Download CSV
## 6. AI Usage

AI is intentionally limited to one task:

> Explain why a generated test case is valid, invalid, or a boundary case.

The validation process is controlled by Python.

```text
Generated Test Data
        ↓
Python Validation
        ↓
Validation Result
        ↓
AI Explanation
```

The AI component does not:

- Decide validity
- Change validation results
- Modify field rules
- Generate validation logic
- Override Python validation

This keeps the core testing logic deterministic and rule-based.

---

## 7. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application and validation logic |
| Pandas | Reading and processing rule tables |
| Streamlit | User interface |
| Pytest | Automated testing |
| Google Gemini | Validation-result explanations |
| Git & GitHub | Version control and project management |

---

## 8. Supported Rule Types

The application currently supports:

### Data Types

- String
- Integer
- Float
- Boolean

### Rule Types

- Required fields
- Minimum values/lengths
- Maximum values/lengths
- Allowed values
- Email format
- Phone format
- URL format
- Date format
- Regular expressions

The exact rules are determined by the uploaded rule table rather than being fixed to one particular dataset.

---

## 9. Input Rule Table

The application accepts a CSV rule table.

The required columns are:

```text
field_name
type
required
```

Optional columns include:

```text
min
max
allowed_values
format_rule
description
```

Example structure:

```text
field_name,type,required,min,max,allowed_values,format_rule,description
age,integer,True,18,65,,,Age of the user
email,string,True,,,,email,User email address
status,string,True,,,active|inactive|pending,,Account status
```

The application also handles accidental CSV index columns such as `Unnamed: 0`.

---

## 10. Example Generated Test Cases

For a rule such as:

```text
age
minimum = 18
maximum = 65
```

the generator can create:

```text
18 → At minimum boundary
17 → Below minimum boundary
65 → At maximum boundary
66 → Above maximum boundary
```

Other examples include:

```text
Invalid email
Missing required field
Wrong data type
Invalid allowed value
```

The generated output records the reason for each test case.

---

## 11. Validation

Python validates each generated value against its corresponding field rule.

The application records:

- Expected result
- Actual result
- Match status
- Field-level validation result
- Validation message

A test case is considered correctly processed when the actual Python validation result matches the expected result.

---

## 12. Project Structure

```text
test-data-generation-validation/
│
├── README.md
├── REQUIREMENTS.md
├── DESIGN.md
├── TESTING.md
├── TASKS.md
├── requirements.txt
├── app.py
│
├── src/
│   ├── __init__.py
│   ├── models.py
│   ├── rule_parser.py
│   ├── rule_normalizer.py
│   ├── generator.py
│   ├── validator.py
│   ├── ai_explainer.py
│   └── summary.py
│
├── tests/
│   ├── __init__.py
│   ├── test_parser.py
│   ├── test_normalizer.py
│   ├── test_generator.py
│   ├── test_validator.py
│   ├── test_summary.py
│   └── test_robustness.py
│
└── screenshots/
```

---

## 13. Installation

Clone the repository:

```bash
git clone https://github.com/Thrivi13/test-data-generation-validation.git
```

Move into the project directory:

```bash
cd test-data-generation-validation
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## 14. Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in the browser.

Upload a CSV rule table and use the interface to:

1. Parse the rules.
2. Generate test cases.
3. Validate the generated data.
4. View the validation results.
5. Download the results.

---

## 15. Running the Tests

The project uses `pytest` for automated testing.

Run:

```bash
pytest -q
```

Latest test result:

```text
38 passed
```

The automated tests cover parsing, normalization, test-data generation, validation, result summaries, and robustness scenarios.

More details are available in `TESTING.md`.

---

## 16. AI Configuration

AI explanations require a Gemini API key.

Set the environment variable:

### Windows Command Prompt

```bash
set GEMINI_API_KEY=your_api_key_here
```

### Windows PowerShell

```bash
$env:GEMINI_API_KEY="your_api_key_here"
```

Do not commit API keys or other secrets to GitHub.

The application can still perform the core test-data generation and validation without the AI explanation feature.

---

## 17. Testing Evidence

The project includes evidence of:

- Automated unit testing
- Boundary testing
- Negative testing
- Invalid rule-table handling
- Generated test-data verification
- End-to-end Streamlit testing
- Validation result comparison

Detailed testing information is documented in:

```text
TESTING.md
```

Screenshots and demonstration evidence are maintained separately as part of the project submission.

---

## 18. Current Limitations

- The application currently accepts CSV rule tables.
- Supported data types and validation formats are limited to the implemented rule set.
- AI explanations require a configured Gemini API key.
- Generated values are synthetic and intended for testing purposes.
- The current implementation is a prototype rather than a production test-management platform.
- The application does not currently provide a dedicated REST API.

---

## 19. Future Improvements

Possible future improvements include:

- Support for additional data types.
- More complex validation rules.
- Larger and more configurable test-data generation.
- REST API integration.
- Automated UI testing.
- Performance testing with larger datasets.
- Additional export formats.
- More advanced reporting and test coverage analysis.

---

## 20. Development Approach

The project was developed incrementally following an SDLC-based approach:

```text
Understand
    ↓
Design
    ↓
Build
    ↓
Test
    ↓
Handover
```

The development process included:

- Requirement analysis
- User stories and acceptance criteria
- Task breakdown
- Architecture and design
- Modular implementation
- Automated testing
- Defect fixing
- Documentation
- Final demonstration preparation

---

## 21. Repository Documentation

The repository contains the following supporting documents:

| Document | Purpose |
|---|---|
| `REQUIREMENTS.md` | Project requirements, user stories, scope, and acceptance criteria |
| `DESIGN.md` | Architecture, components, data flow, and design decisions |
| `TASKS.md` | Development task breakdown |
| `TESTING.md` | Testing strategy, scenarios, results, and defects |
| `README.md` | Project overview, setup, usage, and documentation |

---

## 22. Project Status

The core prototype is implemented and tested.

Current status:

- Rule parsing: Complete
- Rule normalization: Complete
- Test-data generation: Complete
- Validation engine: Complete
- Result processing: Complete
- AI explanation layer: Complete
- Streamlit interface: Complete
- Automated testing: Complete
- Testing documentation: Complete
- Final evidence and demonstration preparation: In progress
