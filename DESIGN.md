# Test Data Generation and Validation Tool

## 1. Design Overview

This document explains how I plan to design and build the Test Data Generation
and Validation Tool.

The application will take a field-rule table provided by the user and use
those rules to generate different types of test data.

The main flow will be:

1. Read the field-rule table.
2. Check and normalize the rules.
3. Generate valid, invalid, and boundary test cases.
4. Validate each generated case using Python.
5. Use AI to explain the validation result.
6. Display the results and summary through Streamlit.

The application will be designed to work with different rule tables instead
of being built around a fixed set of fields.

A key design decision is that Python will remain responsible for the actual
validation decision. AI will only be used after validation to provide a
short explanation.

---

# 2. Design Goals

The design will focus on the following goals:

- Keep the application generic and rule-driven.
- Avoid hardcoding specific field names.
- Keep test-data generation separate from validation.
- Keep validation deterministic and easy to test.
- Use AI only for explaining validation results.
- Keep the core Python logic separate from the Streamlit interface.
- Make individual parts of the application easy to understand and maintain.
- Make it possible to add new rule types in the future.
- Keep the first version simple and focused on the main project requirements.

---

# 3. Technology Stack

## Python

Python will be used as the main programming language for the project.

It will handle the core application logic, including:

- Reading and processing rules
- Generating test data
- Validating test cases
- Processing validation results
- Preparing information for the user interface

Python is a good fit for this project because the main work involves
structured data, rule checking, string processing, regular expressions, and
deterministic validation.

---

## Pandas

Pandas will be used to work with the field-rule table and the generated test
data.

It will be useful for:

- Reading CSV files
- Processing tabular rule data
- Storing generated test cases
- Creating validation-result tables
- Calculating summary information

---

## Streamlit

Streamlit will be used to build the user interface.

The application will allow the user to:

1. Upload a field-rule table.
2. Review the provided rules.
3. Generate test cases.
4. Run validation.
5. View the validation results.
6. View AI explanations.
7. Review the final summary.

The main business logic will stay outside Streamlit so that it can be tested
independently.

---

## LLM API

An LLM API will be used for one specific purpose: explaining validation
results.

The AI will receive information such as:

- Field name
- Generated value
- Relevant rule
- Test case category
- Python validation result
- Validation reason

It will then produce a short explanation that is easy for the user to
understand.

The AI will not decide whether the value is valid or invalid.

---

## pytest

pytest will be used for automated testing.

Tests will mainly cover:

- Rule parsing
- Rule normalization
- Test-data generation
- Validation logic
- Boundary cases
- Invalid inputs
- Error handling

---

## Git and GitHub

Git will be used for version control and GitHub will be used to maintain the
project repository.

The project will be developed in small stages rather than putting the entire
application into a single commit.

This will make the Git history useful for showing how the project was
developed.

---

# 4. High-Level Architecture

The application will follow a simple modular architecture.

                    User
                      |
                      v
              +---------------+
              |   Streamlit   |
              |      UI       |
              +-------+-------+
                      |
                      v
              +---------------+
              | Rule Parser & |
              |  Normalizer   |
              +-------+-------+
                      |
                      v
              +---------------+
              | Test Data     |
              |   Generator   |
              +-------+-------+
                      |
                      v
              +---------------+
              |  Validation   |
              |    Engine     |
              +-------+-------+
                      |
                      v
              +---------------+
              | Validation    |
              |    Results    |
              +-------+-------+
                      |
                      v
              +---------------+
              | AI Explainer  |
              |    (LLM)      |
              +-------+-------+
                      |
                      v
              +---------------+
              | Results and   |
              |    Summary    |
              +---------------+
    

# 5. Component Responsibilities

The application will be divided into a few simple components. Each component
will have a clear responsibility instead of putting all the logic into one
large file.

## 5.1 Streamlit UI

The Streamlit application will handle the user interaction and presentation.

It will be responsible for:

- Uploading the field-rule table
- Showing the provided rules
- Starting test-data generation
- Displaying generated test cases
- Displaying validation results
- Showing AI explanations
- Showing the final test summary
- Displaying user-friendly error messages

The main rule processing and validation logic will not be written directly
inside the UI.

---

## 5.2 Rule Parser

The rule parser will read the field-rule table and convert it into a format
that the rest of the application can work with.

It will check things such as:

- Required columns are present
- Field names are available
- Data types are supported
- Minimum and maximum values are usable
- Allowed values are readable
- Format rules are readable

If the rule table contains an invalid configuration, the parser should report
the problem clearly.

---

## 5.3 Rule Normalizer

The rule normalizer will convert the raw rules into a consistent internal
format.

For example, values such as:

- `True`
- `true`
- `TRUE`

should be interpreted consistently when they represent the same rule.

The normalizer will make the rules easier for both the generator and validator
to use.

---

## 5.4 Test Data Generator

The generator will create test cases based on the rules provided by the user.

It will generate three main categories:

- Valid
- Invalid
- Boundary

The generator will not be designed around specific field names.

For example, it should not contain special logic such as:


if field_name == "age":
    ...
## 5.5 Validation Engine

The validation engine will be responsible for checking whether a generated
test value follows the rules provided for that field.

It will handle checks such as:

- Required or optional fields
- Data type
- Minimum and maximum values
- Minimum and maximum string length
- Allowed values
- Regular expressions
- Supported formats such as email, phone, date, and URL

The validation result will be decided entirely by Python.

The validator should also return a reason along with the result.

For example:

**Value:** 17  
**Rule:** Minimum value is 18  
**Result:** Invalid  
**Reason:** The value is below the minimum allowed value.

---

## 5.6 AI Explainer

The AI explainer will be kept separate from the validation engine.

Its only purpose is to explain a result that has already been determined by
Python.

For example:

**Field:** age  
**Value:** 17  
**Rule:** Minimum value is 18  
**Python result:** Invalid

The AI could provide an explanation such as:

> The value is invalid because 17 is below the minimum allowed value of 18.

The AI response will only be shown as an explanation.

It will not be used to decide whether the test case is valid or invalid.

---

## 5.7 Result Processor

The result processor will combine the information produced by the generator
and validation engine.

A final test-case result can contain:

- Test case ID
- Field name
- Generated value
- Test case category
- Expected result
- Actual result
- Pass/Fail status
- Validation reason
- AI explanation

Keeping these details together will make the results easier to display and
review.

---

## 5.8 Summary

The summary part of the application will calculate overall statistics from
the generated test cases.

It will show information such as:

- Total number of test cases
- Number of valid cases
- Number of invalid cases
- Number of boundary cases
- Number of passed validations
- Number of failed validations

This will give the user a quick overview of the generated test data.

---

# 6. Data Flow

The application will process the input through the following stages:

User-Provided Rule Table  
↓  
Parse Rules  
↓  
Validate Rule Configuration  
↓  
Normalize Rules  
↓  
Generate Test Cases  
↓  
Python Validation  
↓  
Store Validation Result  
↓  
Generate AI Explanation  
↓  
Combine Final Results  
↓  
Display Results  
↓  
Summary

The order of these steps is important.

The application should first generate a test case and validate it using
Python. Only after the validation result is available should the AI
explanation be generated.

In simple terms:

Generated Test Case  
↓  
Python Validation  
↓  
Validation Result  
↓  
AI Explanation

This keeps the validation process deterministic.

---

# 7. Test Case Structure

Each generated test case should contain enough information to understand what
was generated and how it was validated.

A test case will conceptually contain:

- test_id
- field_name
- value
- category
- expected_result
- actual_result
- status
- validation_reason
- ai_explanation

The `category` will normally be one of:

- Valid
- Invalid
- Boundary

The `status` will indicate whether the generated case behaved as expected:

- PASS
- FAIL

For example:

**Test ID:** TC001  
**Field:** age  
**Value:** 25  
**Category:** Valid  
**Expected:** Valid  
**Actual:** Valid  
**Status:** PASS

---

# 8. Rule Representation

After parsing and normalization, each field will be represented using a
consistent structure.

A field rule can contain:

- field_name
- data_type
- required
- minimum
- maximum
- allowed_values
- format_rule
- description

Not every field will necessarily have every property.

For example, one field may only have a data type and required flag, while
another field may also have minimum, maximum, and format rules.

The application should handle these optional properties without causing
errors.

---

# 9. Test Data Generation Strategy

The generator will create test cases based on the rules provided by the user.

The three main categories are:

- Valid cases
- Invalid cases
- Boundary cases

The generator should use the available rules instead of depending on
specific field names.

## 9.1 Valid Cases

Valid cases should satisfy all applicable rules.

Depending on the rules, examples could include:

- A number inside an allowed range
- A string with an acceptable length
- A value from an allowed-values list
- A correctly formatted email
- A correctly formatted date
- A value that matches a regular expression

The generated values should be simple and predictable where possible so that
the user can easily understand the test cases.

## 9.2 Invalid Cases

Invalid cases will intentionally violate one or more applicable rules.

Possible examples include:

- A value below the minimum
- A value above the maximum
- A string shorter than the minimum length
- A string longer than the maximum length
- A value not present in an allowed-values list
- An incorrectly formatted value
- A missing required value
- A value that does not match a regular expression

Whenever possible, an invalid case should violate one main rule at a time.
This makes the reason for the failure easier to understand.

## 9.3 Boundary Cases

Boundary cases will focus on values close to important limits.

For numeric ranges, the generator can consider:

- Minimum - 1
- Minimum
- Minimum + 1
- Maximum - 1
- Maximum
- Maximum + 1

For string-length rules, similar cases can be generated around the minimum
and maximum lengths.

For example:

- Minimum length - 1
- Minimum length
- Minimum length + 1
- Maximum length - 1
- Maximum length
- Maximum length + 1

The Python validation engine will still determine whether each boundary case
is actually valid or invalid.

This is important because a boundary case is a category of test data, while
its validation result depends on the rule.

---

# 10. Validation Strategy

The validation engine will evaluate every generated test case against its
normalized rules.

A simplified validation process is:

1. Check the required rule.
2. Check the data type.
3. Check the minimum and maximum values or lengths.
4. Check allowed values.
5. Check format or regular-expression rules.
6. Return the validation result and reason.

The exact checks will depend on the rules available for the field.

The validator should return both the validation result and a useful reason.

For example:

**Valid:** False  
**Reason:** Value is above the maximum allowed value of 65.

This reason can also be provided to the AI explanation component.

---

# 11. Expected vs Actual Result

Each generated test case will have an expected result based on its category
and the generation logic.

The actual result will come from the Python validation engine.

For example:

**Category:** Invalid  
**Expected:** Invalid  
**Actual:** Invalid  
**Status:** PASS

If an invalid test case is unexpectedly accepted:

**Category:** Invalid  
**Expected:** Invalid  
**Actual:** Valid  
**Status:** FAIL

This comparison helps us verify not only the validator but also whether the
test-data generator is producing cases that behave as intended.

---

# 12. AI Integration Design

AI will be integrated only after the Python validation step.

The overall flow will be:

Generated Test Case  
↓  
Python Validator  
↓  
Validation Result + Reason  
↓  
AI Explainer  
↓  
Human-readable Explanation

The AI prompt will contain the information needed to explain the result.

For example:

**Field:** age  
**Value:** 17  
**Rule:** minimum value = 18  
**Category:** Invalid  
**Python result:** Invalid  
**Validation reason:** value is below the minimum

The expected output is a short explanation that is easy for a tester to
understand.

The AI explanation will not be used as part of the validation process.

---

# 13. Error Handling

The application should handle errors at different stages instead of allowing
unexpected errors to reach the user.

## Input Errors

Examples include:

- No file provided
- Empty file
- Missing required columns

The application should show a clear message explaining what is wrong.

## Rule Errors

Examples include:

- Duplicate field names
- Unsupported data types
- Minimum greater than maximum
- Invalid regular expression
- Invalid rule configuration

These errors should be detected before test-data generation begins.

## Generation Errors

If the application cannot generate a suitable value for a particular rule,
it should report the problem instead of silently generating incorrect data.

## AI Errors

The AI service may be unavailable, the API key may be missing, or an API
request may fail.

These failures should not prevent the user from seeing the generated test
cases and Python validation results.

If an AI explanation cannot be generated, the application should still show
the validation result and indicate that the explanation is unavailable.

---

# 14. Project Structure

The planned project structure is:

test-data-generation-validation/
│
├── README.md
├── REQUIREMENTS.md
├── DESIGN.md
├── TESTING.md
├── requirements.txt
├── app.py
│
├── src/
│   ├── __init__.py
│   ├── models.py
│   ├── rule_parser.py
│   ├── generator.py
│   ├── validator.py
│   ├── ai_explainer.py
│   └── summary.py
│
├── tests/
│   ├── test_parser.py
│   ├── test_generator.py
│   └── test_validator.py
│
└── screenshots/

This structure may be adjusted during implementation if we find a simpler or
better way to organize the project.

The main goal is to keep the different responsibilities separate.

---

# 15. Separation of Responsibilities

Each part of the application will have a specific responsibility.

| Component | Responsibility |
|---|---|
| Streamlit UI | User interaction and displaying results |
| Rule Parser | Reading and checking input rules |
| Rule Normalizer | Converting rules into a consistent format |
| Generator | Creating valid, invalid, and boundary cases |
| Validator | Making the actual validation decision |
| Result Processor | Combining generation and validation information |
| AI Explainer | Explaining the Python validation result |
| Summary | Calculating overall test statistics |
| Tests | Checking that the application works correctly |

This separation will make it easier to understand, test, and modify
individual parts of the application.

---

# 16. Security and Configuration

The AI API key should never be written directly into the source code.

It should be stored using an environment variable or Streamlit secrets.

For example:

OPENAI_API_KEY=<configured securely>

The actual API key must not be committed to GitHub.

A `.gitignore` file will be used to prevent local environment files and
sensitive configuration files from being accidentally committed.

---

# 17. Main Design Decisions

## Python Handles Validation

Python will make the actual validation decision because the validation logic
needs to be deterministic and easy to test.

## AI Is an Explanation Layer

AI is required by the project, but it should not control the validation
process.

It will therefore only explain results that have already been determined by
Python.

## Rule-Driven Design

The application will use the rules supplied by the user instead of assuming
a fixed set of field names.

This allows the same application to work with different rule tables.

## Modular Architecture

The parser, generator, validator, AI explainer, summary logic, and UI will be
kept separate.

This makes it easier to test and modify individual components.

## Streamlit for the Interface

Streamlit will provide the interactive interface while allowing the core
Python logic to remain independent from the UI.

## Pandas for Tabular Data

Pandas will be used because the project works mainly with tabular rule data
and generated test results.

---

# 18. Design Limitations

The first version will focus on the rule types defined in the requirements.

It will not attempt to become a complete API testing platform or test
management system.

More advanced rule types and integrations can be added later if needed.

The main goal of the first version is to implement the required functionality
properly rather than adding unnecessary features.

---

# 19. Implementation Plan

After completing the design, implementation will be done step by step.

The planned order is:

1. Implement the rule parser.
2. Implement rule normalization.
3. Implement test-data generation.
4. Implement Python validation.
5. Implement result processing and summary.
6. Integrate the AI explanation layer.
7. Build the Streamlit interface.
8. Add automated tests.
9. Improve error handling.
10. Complete documentation and screenshots.

Each major stage will be committed separately so that the Git history shows
the development process clearly.

The implementation may lead to small design changes. If that happens, this
document will be updated so that it continues to reflect the actual system.
