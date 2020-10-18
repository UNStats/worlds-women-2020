import json
import utils
import utils_arcgis
from bs4 import BeautifulSoup

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

narrative_cat = []

myfile = open('control/linked_narratives.txt', 'w')

for item in user_items:

    if item["id"] in galleries:
        continue

    if item["id"] == '0d1ff2530f17451bb8437c6ea584282e':
        continue

    # Get metadata for current item

    for m in narrative_metadata:
        if m['id'] == item['id']:
            narrative_id = m['narrative_id']
            title = m['title']
            url = m['url']
            continue

    myfile.write('\n=======================================================')
    myfile.write("\nnarrative_id=\t%s" % narrative_id)
    myfile.write("\ntitle=\t%s" % title)
    myfile.write("\nurl=\t%s" % url)
    myfile.write('\n=======================================================')

    json_data = item.get_data()

    for i in json_data['values']['story']['sections']:
        # print(i['content'])
        # print('-----')

        soup = BeautifulSoup(i['content'], "html.parser")

        linked_stories = soup.findAll('a', {"class": "narrative-ref"})

        for j in linked_stories:
            print(j)

            myfile.write("\n\t%s" % j)

            href = j.attrs['href']
            text = j.get_text()

            myfile.write("\n\thref=\t%s" % href)
            myfile.write("\n\ttext=\t%s" % text)

            linked_narrative_id = href.replace('#', '')
            print(linked_narrative_id)

            myfile.write("\n\tlinked_narrative_id =\t%s" %
                         linked_narrative_id)

            narrative_metadata_id = None
            narrative_metadata_title = None
            link = href

            for l in narrative_metadata:
                # print(l['narrative_id'])

                if l['narrative_id'] == linked_narrative_id:
                    narrative_metadata_id = l['id']
                    narrative_metadata_title = l['title']
                    link = base_url + narrative_metadata_id + href

                    continue

            myfile.write("\n\tnarrative_metadata_title:\t%s" %
                         narrative_metadata_title)
            myfile.write("\n\tlink:\t%s" %
                         link)
            myfile.write("\n\t---------------------------------")

            j.attrs['href'] = link

        i['content'] = str(soup)

    with open('narratives/story-map-data/' + narrative_id + '.json', 'w') as fout:
        json.dump(json_data, fout, indent=4)

    item.update(data=json_data)

myfile.close()
