def calculate_tax(income, deductions):
    # Step 1: Cap deductions at exactly 100,000
    capped_deductions = min(deductions, 100000)

    # Step 2: Calculate net income
    net_income = income - capped_deductions

    # Step 3: Calculate progressive tax
    tax = 0
    if net_income > 300000:
        tax += (net_income - 300000) * 0.10
        net_income = 300000
    if net_income > 150000:
        tax += (net_income - 150000) * 0.05

    return tax