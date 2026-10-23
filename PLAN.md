# Implementation plan

> This file records my project-specific steps reviewed before coding. Replace the prompts below with the agreed plan; refer to R1–R3 rather than copying the requirements here.

## Steps
1. Create `tax_calculator.py` with a core function `calculate_tax(income, deductions)`.
2. Implement the standard deduction cap for R3 inside the calculation function.
3. Implement the progressive tax brackets logic for R1 and R2.
4. Create `test_tax_calculator.py` to automate the checks defined in EVIDENCE.md using Python's `unittest`.
5. Add a simple command-line interface (CLI) at the bottom of `tax_calculator.py` to ask the user for inputs and print the tax.

## Later changes, if any
Change initial plan from a basic calculator with 3 simple rules to a comprehensive calculator implementing all major Thai Revenue Department tax deductions. This required changing the data structure to use a dataclass for the inputs and outputs, and rewriting the automated tests.