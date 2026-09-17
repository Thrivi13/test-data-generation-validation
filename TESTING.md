# Testing

## 1. Testing Objective

The purpose of testing is to verify that the application correctly:

- Reads the field-rule table.
- Validates the provided rules.
- Generates valid test data.
- Generates boundary-value test cases.
- Generates invalid test cases.
- Generates missing-required-field cases.
- Generates wrong-data-type cases.
- Validates generated data against the defined rules.
- Compares expected and actual validation results.
- Handles invalid rule tables with clear errors.

---

## 2. Testing Approach

The project uses a combination of:

- Unit testing
- Functional testing
- Boundary testing
- Negative testing
- Input robustness testing
- Manual end-to-end testing

Automated tests are implemented using `pytest`.

The validation decision is made by the Python validation engine. AI is used only to explain the validation result and does not determine whether a test case is valid or invalid.

---

## 3. Automated Testing

The automated test suite covers the following modules:

- Rule Parser
- Rule Normalizer
- Test Data Generator
- Validation Engine
- Result Summary
- Robustness handling

### Test command

pytest -q
## 4. Functional Test Scenarios

| Area | Test Scenario | Expected Result |
|---|---|---|
| Parser | Valid rule table | Rules are parsed successfully |
| Parser | Missing required column | Clear error is returned |
| Parser | Empty rule table | Clear error is returned |
| Parser | Duplicate field name | Clear error is returned |
| Parser | Empty field name | Clear error is returned |
| Parser | Unnamed index column | Index column is ignored |
| Normalizer | Valid required value | Converted to boolean |
| Normalizer | Invalid required value | Error is returned |
| Normalizer | Unsupported data type | Error is returned |
| Normalizer | Numeric boundary | Boundary is converted correctly |
| Generator | Valid data | Valid test case is generated |
| Generator | Minimum boundary | Minimum value is generated |
| Generator | Below minimum | Invalid boundary value is generated |
| Generator | Maximum boundary | Maximum value is generated |
| Generator | Above maximum | Invalid boundary value is generated |
| Generator | Invalid format | Invalid format case is generated |
| Generator | Invalid allowed value | Invalid allowed-value case is generated |
| Generator | Missing required field | Missing value is generated |
| Generator | Wrong data type | Incorrect data type is generated |
| Validator | Valid value | Value is marked valid |
| Validator | Invalid value | Value is marked invalid |
| Validator | Boundary value | Boundary is validated correctly |
| Summary | Result counting | Correct summary is generated |

---

## 5. Boundary Testing

Boundary testing checks values at and immediately outside the defined limits.

For example, if:

age
minimum = 18
maximum = 65

the generator creates:

18  → At minimum boundary
17  → Below minimum boundary
65  → At maximum boundary
66  → Above maximum boundary

The same approach is used for string length rules.

For example:

minimum length = 3
maximum length = 20

the generator tests:

aaa                    → At minimum boundary
aa                     → Below minimum boundary
aaaaaaaaaaaaaaaaaaaa   → At maximum boundary
aaaaaaaaaaaaaaaaaaaaa  → Above maximum boundary


## 6. Negative Testing

Negative test cases are used to verify that invalid data is rejected correctly.

The project tests cases such as:

- Missing required fields
- Invalid email formats
- Invalid phone formats
- Invalid URL formats
- Invalid date formats
- Values outside numeric ranges
- Values outside allowed-value lists
- Incorrect data types
- Values that do not satisfy regular expressions

Each negative test case has an expected validation result of `False`.


## 7. Input Robustness Testing

The application was tested using intentionally invalid rule tables.

### Invalid required value

Example:

required = yes

Expected result:

Invalid rule table: Required must be True or False.


### Unsupported data type

Example:

type = decimal128

Expected result:

Invalid rule table: Unsupported data type: decimal128


### Invalid numeric boundary

A non-numeric value supplied as a minimum or maximum boundary should be rejected during rule normalization.


## 8. Generated Data Verification

Generated test data was manually inspected to verify that:

- Each test case contains the correct case type.
- Boundary values are generated correctly.
- Invalid values violate the intended rule.
- Missing-required cases contain missing values.
- Wrong-type cases contain an incorrect data type.
- Expected validation results are recorded.
- Actual validation results are recorded.
- The expected and actual results can be compared.

The generator creates fresh synthetic data for each test case. The field under test is changed according to the specific scenario while the other fields receive newly generated valid values.


## 9. End-to-End Testing

The complete application was tested through the Streamlit interface.

### Application flow

Upload Rule CSV
      ↓
Parse Rules
      ↓
Normalize Rules
      ↓
Generate Test Data
      ↓
Validate Test Data
      ↓
Display Results
      ↓
Download Results

The generated results contain information such as:

- Case ID
- Case type
- Field name
- Test reason
- Expected result
- Actual result
- Match status
- Generated test data


## 10. AI Testing

AI is used only after Python validation has completed.

The flow is:

Generated Test Case
        ↓
Python Validation
        ↓
Validation Result
        ↓
AI Explanation

Python determines whether the test case is valid or invalid.

The AI component receives the existing validation result and provides a short explanation.

The AI does not:

- Decide validity
- Change validation results
- Modify field rules
- Generate validation logic
- Override Python validation

During development, AI requests were limited to avoid unnecessary API usage. The AI explanation feature is available for demonstration when an API key is configured.


## 11. Defects Found and Fixed

### Defect 1 — Unnamed CSV index column

**Problem:** CSV files could contain an automatically generated `Unnamed:` index column.

**Fix:** The parser was updated to ignore columns beginning with `Unnamed:`.


### Defect 2 — Invalid rule values

**Problem:** Invalid values such as unsupported data types and invalid `required` values needed to be handled clearly.

**Fix:** Validation checks were added during rule normalization.


### Defect 3 — Test reason missing from results

**Problem:** The generator created a test reason, but the validation result initially did not preserve it.

**Fix:** `test_reason` was added to the validation result.


### Defect 4 — Repeated generated data

**Problem:** Earlier versions reused the same valid dataset across multiple test cases.

**Fix:** The generator was changed to create a fresh synthetic dataset for every test case while modifying the field under test according to the scenario.


## 12. Test Result

The latest automated test execution produced:

38 passed

The test suite successfully covers the core parsing, normalization, generation, validation, summary, and robustness functionality.

Manual testing also verified the main Streamlit workflow from rule-table upload through test-data generation, validation, result display, and CSV download.


## 13. Current Limitations

- The application currently accepts CSV rule tables.
- The supported data types and validation formats are limited to the implemented rule set.
- AI explanations require a configured Gemini API key.
- Generated values are synthetic and intended for testing purposes.
- The current application is a prototype rather than a production test-management platform.


## 14. Future Testing Improvements

Future versions could include:

- Larger rule tables
- More complex validation rules
- Additional data types
- Performance testing with large datasets
- More extensive randomized testing
- Automated UI testing
- API-level testing if a REST API is introduced
