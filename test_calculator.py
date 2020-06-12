from calculator import StatsCalculator
import unittest

class TestStatsCalculator(unittest.TestCase):
    income_mid = 239
    income_low = 219
    income_high = 1752
    age_low = 29
    stats_calc = StatsCalculator("./test-fixtures/familyspendingworkbook2expenditurebyincome.xlsx")
    def testWithWrongStatsType(self):
        self.assertRaises(KeyError, self.stats_calc.calc_raw_vals, self.income_low, "foo")

    def testIncomeGetRante(self):
        self.assertEqual(self.stats_calc.get_range_column(self.income_mid, "income_stats"), 5)

    def testIncomeGetEntity(self):
        col = self.stats_calc.get_range_column(self.income_mid, "income_stats")
        self.assertEqual(self.stats_calc.get_entity(col, "income_stats").size, 14)
        self.assertEqual(self.stats_calc.get_entity(col, "income_stats").index.size, 14)

    def testIncomePersonperhousehold(self):
        col = self.stats_calc.get_range_column(self.income_mid, "income_stats")
        res = self.stats_calc.get_personperhousehold(col, "income_stats")
        self.assertEqual(res.size, 1)
        self.assertEqual(res.iloc[0,0], 1.6)

    def testIncomeCalcStats(self):
        res = self.stats_calc.calc_raw_vals(self.income_mid, "income_stats")
        self.assertEqual(res.size, 14)

    def testIncomeLowerBoundary(self):
        res = self.stats_calc.calc_raw_vals(self.income_low, "income_stats")
        self.assertEqual(res.size, 14)
        self.assertLessEqual(res.iloc[0,0], 32.8)

    def testIncomeHigherBoundary(self):
        res = self.stats_calc.calc_raw_vals(self.income_low, "income_stats")
        self.assertEqual(res.size, 14)
        self.assertLessEqual(res.iloc[2,0], 53.5)

    def testAgeLowerBoundary(self):
        res = self.stats_calc.calc_raw_vals(self.age_low, "age_stats")
        self.assertEqual(res.size, 14)
        self.assertLessEqual(res.iloc[0,0], 44.9)

    def testCalcStats(self):
        res = self.stats_calc.calc_stats({"income_stats": self.income_mid, "age_stats":self.age_low})
        self.assertEqual(res['mean'].size, 14)
        self.assertEqual(res['std'].size, 14)

if __name__ == '__main__':
    unittest.main()
