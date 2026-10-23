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
- Command I ran: `python -m unittest test_tax_calculator.py`
- Final result: [Actual test count and outcome.]
- Correction and rerun, if needed: [Brief account, or None needed.]

## Realistic use and final judgment
- Task I tried: [One realistic use from start to finish.]
- Outcome: [What happened and whether it served the intended user/purpose.]
- Judgment: [Done / Partly done / Not done, with a brief reason based on the evidence.]
- Remaining limitation or unfinished work: [One specific item, or a useful next check.]