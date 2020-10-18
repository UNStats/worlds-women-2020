import os
import utils
import time
import csv

# -----------------------------------
# Read all excel files in narratives
# -----------------------------------


path = "data/clean/series/"

series_catalog = []

for file in os.listdir(path):

    data = []
    with open('data/clean/series/' + file, mode="r", encoding="utf-8-sig") as f:
        for line in csv.DictReader(f):
            data.append(dict(line))

    narratives = utils.dictItem2List(
        data, 'NARRATIVE_ID', unique=True, sort_list=True)

    d = dict()

    d['filename'] = f.name
    d['Theme_Code2'] = data[0]['THEME_ID']
    d['Narrative_id'] = narratives
    d['Series'] = data[0]['SERIES']
    d['Series_desc'] = data[0]['SERIES_DESC']

    series_catalog.append(d)

# Write series catalogue
utils.dictList2tsv(series_catalog, 'data/clean/series_catalog.txt')
