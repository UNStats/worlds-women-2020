from PIL import Image
import os
import utils
import time

# -----------------------------------
# Read all excel files in narratives
# -----------------------------------


path = "assets/photos/"
timestr = time.strftime("%Y%m%d-%H%M%S")


data_files = []

for root, dirs, files in os.walk(path):
    if len(files) > 0:
        for f in files:

            basewidth = 1200
            img = Image.open(root + '/'+f)
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)
            img.save('assets/photos/medium/' + f)
