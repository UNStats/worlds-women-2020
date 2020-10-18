import sys
import os
from arcgis.gis import GIS
import copy
import requests
import json
import utils
import utils_arcgis

data_dir = 'data/processed/series_csv/'
data_files = os.listdir('data/processed/series_csv')
# print(data_files)

series_metadata = utils.open_json(
    'data/external/seriesMetadata.json')


# ----------------------
# Set thumbnail link
# ----------------------

thumbnail = 'https://raw.githubusercontent.com/UNStats/worlds-women-2020/main/assets/photos/Thumbnails/WW2020.png'

online_username = ''
online_password = ''
online_connection = "https://www.arcgis.com"
gis_online_connection = GIS(online_connection,
                            online_username,
                            online_password)
print(online_username)


# --------------------------------------------------------------------------------
def build_series_card(s):
    """ Build series metadata card """

    try:
        s_card = dict()

        theme_codes = []
        theme_names = []
        subtheme_codes = []
        subtheme_names = []

        for t in s['themes']:
            theme_codes.append(t['code'])
            theme_names.append(t['name'])

            for st in t['subthemes']:
                subtheme_codes.append(st['code'])
                subtheme_names.append(st['name'])

        # print(f'theme_codes: {theme_codes}')
        narratives = s['narratives']
        tags = s['tags']
        tags.extend(narratives)
        tags.extend(theme_codes)
        tags.append('WorldsWomen2020')
        tags = ",".join(tags)

        print('==========================')
        print(f'tags={tags}')

        s_desc = s['name'].replace('%', 'percent').replace(
            ',', ' ').replace('/', ' ')

        title = 'Series ' + s['code'] + ': ' + s_desc

        s_card['title'] = (title[:250] + '..') if len(title) > 250 else title

        layer_title = s['code']

        s_card['layer_title'] = layer_title[:89] if len(
            layer_title) > 88 else layer_title  # this is very important!!!

        s_card['snippet'] = s_card['title']

        html_card = ''
        html_card = html_card + \
            '<div style="background-color: #f78b33; color:#fff; padding: 15px">'
        html_card = html_card + \
            '  <h1>World\'s Women 2020: Trends and Statistics.< /h1 >'
        html_card = html_card + '</div>'
        html_card = html_card + '<div style="background-color: #f4f4f4; padding: 15px">'
        html_card = html_card + '  <p><strong>Themes:</strong>'
        html_card = html_card + '  <ul style="list-style-type:none">'

        for t in s['themes']:

            html_card = html_card + '    <li>' + \
                '<span class="theme_name">' + t['name'] + '</span>'
            html_card = html_card + '        <ul style="list-style-type:none">'

            for st in t['subthemes']:
                html_card = html_card + '    <li>' + \
                    '<span class="subtheme_name">' + \
                    st['name'] + '</span></li>'

            html_card = html_card + '        </ul>'
            html_card = html_card + '      </li>'
        html_card = html_card + '  </ul>'
        html_card = html_card + '  </p> </div>'

        s_card['description'] = html_card
        s_card['tags'] = tags

        return s_card
    except:
        print('Unexpected error:', sys.exc_info()[0])
        return None

# ------------------------------------------------------------------------


def find_online_item(title, owner, gis_online_connection, force_find=True):

    try:

        # Search for this ArcGIS Online Item
        query_string = "title:'{}' AND owner:{}".format(title, owner)
        print('Searching for ' + title)
        # The search() method returns a list of Item objects that match the
        # search criteria
        search_results = gis_online_connection.content.search(query_string)

        if search_results:
            for item in search_results:
                if item['title'] == title:
                    print(' -- Item ' + title + ' found (simple find)')
                    return item

        if force_find:
            user = gis_online_connection.users.get(owner)
            user_items = user.items(folder='Open Data', max_items=800)
            for item in user_items:
                if item['title'] == title:
                    print(' -- Item ' + title + ' found (force find)')
                    return item
            print(' -- Item ' + title + ' not found (force find)')
            return None

        print(' -- Item ' + title + ' not found (simple find)')
        return None

    except:
        print('Unexpected error:', sys.exc_info()[0])
        return None

# --------------------------------------------------------------------------


def set_field_alias(field_name):

    if field_name == 'SERIES':
        return 'Series Code'
    elif field_name == 'SERIES_DESC':
        return 'Series Name'
    elif field_name == 'REF_AREA':
        return 'Geographic Area Code'
    elif field_name == 'REF_AREA_DESC':
        return 'Geographic Area Name'
    elif field_name == 'GEOLEVEL':
        return 'Geographic Area Level'
    elif field_name == 'GEOLEVEL_DESC':
        return 'Geographic Area Level Description'
    elif field_name == 'OBS_VALUE':
        return 'Value'
    elif field_name == 'UNIT_MEASURE':
        return 'Measurement Unit Code'
    elif field_name == 'UNIT_MEASURE_DESC':
        return 'Measurement Unit Description'
    else:
        return utils.camel_case_split(field_name.replace('_', ' ')).replace(' DESC', ' Description').title()

# -------------------------------------------------


def analyze_csv(item_id, gis_online_connection):
    try:
        sharing_url = gis_online_connection._url + \
            '/sharing/rest/content/features/analyze'

        analyze_params = {'f': 'json',
                          'token': gis_online_connection._con.token,
                          'sourceLocale': 'en-us',
                          'filetype': 'csv',
                          'itemid': item_id}

        r = requests.post(sharing_url, data=analyze_params)

        analyze_json_data = json.loads(r.content.decode('UTF-8'))

        for field in analyze_json_data['publishParameters']['layerInfo']['fields']:
            field['alias'] = set_field_alias(field['name'])

        # set up some of the layer information for display
        analyze_json_data['publishParameters']['layerInfo']['displayField'] = 'OBS_VALUE'

        return analyze_json_data['publishParameters']
    except:
        print('Unexpected error:', sys.exc_info()[0])
        return None


# ----------------------------
failed_series = []
for d in data_files:

    # if d != 'S_0010.csv':
    #     continue

    series = d.replace('.csv', '')

    if series not in ['S_0280', 'S_0390', 'S_0680', 'S_0790', 'S_0795', 'S_0960', 'S_0970', 'S_1150', 'S_1710', 'S_1750']:
        continue

    print(series)

    s = None
    for m in series_metadata:
        if m['code'] == series:
            s = m
            continue
    print(f's: {s}')

    # csv file to be uploaded:
    file = os.path.join(data_dir + d)
    print(file)

    s_card = build_series_card(s)
    print(f'os.path.isfile(file){os.path.isfile(file)}')

    try:
        if os.path.isfile(file):
            csv_item_properties = copy.deepcopy(s_card)
            csv_item_properties['name'] = s['name'].replace('%', 'percent').replace(
                ',', ' ').replace('/', ' ')
            csv_item_properties['title'] = s['name'].replace('%', 'percent').replace(
                ',', ' ').replace('/', ' ')
            csv_item_properties['type'] = 'CSV'
            csv_item_properties['url'] = ''

            print(f'csv_item_properties = {csv_item_properties}')

            csv_item = find_online_item(
                csv_item_properties['title'], online_username, gis_online_connection)

            if csv_item is None:
                print('Adding CSV File to ArcGIS Online....')

                csv_item = gis_online_connection.content.add(item_properties=csv_item_properties,
                                                             thumbnail=thumbnail,
                                                             data=file,
                                                             folder='World\'s Women 2020 Data')

                print('Analyze Feature Service....')

                publish_parameters = analyze_csv(
                    csv_item['id'], gis_online_connection)
                publish_parameters['name'] = csv_item_properties['title'][0:80]
                publish_parameters['layerInfo']['name'] = csv_item_properties['layer_title'][0:80]

                print('Publishing Feature Service....')

                csv_lyr = csv_item.publish(
                    publish_parameters=publish_parameters, overwrite=True)

                # print('.......call generate renderer within publish_csv')
    except:
        print('Unexpected error:', sys.exc_info()[0])
        failed_series.append(s['code'])

print(f'failed_series={failed_series}')
