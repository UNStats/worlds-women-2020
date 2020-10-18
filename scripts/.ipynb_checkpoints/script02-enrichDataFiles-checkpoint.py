
import os
import utils
import csv
import pandas as pd
from operator import itemgetter

# Read DSD
dsd = utils.tsv2dictlist('data/external/DSD.txt')

# Read series metadata:
s_meta = utils.open_json('data/external/seriesMetadata.json')

data_files = os.listdir('data/processed/series/')


for s in s_meta:
    print(f'Processing series {s["code"]}')

    for file in data_files:

        if file.endswith(s['code'] + '.csv'):

            data = []

            with open('data/processed/series/' + file, mode="r", encoding="utf-8-sig") as f:
                for line in csv.DictReader(f):
                    data.append(dict(line))

            # print(data[0])

            new_data = []

            sort_keys = []

            for i in data:

                record = dict()

                for j in dsd:

                    #print(f"--- {j['Concept']}")

                    if j['Mandatory'] == 'Yes':

                        sort_keys.append(j['Concept'])

                        if j['Concept'] in i.keys():
                            if i[j['Concept']] != 'nan':
                                record[j['Concept']] = i[j['Concept']]
                            else:
                                record[j['Concept']] = None
                        else:
                            record[j['Concept']] = None

                        if j['HasCodeList'] == 'Yes':
                            if j['Description'] in i.keys():

                                if i[j['Description']] != 'nan':
                                    record[j['Description']
                                           ] = i[j['Description']]
                                else:
                                    record[j['Description']] = None
                            else:
                                record[j['Description']] = None

                    else:

                        if j['Concept'] in i.keys():

                            sort_keys.append(j['Concept'])

                            if i[j['Concept']] != 'nan':
                                record[j['Concept']] = i[j['Concept']]
                            else:
                                record[j['Concept']] = None

                            if j['HasCodeList'] == 'Yes':
                                if j['Description'] in i.keys():
                                    if i[j['Description']] != 'nan':
                                        record[j['Description']
                                               ] = i[j['Description']]
                                    else:
                                        record[j['Description']] = None
                                else:
                                    record[j['Description']] = None

                new_data.append(record)

    # print(new_data)

    x = sorted(new_data, key=lambda i: (i['REF_AREA'], i['TIME_PERIOD']))

    # x = sorted(new_data, key=itemgetter(sort_keys))
    # utils.dictList2tsv(x, 'data/processed/series/' + s['code'] + '.txt')

    pd.DataFrame.from_dict(x).to_excel(
        'data/processed/series/' + s['code'] + '.xlsx', index=False)

    print(f'-----finished one {s["code"]}')
