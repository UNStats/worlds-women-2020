import json
import utils
import utils_arcgis
from arcgis.gis import GIS

online_username = 'gonzalezmorales_undesa'
online_password = 'LL&66kYrEo'
online_connection = "https://www.arcgis.com"
gis_online_connection = GIS(online_connection,
                            online_username,
                            online_password)
print(online_username)


user = gis_online_connection.users.get('unstats_admin')

user_items = user.items(folder='Historic Data 2019Q3G01', max_items=1000)

for i in user_items:
    i.protect(enable = False)
    print(f'Item: {i.title}')
    i.delete()


