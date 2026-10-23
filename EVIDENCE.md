# Checks and decisions

> This file records what I checked, what actually happened, and why I accepted or changed the work. It does not repeat setup instructions or the implementation plan.

## Concrete checks
| Check / requirement | Given | When | Expected result | Actual result / pass or fail |
|---|---|---|---|---|
| C1 / R1, R2 — normal case | Income: 300,000 | Calculate tax | Deductions: 160k. Net: 140k. Tax is 0. | Actual result matched expected. Pass. |
| C2 / R3 — boundary or failure case | Income: 500,000, Health Ins: 25,000, Life Ins: 90,000 | Calculate tax | Insurance capped at 100k. Net: 240k. Tax: 4,500. | Actual result matched expected. Pass. |

## Two review decisions
- Plan decision: I decided to expand the scope to cover the full Thai Revenue Department rules because a realistic calculator is much more useful.
- Code decision: In `tax_calculator.py`, I grouped the allowances into dictionaries and used a combined cap for health and life insurance to keep the logic clean.

## Automated tests
- Test file and behaviour checked: `test_tax_calculator.py` checking normal calculation and deduction boundary.
- Command I ran: `python3 -m unittest test_tax_calculator.py`
Final result: Ran 2 tests. Both passed successfully.
- Correction and rerun, if needed: I initially had an ImportError because the main function name changed to `calculate_tax_details`[cite: 3], and I needed to run the tests using `python3` on my Mac.

## Realistic use and final judgment
- Task I tried: I ran `python3 tax_calculator.py` and calculated tax for an income of 600,000 THB, with a spouse, and 50,000 THB in provident fund contributions.
- Outcome: The CLI successfully grouped my inputs, capped my standard expense at 100,000 THB, and provided a clear, itemized breakdown of my net income and the final tax payable.
- Judgment: Done. The calculator correctly applying Thai Revenue Department rules and complete tax calculation requirement.
- Remaining limitation or unfinished work: The command-line interface asks a lot of questions one by one. It will be better to continue on building a web interface (like a form) where users can fill the blank instead of keep answering and press enter.