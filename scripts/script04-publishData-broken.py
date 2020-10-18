import utils
import sys
import os
from arcgis.gis import GIS
import copy
import requests
import json
import utils_arcgis_ww2020
import local_gis_connect

# ------------------------
# Set source data directory:
# ------------------------
data_dir = 'data/processed/series_csv/'
data_files = [f for f in os.listdir(data_dir) if f.endswith("csv")]

# ----------------------
# Get series metadata:
# ----------------------
series_metadata = utils.open_json(
    'data/external/seriesMetadata.json')

print('-----------------------------------------------')
print(series_metadata[0])

# ----------------------
# Set thumbnail link
# ----------------------

thumbnail = 'https://raw.githubusercontent.com/UNStats/worlds-women-2020/main/assets/photos/Thumbnails/WW2020.png'

# --------------------------
# Get layer info template
# --------------------------

layer_info = utils.open_json('data/external/layerinfo.json')

layer_info_properties = list(layer_info.keys())
print('-----------------------------------------------')
print(f'layer_info_properties={layer_info_properties}')

# # ------------------------------------
# # Establish ArcGIS online connection
# # -----------------------------------

# online_username, gis_online_connection = utils_arcgis_ww2020.connect_to_arcGIS()
online_username = ''
online_password = ''
online_connection = "https://www.arcgis.com"
gis_online_connection = GIS(online_connection,
                            online_username,
                            online_password)

print('-----------------------------------------------')
print(online_username)
print(gis_online_connection)

# ------------------------------------
# Publish data
# ------------------------------------

failed_series = []

for d in data_files:

    series = d.replace('.csv', '')

    if series != 'S_0320':
        continue

    s = None
    for m in series_metadata:
        if m['code'] == series:
            s = m
            continue

    print('------------------------------------------------------------')
    print(f's={s}')

    # csv file to be uploaded:
    file = os.path.join(data_dir + d)
    print('------------------------------------------------------------')
    print(f'file={file}')

    try:

        s_card = utils_arcgis_ww2020.build_series_card(s)

        print('------------------------------------------------------------')
        print(f's_card.keys={s_card.keys()}')

        utils_arcgis_ww2020.publish_csv(s,
                                        item_properties=s_card,
                                        thumbnail=thumbnail,
                                        layer_info=layer_info,
                                        gis_online_connection=gis_online_connection,
                                        online_username=online_username,
                                        file=file)

    except:
        print('Unexpected error:', sys.exc_info()[0])
        failed_series.append(s['code'])

print(f'failed series: {failed_series}')
