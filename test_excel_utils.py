from excel_utils import ExcelProperyMapper
import unittest

class TestExcelUtils(unittest.TestCase):
    def testInitExcelMapper(self):
        mapper = ExcelProperyMapper({"foo":"bar"})
        self.assertEqual(mapper["foo"], "bar")

    def testInitWithWrongStatsType(self):
        mapper = ExcelProperyMapper()
        self.assertRaises(KeyError, mapper.initialize_with, "foo")

    def testInitWithStateType(self):
        mapper = ExcelProperyMapper()
        self.assertEqual(mapper.initialize_with("income_stats").get('range_skiprows'), 9)
        self.assertEqual(mapper.initialize_with("age_stats").get('range_skiprows'), 5)
