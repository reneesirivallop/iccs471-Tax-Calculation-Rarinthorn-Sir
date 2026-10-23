"""Thai personal income tax calculator.

The calculation functions in this module do not perform input or output.  The
CLI at the bottom of the file is only a user-interface layer around them.
Amounts are annual amounts in Thai baht.
"""

from dataclasses import dataclass


STANDARD_EXPENSE_RATE = 0.50
STANDARD_EXPENSE_CAP = 100_000.0
PERSONAL_ALLOWANCE = 60_000.0
SPOUSE_ALLOWANCE = 60_000.0
CHILD_ALLOWANCE = 30_000.0
PARENT_ALLOWANCE = 30_000.0
SOCIAL_SECURITY_CAP = 10_500.0
LIFE_INSURANCE_CAP = 100_000.0
HEALTH_INSURANCE_CAP = 25_000.0
PROVIDENT_FUND_CAP = 500_000.0
RMF_CAP = 500_000.0
RETIREMENT_SAVINGS_COMBINED_CAP = 500_000.0
MORTGAGE_INTEREST_CAP = 100_000.0
DONATION_RATE_CAP = 0.10


@dataclass(frozen=True)
class TaxCalculation:
    """The itemized result of a Thai personal income tax calculation."""

    total_income: float
    standard_expense_deduction: float
    personal_and_family_allowances: float
    insurance_and_savings_deductions: float
    mortgage_interest_deduction: float
    total_allowances_and_deductions: float
    donation_deduction: float
    net_income_before_donations: float
    final_net_income: float
    tax_payable: float


def _non_negative_amount(value: float, name: str) -> float:
    """Return a non-negative amount or raise a useful validation error."""
    amount = float(value)
    if amount < 0:
        raise ValueError(f"{name} cannot be negative.")
    return amount


def _non_negative_count(value: int, name: str) -> int:
    """Return a non-negative whole-number count."""
    count = int(value)
    if count < 0 or count != value:
        raise ValueError(f"{name} must be a non-negative whole number.")
    return count


def calculate_progressive_tax(taxable_income: float) -> float:
    """Calculate tax using Thailand's annual progressive PIT brackets."""
    taxable_income = max(0.0, float(taxable_income))
    brackets = (
        (150_000.0, 0.00),
        (300_000.0, 0.05),
        (500_000.0, 0.10),
        (750_000.0, 0.15),
        (1_000_000.0, 0.20),
        (2_000_000.0, 0.25),
        (5_000_000.0, 0.30),
        (float("inf"), 0.35),
    )

    tax = 0.0
    lower_bound = 0.0
    for upper_bound, rate in brackets:
        taxable_at_rate = min(taxable_income, upper_bound) - lower_bound
        if taxable_at_rate > 0:
            tax += taxable_at_rate * rate
        if taxable_income <= upper_bound:
            break
        lower_bound = upper_bound
    return tax


def calculate_tax_details(
    income: float,
    spouse_no_income: bool = False,
    children: int = 0,
    qualified_parents: int = 0,
    social_security: float = 0.0,
    life_insurance: float = 0.0,
    health_insurance: float = 0.0,
    provident_fund: float = 0.0,
    rmf: float = 0.0,
    mortgage_interest: float = 0.0,
    donations: float = 0.0,
) -> TaxCalculation:
    """Calculate Thai income tax and apply the requested deduction rules."""
    total_income = _non_negative_amount(income, "Income")
    children = _non_negative_count(children, "Number of children")
    qualified_parents = _non_negative_count(
        qualified_parents, "Number of qualified parents"
    )

    standard_expense = min(
        total_income * STANDARD_EXPENSE_RATE, STANDARD_EXPENSE_CAP
    )
    family_allowances = (
        PERSONAL_ALLOWANCE
        + (SPOUSE_ALLOWANCE if spouse_no_income else 0.0)
        + children * CHILD_ALLOWANCE
        + qualified_parents * PARENT_ALLOWANCE
    )

    social_security_deduction = min(
        _non_negative_amount(social_security, "Social Security contributions"),
        SOCIAL_SECURITY_CAP,
    )
    life_insurance_deduction = min(
        _non_negative_amount(life_insurance, "Life Insurance premiums"),
        LIFE_INSURANCE_CAP,
    )
    health_insurance_deduction = min(
        _non_negative_amount(health_insurance, "Health Insurance premiums"),
        HEALTH_INSURANCE_CAP,
        LIFE_INSURANCE_CAP - life_insurance_deduction,
    )
    provident_fund_deduction = min(
        _non_negative_amount(provident_fund, "Provident Fund contributions"),
        total_income * 0.15,
        PROVIDENT_FUND_CAP,
    )
    rmf_deduction = min(
        _non_negative_amount(rmf, "RMF contributions"),
        total_income * 0.30,
        RMF_CAP,
        RETIREMENT_SAVINGS_COMBINED_CAP - provident_fund_deduction,
    )
    insurance_and_savings = (
        social_security_deduction
        + life_insurance_deduction
        + health_insurance_deduction
        + provident_fund_deduction
        + rmf_deduction
    )
    mortgage_deduction = min(
        _non_negative_amount(mortgage_interest, "Mortgage interest"),
        MORTGAGE_INTEREST_CAP,
    )

    total_deductions = (
        standard_expense
        + family_allowances
        + insurance_and_savings
        + mortgage_deduction
    )
    net_before_donations = max(0.0, total_income - total_deductions)
    donation_deduction = min(
        _non_negative_amount(donations, "Donations"),
        net_before_donations * DONATION_RATE_CAP,
    )
    final_net_income = max(0.0, net_before_donations - donation_deduction)

    return TaxCalculation(
        total_income=total_income,
        standard_expense_deduction=standard_expense,
        personal_and_family_allowances=family_allowances,
        insurance_and_savings_deductions=insurance_and_savings,
        mortgage_interest_deduction=mortgage_deduction,
        total_allowances_and_deductions=total_deductions,
        donation_deduction=donation_deduction,
        net_income_before_donations=net_before_donations,
        final_net_income=final_net_income,
        tax_payable=calculate_progressive_tax(final_net_income),
    )


def calculate_tax(income: float, deductions: float) -> tuple[float, float]:
    """Backward-compatible aggregate calculation used by the original tests.

    ``deductions`` is treated as one aggregate deduction with the project's
    original strict 100,000 THB cap.
    """
    total_income = _non_negative_amount(income, "Income")
    deductions = min(_non_negative_amount(deductions, "Deductions"), 100_000.0)
    net_income = max(0.0, total_income - deductions)
    return net_income, calculate_progressive_tax(net_income)


def _ask_amount(prompt: str) -> float:
    while True:
        try:
            amount = float(input(prompt))
            if amount < 0:
                raise ValueError
            return amount
        except ValueError:
            print("Please enter a non-negative number.")


def _ask_count(prompt: str) -> int:
    while True:
        try:
            count = int(input(prompt))
            if count < 0:
                raise ValueError
            return count
        except ValueError:
            print("Please enter a non-negative whole number.")


def _ask_yes_no(prompt: str) -> bool:
    while True:
        answer = input(prompt).strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please enter y or n.")


def _format_baht(amount: float) -> str:
    return f"{amount:,.2f} THB"


def run_cli() -> None:
    """Collect calculator inputs and print an itemized tax summary."""
    print("\n=== Thai Personal Income Tax Calculator ===")
    print("Enter annual amounts in Thai baht.\n")
    result = calculate_tax_details(
        income=_ask_amount("Total employment income (salary): "),
        spouse_no_income=_ask_yes_no("Do you have a spouse with no income? (y/n): "),
        children=_ask_count("Number of children: "),
        qualified_parents=_ask_count(
            "Number of qualified parents (over 60, low income) supported: "
        ),
        social_security=_ask_amount("Social Security contributions: "),
        life_insurance=_ask_amount("Life Insurance premiums: "),
        health_insurance=_ask_amount("Health Insurance for yourself: "),
        provident_fund=_ask_amount("Provident Fund contributions: "),
        rmf=_ask_amount("RMF contributions: "),
        mortgage_interest=_ask_amount("Home Mortgage Interest paid: "),
        donations=_ask_amount("General charitable donations: "),
    )

    print("\n=== Tax Calculation Summary ===")
    print(f"Total Income:                         {_format_baht(result.total_income)}")
    print(
        "Standard Expense Deduction:           "
        f"{_format_baht(result.standard_expense_deduction)}"
    )
    print(
        "Personal & Family Allowances:         "
        f"{_format_baht(result.personal_and_family_allowances)}"
    )
    print(
        "Insurance, Savings & Social Security: "
        f"{_format_baht(result.insurance_and_savings_deductions)}"
    )
    print(
        "Mortgage Interest Deduction:          "
        f"{_format_baht(result.mortgage_interest_deduction)}"
    )
    print(
        "Total Allowances & Deductions:        "
        f"{_format_baht(result.total_allowances_and_deductions)}"
    )
    print(f"Donation Deduction (10% cap):          {_format_baht(result.donation_deduction)}")
    print(f"Final Net Income:                      {_format_baht(result.final_net_income)}")
    print(f"Total Tax Payable:                     {_format_baht(result.tax_payable)}")


if __name__ == "__main__":
    run_cli()
