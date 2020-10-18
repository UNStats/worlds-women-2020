import os
import utils
import time
import json
import math
import string

# ----------------------------------------------
# This script reads the json file with the merged
# data ("02_AllData.json") and the Data Structure
# Definition ("DSD.txt"), and creates one individual
# tab-delimited file for each series
# -----------------------------------------------

# Read the "ragged" data


data = utils.open_json('data/02_AllData.json')
print(data[0])

# Read the DSD

dsd = utils.tsv2dictlist('data/source/DSD.txt')
print(dsd[0])

# Read the geo tree

geo = utils.tsv2dictlist('data/source/geo_tree.txt')
print(geo[0])

# Read the series catalog

series_catalog = utils.tsv2dictlist('data/source/SeriesCatalog.txt')
print(series_catalog[0])

# Compulsory keys:
compulsory_keys = ['THEME_ID',
                   'NARRATIVE_ID',
                   'NARRATIVE_DESC',
                   'SERIES',
                   'FREQ',
                   'REPORTING_TYPE',
                   'TIME_PERIOD',
                   'REF_AREA',
                   'OBS_VALUE',
                   'UNIT_MEASURE',
                   'UNIT_MULT',
                   'NATURE',
                   'GEOLEVEL',
                   'SOURCE_DETAIL'
                   ]

# Loop through the series catalog:

series_not_found = []

empty_col_report = []

missing_vals_report = []

for s in series_catalog:

    series = s['SERIES']

    # if series != 'S_0160':
    #     continue

    print(f"----------series is {series}---------")

    # Extract the data pertatining to this series:

    data_s = utils.select_dict(data, {'SERIES': series})

    if len(data_s) == 0:
        series_not_found.append(series)
        continue

    # obtain the list of keys across all records in data_s:

    keys = []
    for i in data_s:
        keys.extend(list(i.keys()))
        keys = list(set(keys))

    # For each record, create a new "merged" record in csv format:
    series_data = []

    for record in data_s:

        new_record = dict()

        geo_record = utils.select_dict(
            geo, {'geoAreaCode': record['REF_AREA']})

        if len(geo_record) > 0:
            new_record['X'] = geo_record[0]['X']
            new_record['Y'] = geo_record[0]['Y']
        else:
            new_record['X'] = None
            new_record['Y'] = None

        for item in dsd:
            if item['Concept'] in keys:
                concept = item['Concept']
                role = item['Role']

                if len(item['Description']) > 0:
                    desc = item['Description']
                else:
                    desc = None

                if concept in record.keys():
                    new_record[concept] = record[concept]
                else:
                    new_record[concept] = None

                if desc:
                    if desc in record.keys():
                        new_record[desc] = record[desc]
                    else:
                        new_record[desc] = None

        series_data.append(new_record)

    # Remove empty columns:
    empty_keys = utils.empty_dictlist_variables(series_data)

    remove_keys = [i for i in empty_keys if i not in compulsory_keys]

    empty_compulsory = [i for i in empty_keys if i in compulsory_keys]

    empty_col_report.append({'series': series, 'empty_cols': empty_compulsory})

    #print(f'Series {series} has empty columns: {empty_compulsory}')

    series_data = utils.subdict_list(series_data, remove_keys, exclude=True)

    keys_missing_values = utils.dictlist_missing_values(
        series_data, ['OBS_VALUE', 'UNIT_MEASURE', 'FREQ', 'TIME_PERIOD', 'REF_AREA'])

    missing_vals_report.append(
        {'series': series, 'missing_vals': keys_missing_values})

    utils.dictList2csv(series_data, 'data/clean/series/' +
                       s['THEME_ID'] + '__' + s['INDICATOR_CODE'] + '__' + series + '.csv')

print(series_not_found)

utils.dictList2csv(empty_col_report, 'data/empty_columns_report.csv')
utils.dictList2csv(missing_vals_report, 'data/missing_values_report.csv')
