import os
import utils
import time
import json
import math
import string

# ----------------------------------------------
#   This script reads the unified tabular view
# of all data records and creates tables for
# validation of code lists.
#   In the case of SERIES, there
# are no codes yet, so this will help create
# series codes.
# -----------------------------------------------

# Read the merged data
data = utils.tsv2dictlist('data/03_MergedData.txt')
print(data[0])

# Read the DSD

dsd = utils.tsv2dictlist('data/source/DSD.txt')
print(dsd[0])

# extract coded concepts from DSD:

coded_concepts = utils.subdict_list(utils.select_dict(dsd, {'Coded': 'Yes'}), [
                                    'Concept', 'Description'])

print(coded_concepts)

for i in coded_concepts:

    keys = [i['Concept']]
    if len(i['Description']) > 0:
        keys.append(i['Description'])

    codeListName = 'CL_' + i['Concept']

    codeList = utils.unique_dicts(utils.subdict_list(data, keys))

    codeList = utils.select_dict(codeList, {i['Concept']: ''}, keep=False)

    utils.dictList2csv(codeList, 'data/clean/code_lists/' +
                       codeListName + '.csv')
