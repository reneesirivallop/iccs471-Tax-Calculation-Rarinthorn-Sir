import unittest
from tax_calculator import calculate_thai_tax

class TestTaxCalculator(unittest.TestCase):
    def test_normal_case(self):
        # Only income, standard expense triggers, personal allowance triggers
        inputs = {'income': 300000}
        # Standard expense: 100k (capped). Personal: 60k. Total deductions: 160k. Net: 140k. Tax: 0.
        result = calculate_thai_tax(inputs)
        self.assertEqual(result['net_income'], 140000)
        self.assertEqual(result['tax'], 0)

    def test_boundary_case(self):
        # Health + Life Insurance boundary (cap at 100k)
        inputs = {
            'income': 500000, 
            'health_insurance': 25000, 
            'life_insurance': 90000 
        }
        # Standard expense: 100k. Personal: 60k. Insurance (capped): 100k. 
        # Total deductions: 260k. Net: 240k. 
        # Tax: first 150k is 0, remaining 90k at 5% = 4,500
        result = calculate_thai_tax(inputs)
        self.assertEqual(result['net_income'], 240000)
        self.assertEqual(result['tax'], 4500)

if __name__ == '__main__':
    unittest.main()