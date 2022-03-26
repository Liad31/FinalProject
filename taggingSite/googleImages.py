import json

import requests
from PIL import Image
from os import listdir
from os.path import isfile, join
import os
# onlyfiles = [f for f in listdir('./images2') if isfile(join('./images2', f))]
# for f in onlyfiles:
#     path = os.getcwd() + '/images2/' + f
#     im1 = Image.open(fr'{path}')
#     path = 'images2/' + f.split('.')[0] + ".png"
#     im1.save('images2/' + f.split('.')[0] + ".png")

headers={"Content-Type": "application/json"}
for file in os.listdir('images2/'):
    fileName=file.split(".")[0]
    type = file.split(".")[1]
    path=os.path.join('images2/',file)
    if type != 'png':
        os.remove(path)
        continue
    # try:
    #     requests.post("http://localhost:8001/api/database/postNewImage", data=json.dumps({"id":fileName}), headers=headers)
    # except Exception as e:
    #     os.remove(path)
    #     print(path)
    #     print(e)

# path = './images2'
# files = os.listdir(path)
#
#
# for index, file in enumerate(files):
#     os.rename(os.path.join(path, file), os.path.join(path, ''.join([str(file) + '__', '.png'])))
