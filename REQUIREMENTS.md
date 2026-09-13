# Test Data Generation and Validation Tool

## 1. Project Overview

The goal of this project is to build a tool that can automatically generate
test data based on a field-rule table provided by the user.

The tool will generate three main types of test cases:

- Valid test cases
- Invalid test cases
- Boundary test cases

After generating the test data, the application will validate each case
against the given rules using Python.

AI will be used for only one task in this project: explaining why a generated
test case is valid, invalid, or a boundary/edge case.

The actual validation decision will be made by Python and not by AI.

---

## 2. Problem Statement

When testing forms or APIs, test data is often created manually. This can be
time-consuming, and it is also easy to miss important negative and boundary
cases.

For example, when a field has a minimum and maximum value, it is useful to
test values inside the range as well as values just below and above the
limits.

This project aims to automate this process by taking validation rules as
input and generating useful test cases from those rules.

---

## 3. Objectives

The application should be able to:

1. Accept a field-rule table provided by the user.
2. Read and validate the rules from the table.
3. Generate valid, invalid, and boundary test cases.
4. Validate every generated test case using Python.
5. Compare the expected result with the actual validation result.
6. Use AI to explain the validation result.
7. Display the generated test data and validation results clearly.
8. Provide a summary of the generated test cases.
9. Handle incorrect or unsupported rules properly.
10. Keep the application modular so that it can be extended later.

---

## 4. Target Users

The main users of this tool would be:

- QA engineers
- Test engineers
- Software developers

It can be useful for anyone who needs to quickly create and review test data
for a form or API.

---

## 5. User Stories

### User Story 1 - Provide Rules

As a tester, I want to provide a field-rule table so that the application can
understand the validation rules I want to test.

### User Story 2 - Generate Valid Test Cases

As a tester, I want the application to generate valid test cases so that I
do not have to create all valid inputs manually.

### User Story 3 - Generate Invalid Test Cases

As a tester, I want the application to generate invalid test cases so that I
can test how a form or API handles incorrect input.

### User Story 4 - Generate Boundary Test Cases

As a tester, I want values around important limits to be generated so that I
can test minimum and maximum boundary conditions.

### User Story 5 - Validate Test Cases

As a tester, I want every generated test case to be checked against the
provided rules so that I can verify whether the generated data is actually
valid or invalid.

### User Story 6 - Understand Validation Results

As a tester, I want to see a short explanation for each result so that I can
understand why a test case passed, failed, or represents a boundary/edge case.

### User Story 7 - Review Results

As a tester, I want to see the generated test cases and validation results in
a table so that I can easily review them.

### User Story 8 - Reuse the Tool

As a developer, I want the application to use the supplied rules dynamically
instead of hardcoding specific field names so that the tool can work with
different rule tables.

---

# 6. Functional Requirements

Functional requirements describe what the application should do.

## FR-01: Accept Rule Table

The application should accept a field-rule table provided by the user.

The table can contain information such as:

- Field name
- Data type
- Required/optional
- Minimum value or length
- Maximum value or length
- Allowed values
- Format rule
- Description

The application should not depend on a fixed set of field names.

---

## FR-02: Validate the Rule Table

Before generating test cases, the application should check whether the
provided rule table is valid and usable.

It should identify problems such as:

- Missing required columns
- Empty field names
- Duplicate field names
- Unsupported data types
- Invalid minimum or maximum values
- Minimum value greater than maximum value
- Invalid regular expressions
- Incorrect rule configuration

The application should show a clear error message instead of failing
unexpectedly.

---

## FR-03: Normalize the Rules

The application should convert the input rules into a consistent internal
format before using them for generation and validation.

This will make rule handling easier and more consistent throughout the
application.

---

## FR-04: Generate Test Data

The application should generate test cases based on the rules provided by
the user.

The generated cases should be divided into:

- Valid cases
- Invalid cases
- Boundary cases

The generation logic should come from the supplied rules rather than
hardcoded field-specific logic.

---

## FR-05: Generate Valid Cases

Valid test cases should satisfy all applicable rules.

Depending on the rules provided, examples could include:

- A value within an allowed range
- A string within the allowed length
- A value from an allowed-values list
- A correctly formatted value
- A valid value for the specified data type

---

## FR-06: Generate Invalid Cases

Invalid test cases should intentionally violate one or more rules.

Examples include:

- Value below the minimum
- Value above the maximum
- String shorter than the minimum length
- String longer than the maximum length
- Value not present in an allowed-values list
- Incorrect format
- Missing required value
- Value that does not match a regular expression

---

## FR-07: Generate Boundary Cases

The application should generate test cases around important limits.

For numeric minimum and maximum values, the generator should consider cases
such as:

- Minimum - 1
- Minimum
- Minimum + 1
- Maximum - 1
- Maximum
- Maximum + 1

For string-length rules, similar cases should be generated around the minimum
and maximum lengths.

The validation result for each boundary case should be determined by the
Python validation logic.

---

## FR-08: Validate Generated Test Cases

The application should validate every generated test case using Python.

The validation should be deterministic. The same input and rules should
produce the same validation result.

Python should decide whether the case is valid or invalid.

AI should not be used to make the validation decision.

---

## FR-09: Store Validation Results

For each generated test case, the application should provide information such
as:

- Test case ID
- Field/value information
- Test case category
- Expected result
- Actual result
- Pass/Fail status
- Reason for failure, when applicable

---

## FR-10: Generate AI Explanations

AI will have one specific responsibility in this project:

> Explain the validation result that has already been determined by Python.

For example:

**Value:** 17  
**Rule:** Minimum allowed value is 18  
**Python result:** Invalid  

**AI explanation:**  
The value is invalid because it is below the minimum allowed value of 18.

AI should not:

- Decide whether a test case is valid or invalid
- Decide whether a test case is a boundary case
- Change the validation result produced by Python
- Modify or override the user-provided rules
- Generate the actual validation logic
- Replace the Python validation engine



---

## FR-11: Display Results

The application should display the generated test cases and their validation
results in a clear table.

The user should be able to easily identify:

- Test case category
- Generated value
- Expected result
- Actual result
- Pass/Fail status
- Explanation

---

## FR-12: Provide a Test Summary

The application should provide a summary containing information such as:

- Total test cases
- Valid cases
- Invalid cases
- Boundary cases
- Passed validations
- Failed validations

Important negative and boundary cases should also be easy to identify.

---

## FR-13: Handle Errors

The application should handle invalid inputs and unsupported configurations
gracefully.

It should provide understandable error messages instead of displaying
unhandled exceptions to the user.

---

# 7. Initial Rule Capabilities

The first version of the application should support common data types and
validation rules.

## Data Types

- String
- Integer
- Float
- Boolean

## Rules

- Required/optional
- Minimum value
- Maximum value
- Minimum string length
- Maximum string length
- Allowed values
- Regular expressions
- Common formats such as email, phone, date, and URL

The design should allow more rule types to be added later.

---

# 8. Expected Outputs

The application should produce three main outputs.

## 8.1 Generated Test Data Table

A table containing the generated test cases.

Example:

| Test ID | Field | Value | Category |
|---|---|---|---|
| TC001 | example_field | example_value | Valid |
| TC002 | example_field | boundary_value | Boundary |
| TC003 | example_field | invalid_value | Invalid |

The example above is only to show the output format. The actual fields and
values will come from the rule table provided by the user.

## 8.2 Validation Results

A table showing the expected and actual validation results.

Example:

| Test ID | Expected | Actual | Status |
|---|---|---|---|
| TC001 | Valid | Valid | PASS |
| TC002 | Invalid | Invalid | PASS |

## 8.3 AI Explanation

A short explanation of why the generated case is valid, invalid, or a
boundary/edge case.

---

# 9. Non-Functional Requirements

Non-functional requirements describe how the application should behave and
the qualities the application should have.

## NFR-01: Maintainability

The application should be divided into logical parts such as:

- Rule parsing
- Rule normalization
- Test-data generation
- Validation
- AI explanation
- User interface

This will make the code easier to understand, maintain, and modify.

---

## NFR-02: Reusability

The core logic should work with different rule tables without requiring
changes for individual field names.

The application should be driven by the rules supplied by the user.

---

## NFR-03: Testability

Important rule-handling, test-data generation, and validation logic should
have automated tests.

The core logic should be separated from the UI so that it can be tested
independently.

---

## NFR-04: Usability

The application should provide a simple workflow:

1. Provide the rule table.
2. Review the rules.
3. Generate test cases.
4. Validate the cases.
5. Review the results.
6. View explanations and the summary.

The results should be easy to understand even for a user who is not familiar
with the internal code.

---

## NFR-05: Transparency

The application should clearly show which result was determined by Python and
which part was generated by AI.

The user should be able to understand the reason for a validation result
without confusing the AI explanation with the actual validation decision.

---

## NFR-06: Reliability

The application should handle invalid rule tables, unsupported rules, and
invalid generated values without unexpected crashes.

---

## NFR-07: Extensibility

The project should be structured so that new data types or validation rules
can be added later without changing the complete application.

---

# 10. Technology Stack

The planned technology stack is:

- **Python** - Main programming language and validation logic
- **Pandas** - Reading and processing rule and test-data tables
- **Streamlit** - User interface
- **LLM API** - Generating explanations for validation results
- **Git/GitHub** - Version control and project submission
- **pytest** - Automated testing

---

# 11. High-Level Workflow


User-Provided Rule Table
          |
          v
      Read Rules
          |
          v
   Validate / Normalize
          |
          v
   Generate Test Cases
          |
     +----+----+
     |    |    |
     v    v    v
   Valid Invalid Boundary
     |    |    |
     +----+----+
          |
          v
   Python Validation
          |
          v
   Validation Results
          |
          v
    AI Explanation
          |
          v
    Display Results
          |
          v
        Summary
        # 12. Scope

## In Scope

The initial version of the project will include:

- User-provided field-rule table
- Rule parsing and normalization
- Valid test-data generation
- Invalid test-data generation
- Boundary test-data generation
- Deterministic validation using Python
- AI-generated explanations
- Validation results table
- Test summary
- Streamlit interface
- Automated tests
- Git/GitHub version control
- Project documentation

## Out of Scope for the Initial Version

The first version will not focus on:

- Browser automation
- Complete end-to-end API automation
- Database testing
- Load or performance testing
- Penetration testing
- AI-based validation
- Automatically changing user-defined rules
- Building a complete test-management system

These can be considered as possible future improvements if required.

---

# 13. Project Constraints

The project will follow these main constraints:

1. The user-provided rule table will be treated as the source of truth.
2. Field names should not be hardcoded into the main generation or validation
   logic.
3. Python must make the actual validation decision.
4. AI must only explain the result determined by Python.
5. The first version should focus on the required functionality instead of
   adding unnecessary features.
6. The code should remain simple enough for another developer to understand
   and run.
7. The application should work with different rule tables instead of being
   designed only for the sample input.

---

# 14. Risks and How I Plan to Handle Them

| Risk | How I plan to handle it |
|---|---|
| Generated data does not follow the rules | Validate every generated case using the validation engine |
| Generator and validator produce different results | Keep rule interpretation consistent across the application |
| AI gives an incorrect explanation | Provide AI with the Python validation result and relevant rule information |
| Invalid rule table causes errors | Validate and normalize the rule table before generation |
| Hardcoded fields make the tool difficult to reuse | Drive the application from the supplied rule table |
| Too many features make the project incomplete | Focus on the required functionality first |
| Another developer cannot run the project | Provide clear setup, usage, and testing documentation |
| Unsupported rule types are provided | Detect them and show a clear message to the user |
| Boundary cases are generated incorrectly | Validate boundary cases against the same Python validation logic |

---

# 15. Acceptance Criteria

The project will be considered successful when:

- A user can provide a field-rule table.
- The application can read and validate the provided rules.
- The application does not depend on hardcoded field names.
- Valid, invalid, and boundary cases can be generated.
- Every generated case is validated using Python.
- Expected and actual validation results can be compared.
- AI provides explanations without making validation decisions.
- Invalid rule configurations are handled clearly.
- Results are displayed in an understandable format.
- A summary of the generated cases is available.
- Important generation and validation logic has automated tests.
- Boundary and negative cases are covered by testing.
- Another developer can run the project using the documentation.

---

# 16. Definition of Done

The project will be considered complete when:

- [ ] Requirements are documented.
- [ ] User stories and tasks are planned.
- [ ] System design and architecture are documented.
- [ ] Rule parsing and normalization are implemented.
- [ ] Test-data generation is implemented.
- [ ] Deterministic validation is implemented.
- [ ] AI explanation is integrated according to the project requirement.
- [ ] Streamlit interface is implemented.
- [ ] Automated tests are added.
- [ ] Boundary and negative cases are tested.
- [ ] Error handling is demonstrated.
- [ ] Testing results are documented.
- [ ] README contains setup and usage instructions.
- [ ] Git history shows incremental development.
- [ ] Screenshots/evidence of the working application are available.
- [ ] The repository is ready for another developer to understand and run.
