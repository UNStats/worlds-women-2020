import json
import utils
import utils_arcgis

narrative_metadata = utils.tsv2dictlist(
    'narratives/story-map-data/_narrative_cat.txt')

online_username, gis_online_connection = utils_arcgis.connect_to_arcGIS()

print(online_username)
print(gis_online_connection)


galleries = ['3c36e1a9aedb43f3b6db137c406ab35c',
             '42a7b42eb34243038b37f2ab8157470d',
             'bb045390cd8e43b6b49dd166276f5ac9',
             'db4d332e5d244548b7e5a82d20188f44',
             '28f0187465b440e48cc62bf38f86018f',
             '87884331961542daa8e19696f7bac96b',
             '2501891d28164237b903c1a5ff31621f']


user = gis_online_connection.users.get('unstats_admin')

user_items = user.items(folder='World\'s Women 2020 Narratives', max_items=800)

narrative_cat = []

for item in user_items:

    if item["id"] in galleries:
        continue

    # if item["id"] != '0d1ff2530f17451bb8437c6ea584282e':
    #     continue

    for m in narrative_metadata:
        if m['id'] == item['id']:
            narrative_id = m['narrative_id']
            continue

    d = dict()

    d['narrative_id'] = narrative_id
    d['title'] = item["title"]
    d['id'] = item["id"]
    d['url'] = item["url"]
    d['tags'] = ['World\'s Women 2020', 'narrative']
    d['tags'].append(narrative_id)
    d['description'] = item["description"]

    item.update(item_properties={'tags': d['tags']})

    narrative_cat.append(d)

utils.dictList2tsv(
    narrative_cat, 'narratives/story-map-data/_narrative_cat.txt')

# print(f' -- Item title: {item["title"]}')
# print(f' -- Item id: {item["id"]}')
# print(f' -- Item url: {item["url"]}')
# print(f' -- Item tags: {item["tags"]}')
# print(f' -- Item description: {item["description"]}')
# print(f' -- Item description: {item["data"]}')
# print(' -------')

# storymap_item = gis.content.get(item["id"])
# json_data = storymap_item.get_data()
# # make your changes to JSON
# # storymap_item.update(data=json_data)
