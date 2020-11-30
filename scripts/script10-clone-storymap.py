import json
import utils
import utils_arcgis
from datetime import datetime, timezone

user, gis = utils_arcgis.connect_to_arcGIS()

print(user)
print(gis)

# Enter the Item ID for the StoryMap to be cloned:
template_id  = 'df45ccd1dc1246b08c466b892abaa355'

# Get StoryMap template:
storymap_template = gis.content.get(template_id)
print(storymap_template)

# Get data from StoryMap template
storymap_data = storymap_template.get_data()
#print(storymap_data)

with open('test_original.json', 'w') as json_file:
    json.dump(storymap_data, json_file, indent=4)

# make your changes to JSON

# Read new json file:
with open('test.json') as f:
  new_storymap_data = json.load(f)

# Clone template into a new storymap:
storymap_new = gis.content.clone_items(items=[storymap_template],
                                       folder = "World\'s Women 2020 Narratives - Staging")

print(storymap_new)

storymap_new[0].update(data=new_storymap_data,
                       item_properties={'tags':'tag1,tag2',
                                        'title': 'New Title',
                                        'description': 'new description',
                                        'snippet': 'new snippet'})


