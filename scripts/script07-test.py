import json
import utils
import utils_arcgis


online_username, gis_online_connection = utils_arcgis.connect_to_arcGIS()

print(online_username)
print(gis_online_connection)


user = gis_online_connection.users.get('gonzalezmorales_undesa')

user_items = user.items(folder='tests', max_items=800)

narrative_cat = []

for item in user_items:

    if()

    d = dict()

    d['narrative_id'] = item["title"][:item["title"].find(' ')]
    d['title'] = item["title"]
    d['id'] = item["id"]
    d['url'] = item["url"]
    d['tags'] = item["tags"]
    d['description'] = item["description"]

    narrative_cat.append(d)

    json_data = item.get_data()

    with open('control/'+d['narrative_id']+'_before.json', 'w') as fout:
        json.dump(json_data, fout, indent=4)

    json_data['values']['settings']['header']['linkURL'] = 'https://worlds-women-2020-data-undesa.hub.arcgis.com/'
    json_data['values']['settings']['header']['logoURL'] = 'https://raw.githubusercontent.com/UNStats/worlds-women-2020/main/assets/logos/UNStats%20Logo-short.png'

    json_data["annotations_unsd"] = {"narrative_id": d['narrative_id']}

    item.update(data=json_data)

    json_data = item.get_data()

    with open('control/'+d['narrative_id']+'_after.json', 'w') as fout:
        json.dump(json_data, fout, indent=4)

utils.dictList2tsv(
    narrative_cat, 'control/_narrative_cat.txt')

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
