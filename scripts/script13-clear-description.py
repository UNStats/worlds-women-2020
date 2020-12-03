import json
import utils
import utils_arcgis


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

    # Skip galleries (they are saved in the same folder as narratives)
    if item["id"] in galleries:
        continue
    
    item.update(item_properties={'snippet': ' '})

    print(item['id'])
    print(item['title'])
    
