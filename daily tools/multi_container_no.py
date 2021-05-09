from loguru import logger
from collections import defaultdict
import pandas as pd


class MultiContainer:
    def __init__(self, data: list):
        self.data = data
        self.final_data = []
        self.temp_data = defaultdict(list)

    def analyze_data(self):
        for each_row in self.data:
            if len(each_row) < 2:
                logger.info('该行长度小于2, 无法提取其中的箱号,将忽略此行')
                continue
            container_no = each_row[1]
            self.temp_data[container_no].append(each_row)

    def digest_each_row(self):
        for each_row in self.temp_data.values():
            self.final_data.append(each_row)

    def analyze_data_by_pandas(self):
        data_df = pd.DataFrame(self.data)
        after_data_df = data_df.groupby(1)
        for each_group, index in after_data_df.indices.items():
            print(data_df.loc[index])  # .to_csv(f'{each_group}.csv')
            # data_df.loc[index].to_csv(f'{each_group}.csv')
            data_df.loc[index].to_excel(f'{each_group}.xlsx')
            # print(each_group)
            # each_group.to_csv()

    def main(self):
        # self.analyze_data()
        # self.digest_each_row()
        self.analyze_data_by_pandas()
        pass


if __name__ == '__main__':
    """输出结果如何不用查看column_index, row_index"""

    list1 = [
        ['CNCC274831', 'TRHU4470059', None, None, '1X40HQ', '8201500090', 'TOOLS(Pruning Shear)', 923, 'CARTON',
         17154.2, 68.339, 'INGCO', None, None],
        ['CNCC274831P1', 'CMAU5983344', None, None, '1X40HQ', '8203200000', 'TOOLS(End cutting pliers)', 1180, 'CARTON',
         21561, 68.434, 'INGCO', None, None],
        ['CNCC274831P2', 'SEGU5387191', None, None, '1X40HQ', '8204110000',
         'TOOLS(7PCS insulated open end spanners set)', 953, 'CARTON', 16856.7, 68.237, 'INGCO', None, None],
        ['CNCC274831P3', 'TCNU3218413', None, 'P9336981', '1X40HQ', '8201600090', 'TOOLS(Hedge shear)', 1203, 'CARTON',
         18116.8, 68.61, 'INGCO', None, None],
        ['CNCC274831P4', 'TRHU4470059', None, 'P9336819', '1X40HQ', '8202100000', 'TOOLS(Hand saw)', 1169, 'CARTON',
         21361.41, 68.497, 'INGCO', None, None],
        ['CNCC274831P5', 'CMAU5983344', None, 'P9336887', '1X40HQ', '8205400000', 'TOOLS(6 pcs screwdriver set)', 818,
         'CARTON', 15474, 68.566, 'INGCO', None, None],
        ['CNCC274831P6', 'CMAU4432326', None, 'P9336879', '1X40HQ', '8202100000', 'TOOLS(MiNi Hand Frame)', 1946,
         'CARTON', 23300, 68.533, 'INGCO', None, None],
        ['CNCC274831P7', 'SEGU5387191', None, 'P9336885', '1X40HQ', '8201500090', 'TOOLS(Pruning Shear)', 1138,
         'CARTON', 19400.65, 68.485, 'INGCO', None, None],
        ['CNCC274831P8', 'CMAU4432326', None, None, '1X40HQ', '8205200000', 'TOOLS(Machinist hammer)', '1079', 'CARTON',
         25077.5, 68.542, 'INGCO', None, None],
        ['CNCC274831P9', 'GESU5936492', None, 'P9336884', '1X40HQ', '8205590000', 'TOOLS(Tile cutter)', 913, 'CARTON',
         13539.7, 68.551, 'INGCO', None, None]
    ]
    mc = MultiContainer(list1)
    mc.main()
