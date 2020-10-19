import json
import utils
import utils_arcgis
from bs4 import BeautifulSoup
from copy import copy

narrative_metadata = utils.tsv2dictlist(
    'narratives/story-map-data/_narrative_cat.txt')

online_username, gis_online_connection = utils_arcgis.connect_to_arcGIS()

print(online_username)
print(gis_online_connection)

base_url = 'https://worlds-women-2020-data-undesa.hub.arcgis.com/app/'


galleries = ['3c36e1a9aedb43f3b6db137c406ab35c',
             '42a7b42eb34243038b37f2ab8157470d',
             'bb045390cd8e43b6b49dd166276f5ac9',
             'db4d332e5d244548b7e5a82d20188f44',
             '28f0187465b440e48cc62bf38f86018f',
             '87884331961542daa8e19696f7bac96b',
             '2501891d28164237b903c1a5ff31621f']


user = gis_online_connection.users.get('unstats_admin')

user_items = user.items(folder='World\'s Women 2020 Narratives', max_items=800)


with open('narratives/_templates/style_plain.txt', 'r') as file:
    new_style = file.read()

#print(f"new_style = {new_style}")

for item in user_items:

    if item["id"] in galleries:
        continue

    for m in narrative_metadata:
        if m['id'] == item['id']:
            narrative_id = m['narrative_id']
            continue

    if item["id"] == '0d1ff2530f17451bb8437c6ea584282e':
        continue

    # Get metadata for current item

    json_data = item.get_data()

    first_section = json_data['values']['story']['sections'][0]['content']

    soup = BeautifulSoup(first_section, "html.parser")

    style = soup.style

    print(f"Original style:\n {style}")

    style.string = new_style

    print(soup)

    json_data['values']['story']['sections'][0]['content'] = str(soup)

    item.update(data=json_data)

    json_data = item.get_data()

    with open('narratives/story-map-data/'+narrative_id+'.json', 'w') as fout:
        json.dump(json_data, fout, indent=4)
