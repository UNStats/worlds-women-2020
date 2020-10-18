import utils
import json

# Read data catalog
dataCat = utils.tsv2dictlist('data/external/dataCatalog.txt')
print(dataCat[0])

# Read themes:
themesCat = utils.tsv2dictlist('data/external/themes.txt')

# Read subthemes:
subthemesCat = utils.tsv2dictlist('data/external/subthemes.txt')

# -------------------------------------------------------------
# Create JSON file with series metadata
# --------------------------------------------------------------

sMetadata = []

for s in dataCat:

    themes = s['Theme_id'].replace("'", "").strip("][").split(", ")

    subthemes = s['Subtheme_id'].replace("'", "").strip("][").split(", ")

    narratives = s['Narrative_id'].replace("'", "").strip("][").split(", ")

    tags = s['Tags'].split(", ")

    d = dict()
    d['code'] = s['Series']
    d['name'] = s['Series_Desc']
    d['themes'] = []

    for t in themes:

        for tt in themesCat:
            if t != tt['Theme_Code']:
                continue
            d_theme = dict()
            d_theme['code'] = t
            d_theme['name'] = tt['Theme_Desc']

            d_theme['subthemes'] = []

            for st in subthemes:

                for sstt in subthemesCat:

                    if st != sstt['Subtheme_Code']:
                        continue

                    d_subtheme = dict()
                    d_subtheme['code'] = st
                    d_subtheme['name'] = sstt['Subtheme_Desc']

                    d_theme['subthemes'].append(d_subtheme)

            d['themes'].append(d_theme)

    d['narratives'] = narratives
    d['tags'] = tags

    sMetadata.append(d)

# Write narratives catalogue
with open("data/external/seriesMetadata.json", "w") as write_file:
    json.dump(sMetadata, write_file, indent=4)
