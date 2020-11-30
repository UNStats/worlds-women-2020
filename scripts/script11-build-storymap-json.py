
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


#------------------------------
# Conect to ArcGIS online
#------------------------------

user, gis = utils_arcgis.connect_to_arcGIS()

print(user)
print(gis)

# Enter the Item ID for the StoryMap to be cloned:
template_id  = 'df45ccd1dc1246b08c466b892abaa355'

# Get StoryMap template:
storymap_template = gis.content.get(template_id)

# Get data from StoryMap template
storymap_data = storymap_template.get_data()


#---------------------------------
# Build new storymap data
#---------------------------------

themes = [{'theme_id': 'ND', 'theme_desc': 'Power and decision making'},
          {'theme_id': 'NE', 'theme_desc': 'Education'},
          {'theme_id': 'NH', 'theme_desc': 'Health'},
          {'theme_id': 'NN', 'theme_desc': 'Environment'},
          {'theme_id': 'NP', 'theme_desc': 'Population and families'},
          {'theme_id': 'NV', 'theme_desc': 'Violence against women and the girl child'},
          {'theme_id': 'NW', 'theme_desc': 'Economic empowerment'}]


#----------------------------------
# fixed template values
#----------------------------------

contentActions = [],
creaDate = 1602805607319,
pubDate = 1602805607319,
status = 'PUBLISHED'
media =  {
            "type": "image",
            "image": {
                "url": "https://raw.githubusercontent.com/UNStats/worlds-women-2020/main/assets/photos/Medium/ben-white-EMZxDosijJ4-unsplash.jpg",
                "type": "image",
                "altText": "",
                "sizes": [
                    {
                        "name": "ben-white-EMZxDosijJ4-unsplash.jpg",
                        "url": "https://raw.githubusercontent.com/UNStats/worlds-women-2020/main/assets/photos/Medium/ben-white-EMZxDosijJ4-unsplash.jpg",
                        "width": 1200
                    }
                ],
                "display": "fill"
            }
        }

# Get list of directories under narrative3
narrative_ids = os.listdir('narratives3/')
print(f'narrative_ids = {narrative_ids}')
print('------------')

for n in narrative_ids:
    
    path = 'narratives3/'+ n +'/index.html'

    theme_id = n[0:2]

    n_theme = next((t['theme_desc'] for t in themes if t['theme_id'] == theme_id), None)

    # read html content

    f = open(path, encoding='utf8')      # simplified for the example (no urllib)
    soup = BeautifulSoup(f, features='html.parser')
    f.close()

    n_title = soup.find('div', attrs={'class': 'title'}).string

    n_description = '<div><ul><li><b>Narrative ID</b>: '+ n +'</li><li><b>Narrative Title</b>: '+ n_title +'</li><li><b>Theme</b>: '+ n_theme +'</li><li><b>SDG indicators</b>: </li><li><b>Beijing objectives</b>: </li><li><b>Related-narratives</b>: </li><li><b>Labels</b>: </li></ul><b>App ID</b>: [ITEM_ID]<br /></div><div><br /></div>'
    
    n_sections = soup.findAll('section')

    # Generate list of sections:
    
    sections = []

    for i in range(len(n_sections)):


        # Get section title from <h2> element if it exists:
        if i > 1 and i < len(n_sections)-2:
            h2_tag = n_sections[i].find("h2")
            if h2_tag:
                h2_tag.extract()
                section_title = '<span style=\"font-size:26px;\">' + h2_tag.text + '</span>'
            else:
                section_title = '<span style=\"font-size:26px;\"> </span>'
        else:
            section_title = '<span style=\"font-size:26px;\"> </span>'
        
        # Remove <section> tag:
        section_content = str(n_sections[i])
        section_content = re.sub(r"<section (.*?)>", "", section_content)
        section_content = re.sub(r"</section(.*?)>", "", section_content)


        section_data = dict()

        if i==0:
            section_data['title'] =  '<p><span style=\"font-size:18px;\"><span style=\"color:#FF8C00;\"><strong>' + n_theme +'</strong></span></span></p>\n'
            section_data['content'] =  '<style type=\"text/css\">    p,\n    h1,\n    h2,\n    h3,\n    h4,\n    h5,\n    li {\n        margin-bottom: 2em;\n    }\n\n    .sidePanel .content {\n        font-size: 13px;\n    }\n\n    title {\n        font-size: 40px;\n        line-height: 1.6;\n\n    }\n\n    .methodology {\n        margin: 10px;\n        padding: 40px 20px 20px 20px;\n        background-color: rgb(255, 206, 151);\n    }\n\n    .concept {\n        font-weight: 600;\n    }\n\n    .footnote-index {\n        vertical-align: super;\n        font-size: 0.7em;\n        margin-left: 2px;\n        color: #FF5733;\n    }\n\n    .section a[data-storymaps] {\n        border-bottom: none !important;\n        text-decoration: none;\n        cursor: pointer;\n        color: #FF5733;\n    }\n\n    /* This is based on https: //www.sitepoint.com/accessible-footnotes-css/ */\n\n    .footnotes {\n        border-top: 1px solid #555;\n\n        font-size: 0.9em;\n    }\n\n    .references {\n        font-size: 0.9em;\n    }\n</style>\n<div class=\"title\">'+ n_title +'</div>\n'
        elif i==1:
            
            section_data['title'] = '<span style=\"font-size:26px;\">Key points</span>'
            section_data['content'] = section_content

        elif i in (len(n_sections)-2, len(n_sections)-1):
            section_data['title'] = section_title
            section_data['content'] = section_content

        else:

            section_data['title'] = section_title
            section_data['content'] = section_content


        section_data['contentActions'] = contentActions
        section_data['creaDate'] = creaDate
        section_data['pubDate'] = pubDate
        section_data['status'] = status
        section_data['media'] = media 

        sections.append(section_data)

    new_storymap_data = copy.deepcopy(storymap_data) 

    new_storymap_data['values']['title'] = n_theme
    new_storymap_data['values']['story']['sections'] = sections

    # file_sections = n + '_sections.json'
    # with open(file_sections, 'w') as json_file:
    #     json.dump(sections, json_file, indent=4)

    # Clone template into a new storymap:
    storymap_new = gis.content.clone_items(items=[storymap_template],
                                        folder = "World\'s Women 2020 Narratives - Staging")

    #print(n)
    #print(storymap_new)

    storymap_new[0].update(data=new_storymap_data,
                           item_properties={'tags': n,
                                            'title': n + ' - ' + n_title,
                                            'description': n_theme,
                                            'snippet': '..'})




    