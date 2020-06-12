import pandas as pd

class ExcelReader():
    def __init__(self, filepath):
        self.xlsfile = pd.ExcelFile(filepath)

    def read_excel(self, sheet_name, cols, skiprows, header, nrows, index_col=None):
        return pd.read_excel(self.xlsfile, sheet_name=sheet_name, usecols=cols, skiprows=skiprows, header=header, nrows=nrows, index_col=index_col)


class ExcelProperyMapper(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v

    def _initialize_with_income_stats(self):
        self['range_cols'] = [4,5,6,7,8,9,10,11,12,13]
        self['range_skiprows'] = 9
        self['sheet_name'] = 'A4'
        self['entity_skiprows'] = 22
        self['entity_nrows'] = 30
        self['entity_index_col'] = 0
        self['personperhousehold_skiprows'] = 17
        return self

    def _initialize_with_age_stats(self):
        self['range_cols'] = [5,6,7,8]
        self['range_skiprows'] = 5
        self['sheet_name'] = 'A9'
        self['entity_skiprows'] = 21
        self['entity_nrows'] = 30
        self['entity_index_col'] = 0
        self['personperhousehold_skiprows'] = 15
        return self

    def initialize_with(self, stats_type):
        switcher = {
            "income_stats": self._initialize_with_income_stats,
            "age_stats": self._initialize_with_age_stats
        }
        return switcher[stats_type]()
