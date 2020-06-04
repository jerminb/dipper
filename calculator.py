import pandas as pd
from util import househouldPersonCalculator
from excel_utils import ExcelReader, ExcelProperyMapper

_person_ratio = 0.8

class StatsCalculator():
    mapper = {}
    file_reader = None

    def __init__(self, file):
        self.file_reader = ExcelReader(file)
        self.mapper['income_stats'] = ExcelProperyMapper().initialize_with("income_stats")
        self.mapper['age_stats'] = ExcelProperyMapper().initialize_with("age_stats")

    def get_range_column(self, val, stats_type):
        valrange=self.file_reader.read_excel(self.mapper[stats_type]['sheet_name'], self.mapper[stats_type]['range_cols'], self.mapper[stats_type]['range_skiprows'], None, 1)
        colindex=valrange.iloc[0].searchsorted(val)
        return valrange.columns[colindex-1]

    def get_entity(self, range_column, stats_type):
        return self.file_reader.read_excel(self.mapper[stats_type]['sheet_name'], [1, range_column], self.mapper[stats_type]['entity_skiprows'], None, self.mapper[stats_type]['entity_nrows'], index_col=self.mapper[stats_type]['entity_index_col']).dropna()

    def get_personperhousehold(self, range_column, stats_type):
        return self.file_reader.read_excel(self.mapper[stats_type]['sheet_name'], [range_column], self.mapper[stats_type]['personperhousehold_skiprows'], None, 1)

    def calc_raw_vals(self, val, stats_type):
        entity_col = self.get_range_column(val, stats_type)
        entity = self.get_entity(entity_col, stats_type)
        pphd = self.get_personperhousehold(entity_col, stats_type)
        hhr = househouldPersonCalculator(pphd.iloc[0,0])
        return entity.iloc[:].mul(_person_ratio/hhr)

    def calc_stats(self, type_map):
        dfs = []
        for key in type_map:
            dfs.append(self.calc_raw_vals(type_map[key], key))
        rawdf=pd.concat(dfs, axis=1)
        rawdf['mean'] = rawdf.mean(axis=1)
        rawdf['std'] = rawdf.std(axis=1)
        return rawdf
