from arcgis.gis import GIS
import sys
import json
import getpass
import os
import utils
import copy
import requests


def connect_to_arcGIS():
    """Open connection to ArcGIS Online Organization"""

    online_username = input('Username: ')
    online_password = getpass.getpass('Password: ')
    online_connection = "https://www.arcgis.com"
    gis_online_connection = GIS(online_connection,
                                online_username,
                                online_password)

    return online_username, gis_online_connection


def open_data_group(gis_online_connection, id):
    """Explore existing open data gruop"""

    open_data_group = gis_online_connection.groups.get(id)
    return (open_data_group)


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
        html_card = html_card + '  <ul>'

        for t in s['themes']:

            html_card = html_card + '    <li><span class="theme_code">' + t['code'] + '</span> - ' + \
                '<span class="theme_name">' + t['name'] + '</span>'
            html_card = html_card + '        <ul>'

            for st in t['subthemes']:
                html_card = html_card + '    <li><span class="subtheme_code">' + \
                    st['code'] + '</span> - ' + \
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
            user_items = user.items(
                folder='World\'s Women 2020 Data', max_items=800)
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


def publish_csv(s,
                item_properties,
                thumbnail,
                layer_info,
                gis_online_connection,
                online_username,
                file,
                statistic_field='OBS_VALUE',
                property_update_only=False,
                color=[169, 169, 169]):

    # Check if service name is available; if not, update the link
    service_title = s['code']
    print('------------------------------------------------------------')
    print(f'service_title={service_title}')

    service_title_num = 1

    # Check if service name is available:
    gis_online_connection.content.is_service_name_available(
        service_name=service_title, service_type='featureService')

    while not gis_online_connection.content.is_service_name_available(service_name=service_title, service_type='featureService'):
        service_title = s['code'] + '_' + str(service_title_num)
        service_title_num += 1
        print('------------------------------------------------------------')
        print(f'service_title_num={service_title_num}')

    print('------------------------------------------------------------')
    print(f'service_title={service_title}')

    # print(s_card)
    if os.path.isfile(file):

        csv_item_properties = copy.deepcopy(item_properties)
        csv_item_properties['name'] = service_title
        csv_item_properties['title'] = service_title
        csv_item_properties['type'] = 'CSV'
        csv_item_properties['url'] = ''

        print('------------------------------------------------------------')
        print(f'csv_item_properties={csv_item_properties}')

        # Does this CSV already exist
        csv_item = find_online_item(
            csv_item_properties['title'], online_username, gis_online_connection)

        if csv_item is None:
            print('------------------------------------------------------------')
            print('Adding CSV File to ArcGIS Online....')

            # display(gis_online_connection)
            print('------------------------------------------------------------')
            print(f'thumbnail={thumbnail}')
            print('------------------------------------------------------------')
            print(f'file={file}')

            file = '/data/processed/series_csv/S_0320.csv'

            csv_item_properties = {'title': 'Test Title',
                                   'description': 'Test Description',
                                   'tags': 'tag1,tag2'}

            csv_item = gis_online_connection.content.add(
                item_properties=csv_item_properties, thumbnail=thumbnail, data=file)
            print('------pass 2------')
            if csv_item is None:
                return None

            print('Analyze Feature Service....')

            # Change attribute types:
            publish_parameters = analyze_csv(
                csv_item['id'], gis_online_connection)

            if publish_parameters is None:
                return None
            else:
                publish_parameters['name'] = csv_item_properties['title']
                publish_parameters['layerInfo']['name'] = csv_item_properties['layer_title']

                print('Publishing Feature Service....')

                csv_lyr = csv_item.publish(
                    publish_parameters=publish_parameters, overwrite=True)

                # Update the layer infomation with a basic rendering based on the Latest Value
                # use the hex color from the SDG Metadata for the symbol color

        else:
            # Update the Data file for the CSV File
            csv_item.update(item_properties=csv_item_properties,
                            thumbnail=thumbnail, data=file)

            # Find the Feature Service and update the properties
            csv_lyr = find_online_item(
                csv_item_properties['title'], online_username, gis_online_connection)

    else:
        print('File ' + file + ' does not exist.')
        return None


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

            # IndicatorCode is coming in as a date Field make the correct

            # if field['name'] == 'target_descEN':
            #     field['type'] = 'esriFieldTypeString'
            #     field['sqlType'] = 'sqlTypeNVarchar'

            # elif field['name'] == 'min_year':
            #     field['type'] = 'esriFieldTypeInteger'
            #     field['sqlType'] = 'sqlTypeInt'

            # elif field['name'].startswith('value_'):
            #     field['type'] = 'esriFieldTypeDouble'
            #     field['sqlType'] = 'sqlTypeFloat'

            # else:
            #     field['type'] = 'esriFieldTypeString'
            #     field['sqlType'] = 'sqlTypeNVarchar'

        # set up some of the layer information for display
        analyze_json_data['publishParameters']['layerInfo']['displayField'] = 'OBS_VALUE'
        return analyze_json_data['publishParameters']
    except:
        print('Unexpected error:', sys.exc_info()[0])
        return None


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


def update_item_categories(s, gis_online_connection):
    update_url = gis_online_connection._url + "/sharing/rest/content/updateItems"
    items = [{item["id"]:{"categories": [
        "/Categories/Gender"]}}]
    update_params = {'f': 'json',
                     'token': gis_online_connection._con.token,
                     'items': json.dumps(items)}
    r = requests.post(update_url, data=update_params)
    update_json_data = json.loads(r.content.decode("UTF-8"))
    print(update_json_data)


def set_content_status(gis_online_connection, update_item, authoratative=True):
    sharing_url = gis_online_connection._url + \
        "/sharing/rest/content/items/" + update_item.id + "/setContentStatus"
    sharing_params = {'f': 'json', 'token': gis_online_connection._con.token,
                      'status': 'org_authoritative' if authoratative else 'deprecated',
                      'clearEmptyFields': 'false'}
    r = requests.post(sharing_url, data=sharing_params)
    sharing_json_data = json.loads(r.content.decode("UTF-8"))
