import os
import utils
import time
import csv

# -----------------------------------
# Read all excel files in narratives
# -----------------------------------


path = "../../../United Nations/Francesca Grum - WW2020/__Hub/Data/CleanData_Revision1/Series"
timestr = time.strftime("%Y%m%d-%H%M%S")

old_data_files = []
new_data_files = []

for root, dirs, files in os.walk(path):
    if len(files) > 0:
        for f in files:

            if f.endswith('xlsx'):
                d = dict()

                d['path'] = root.replace("\\", "/")
                d['filename'] = f
                x = f.split('__')
                d['theme_id'] = x.pop(0)
                d['indicator_id'] = x.pop(0)
                x = x[0].split('.')
                d['series_id'] = x.pop(0)
                d['type'] = x[0]

                new_data_files.append(d)

            if f.endswith('csv'):
                d = dict()

                d['path'] = root.replace("\\", "/")
                d['filename'] = f
                x = f.split('__')
                d['theme_id'] = x.pop(0)
                d['indicator_id'] = x.pop(0)
                x = x[0].split('.')
                d['series_id'] = x.pop(0)
                d['type'] = x[0]

                old_data_files.append(d)


# Write narratives catalogue
utils.dictList2tsv(old_data_files, 'data/Revision1_old.txt')
utils.dictList2tsv(new_data_files, 'data/Revision1_new.txt')

ref_areas = []
with open('data/clean/code_lists/CL_REF_AREA.csv', mode="r", encoding="utf-8-sig") as f:
    for line in csv.DictReader(f):
        ref_areas.append(dict(line))

for g in ref_areas:
    g['REF_AREA_DESC'] = g['REF_AREA_DESC'].strip(u'\u200b')

for new in new_data_files:
    old = utils.select_dict(
        old_data_files, {'series_id': new['series_id']}, keep=True)[0]

    new_d = utils.xlsx2dict(
        new['path'] + '/' + new['filename'], new['filename'].replace('.xlsx', ''))

    for i in new_d:
        for j in ref_areas:
            if j['REF_AREA'] == i['REF_AREA']:
                i['REF_AREA_DESC'] = j['REF_AREA_DESC']

    filename = 'data/clean/series/' + \
        new['theme_id'] + '__' + new['indicator_id'] + \
        '__' + new['series_id'] + '.csv'

    utils.dictList2csv(new_d, filename)


for file in os.listdir('data/clean/series/'):
    x = []
    with open('data/clean/series/' + file, mode="r", encoding="utf-8-sig") as f:
        for line in csv.DictReader(f):
            x.append(dict(line))

    for i in x:
        i['FREQ'] = 'A'

    utils.dictList2csv(x, 'data/clean/series/' + file)
