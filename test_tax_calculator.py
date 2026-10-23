import unittest
from tax_calculator import calculate_tax

class TestTaxCalculator(unittest.TestCase):
    def test_normal_case(self):
        # C1: Income 250,000, Deduction 0 -> Net 250k, Tax 5,000
        net, tax = calculate_tax(250000, 0)
        self.assertEqual(net, 250000)
        self.assertEqual(tax, 5000)

    def test_boundary_case(self):
        # C2: Income 500,000, Deduction 150,000 -> Capped deduction 100k
        # Net 400k. Tax = (150k * 5%) + (100k * 10%) = 7,500 + 10,000 = 17,500
        net, tax = calculate_tax(500000, 150000)
        self.assertEqual(net, 400000)
        self.assertEqual(tax, 17500)

if __name__ == '__main__':
    unittest.main()