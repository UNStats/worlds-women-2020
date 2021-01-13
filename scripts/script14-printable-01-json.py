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

#================================

online_username, gis_online_connection = utils_arcgis.connect_to_arcGIS()

print(online_username)
print(gis_online_connection)

user = gis_online_connection.users.get('unstats_admin')

user_items = user.items(folder='World\'s Women 2020 Narratives', max_items=800)

for item in user_items:

    d = dict()

    d['title'] = item["title"]
    d['description'] = item["description"]
    d['id'] = item["id"]
    d['url'] = item["url"]
    d['tags'] = item["tags"]

    #print(f'dictionary: {d}')
    
    
    #----------------------------------

    json_data = item.get_data()

    print(item['title'])
    with open('pdf/'+item['id']+'.json', 'w') as fout:
        json.dump(json_data, fout, indent=4)
