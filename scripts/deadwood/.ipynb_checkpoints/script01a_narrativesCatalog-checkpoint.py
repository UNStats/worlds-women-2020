import os
import utils
import time

# -----------------------------------
# Read all excel files in narratives
# -----------------------------------


path = "../../../United Nations/Francesca Grum - WW2020/__Hub/NarrativeAndData"
timestr = time.strftime("%Y%m%d-%H%M%S")


data_files = []

for root, dirs, files in os.walk(path):
    if len(files) > 0:
        for f in files:

            if f.endswith('xlsx'):
                d = dict()

                d['path'] = root.replace("\\", "/")
                d['filename'] = f
                x = f.split('_')
                d['narrative_id'] = x.pop(0)
                d['narrative_desc'] = '_'.join(x).split('.')[0]
                d['theme_id'] = d['narrative_id'][0:2]

                data_files.append(d)

# Write narratives catalogue
utils.dictList2tsv(data_files, 'data/01_Data Catalog.txt')


data_files = []

for root, dirs, files in os.walk(path):
    if len(files) > 0:
        for f in files:

            if f.endswith('docx'):
                d = dict()

                d['path'] = root.replace("\\", "/")
                d['filename'] = f
                x = f.split('_')
                d['narrative_id'] = x.pop(0)
                d['narrative_desc'] = '_'.join(x).split('.')[0]
                d['theme_id'] = d['narrative_id'][0:2]

                data_files.append(d)

# Write narratives catalogue
utils.dictList2tsv(data_files, 'data/01_Narratives Catalog.txt')
