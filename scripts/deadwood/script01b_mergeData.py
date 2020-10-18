import os
import utils
import time
import json
import math
import string

# ----------------------------------------------
# This script picks the main "Data" table from each
# narrative, and merges them into a single json file
# ("02_AllData.json")
# -----------------------------------------------


all_data = []
no_data = []

cols = ['THEME_ID', 'NARRATIVE_ID', 'NARRATIVE_DESC']
print(cols)

data_catalogue = utils.tsv2dictlist('data/01_Data Catalog.txt')

for dataset in data_catalogue:

    # if dataset['narrative_id'] not in ['NP20', 'NE10']:
    #     continue

    print(f"processing file {dataset['filename']}")

    try:
        data = utils.xlsx2dict(
            dataset['path'] + '/' + dataset['filename'], 'Data')

    except:
        print(
            f"Failed opening data worksheet in {dataset['path'] + '/' +dataset['filename']}")
        no_data.append(dataset['narrative_id'])
        continue

    else:
        print(f"Success opening data worksheet in {dataset['filename']}")

        # Make column names uppercase:

        for i in range(len(data)):

            new_record = dict()

            new_record['THEME_ID'] = dataset['theme_id']
            new_record['NARRATIVE_ID'] = dataset['narrative_id']
            new_record['NARRATIVE_DESC'] = dataset['narrative_desc']

            for k in data[i].keys():
                new_key = k.upper().replace(' ', '')
                if data[i][k] == 'nan':
                    new_record[k.upper()] = None
                else:
                    new_record[new_key] = data[i][k]

                if new_key in ['AFGHANISTAN', 'OBSSERVATIONVALUE', 'WORLD']:
                    print(f"Check column titles for {dataset['narrative_id']}")
                    break

            if i == 0:

                # print(cols)
                # print(list(data[i].keys()))

                cols.extend(list(new_record.keys()))
                cols = list(set(cols))

                check = True in (item.startswith(
                    'VIOLENC_') for item in cols)

                if check is True:
                    print(
                        f"********************Check {dataset['narrative_id']}")
                    break

                # print(cols)

                # print('-------')

            all_data.append(new_record)


cols.sort()

print(no_data)
print(cols)

# Write narratives catalogue
with open("data/02_AllData.json", "w") as write_file:
    json.dump(all_data, write_file, indent=4)
