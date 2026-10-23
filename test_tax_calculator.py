import unittest
from tax_calculator import calculate_tax_details

class TestTaxCalculator(unittest.TestCase):
    def test_normal_case(self):
        # Only income, standard expense triggers, personal allowance triggers
        result = calculate_tax_details(income=300000.0)
        
        # Standard expense: 100k (capped). Personal: 60k. Total deductions: 160k. Net: 140k. Tax: 0.
        self.assertEqual(result.final_net_income, 140000.0)
        self.assertEqual(result.tax_payable, 0.0)

    def test_boundary_case(self):
        # Health + Life Insurance boundary (cap at 100k)
        result = calculate_tax_details(
            income=500000.0, 
            health_insurance=25000.0, 
            life_insurance=90000.0
        )
        
        # Standard expense: 100k. Personal: 60k. Insurance (capped): 100k. 
        # Total deductions: 260k. Net: 240k. 
        # Tax: first 150k is 0, remaining 90k at 5% = 4,500
        self.assertEqual(result.final_net_income, 240000.0)
        self.assertEqual(result.tax_payable, 4500.0)

if __name__ == '__main__':
    unittest.main()