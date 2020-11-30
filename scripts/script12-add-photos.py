
import os
import utils
import csv
import json
import copy
import re 

from bs4 import BeautifulSoup

import utils
import utils_arcgis
from datetime import datetime, timezone


# Read main photos as dict

# Read themes:
photos = utils.tsv2dictlist('data/external/main_photos-3rd-batch.txt')

print(photos)

photo_metadata_url = "https://unstats.un.org/unsd/demographic-social/gender/worldswomen/2020/img/alissa-de-leva-unsplash.jpg"
photo_metadata_name = "alissa-de-leva-unsplash.jpg"

photo_footnote_url = "https://unstats.un.org/unsd/demographic-social/gender/worldswomen/2020/img/lindsay-henwood-unsplash.jpg"
photo_footnote_name = "lindsay-henwood-unsplash.jpg"

#================================

online_username, gis_online_connection = utils_arcgis.connect_to_arcGIS()

print(online_username)
print(gis_online_connection)

user = gis_online_connection.users.get('unstats_admin')

user_items = user.items(folder='ww2020 - Narratives3', max_items=800)

for item in user_items:

    #print(item["id"])


    d = dict()

    d['narrative_id'] = item["title"][:item["title"].find(' ')]
    d['title'] = item["title"][item["title"].find('-')+2::]
    d['id'] = item["id"]
    d['url'] = item["url"]
    d['tags'] = item["tags"]
    d['tags'].append(d['narrative_id'])
    d['description'] = item["description"]

    photo_url = ''
    photo_name = ''
    
    for p in photos:

        if p['NarrativeID'] == d['narrative_id']:
            photo_url = p['URL']
            photo_name = p['Photo']
            continue
    
    
    print(photo_url)
    print(photo_name)
    
    #----------------------------------

    json_data = item.get_data()

    
    with open('control/'+d['narrative_id']+'_before.json', 'w') as fout:
        json.dump(json_data, fout, indent=4)

    json_data["annotations_unsd"] = {"narrative_id": d['narrative_id']}

    n = len(json_data['values']['story']['sections'])
    print(f'Narrative {d["narrative_id"]} has {n} sections')

    json_data['values']['story']['sections'][0]['media']['image']['url'] = photo_url
    json_data['values']['story']['sections'][0]['media']['image']['sizes'][0]['name'] = photo_name
    json_data['values']['story']['sections'][0]['media']['image']['sizes'][0]['url'] = photo_url

    print(json_data['values']['story']['sections'][0]['media'])
    print('------------------')

    json_data['values']['story']['sections'][n-2]['media']['image']['url'] = photo_metadata_url
    json_data['values']['story']['sections'][n-2]['media']['image']['sizes'][0]['name'] = photo_metadata_url
    json_data['values']['story']['sections'][n-2]['media']['image']['sizes'][0]['url'] = photo_metadata_url

    print(json_data['values']['story']['sections'][n-2]['media'])
    print('------------------')
    
    json_data['values']['story']['sections'][n-1]['media']['image']['url'] = photo_footnote_url
    json_data['values']['story']['sections'][n-1]['media']['image']['sizes'][0]['name'] = photo_footnote_name
    json_data['values']['story']['sections'][n-1]['media']['image']['sizes'][0]['url'] = photo_footnote_url

    print(json_data['values']['story']['sections'][n-2]['media'])
    print('******************************')

    item.update(data=json_data)

    json_data = item.get_data()

    with open('control/'+d['narrative_id']+'_after.json', 'w') as fout:
        json.dump(json_data, fout, indent=4)


