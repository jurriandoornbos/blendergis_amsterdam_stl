from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
import os
import glob

dir  = "raw_data"
#read the bag_ids file:

with open("bag_ids.txt", "r") as f:
    ids = f.readlines()

#download all the ids
for id in ids:
    id = id.strip("\n")
    id= id.strip()
    url = "https://data.3dbag.nl/obj/v210908_fd2cee53/3dbag_v210908_fd2cee53_{}.zip".format(id)
    response = urlopen(url)
    zipfile = ZipFile(BytesIO(response.read()))
    zipfile.extractall(path = dir )
    print(str(id), ": done")




for f in os.listdir(dir):
    if os.path.isfile(os.path.join(dir, f)):
        if not "lod22" in f:
            os.remove(dir+ "/" + f)
            print('removed: ' + f)

