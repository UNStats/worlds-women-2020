import os
import utils
import time
import json
import math
import string

# ----------------------------------------------
# This script reads the json file with the merged
# data ("02_AllData.json") and the Data Structure
# Definition ("DSD.txt"), and creates a unified
# tabular view of all the data records.
# -----------------------------------------------

# Read the "ragged" data


data = utils.open_json('data/02_AllData.json')
print(data[0])

# Read the DSD

dsd = utils.tsv2dictlist('data/source/DSD.txt')
print(dsd[0])

# For each record, create a new "merged" record in csv format
merged_data = []

for record in data:

    new_record = dict()

    for item in dsd:

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

    merged_data.append(new_record)

utils.dictList2tsv(merged_data, 'data/03_MergedData.txt')
