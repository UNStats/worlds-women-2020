import os
import utils


# Get data files
data_dir = 'data/processed/series'
data_files = [f for f in os.listdir(data_dir) if f.endswith("xlsx")]

print(data_files)

for f in data_files:

    xlsx_dataset = 'data/processed/series/' + f
    print(f'----passed {f} ----')
    data_dict = utils.xlsx2dict(xlsx_dataset, 'Sheet1')

    utils.dictList2tsv(data_dict, 'data/processed/series_csv/' +
                       f.replace('xlsx', 'csv'))
