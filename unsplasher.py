import requests
import time
import os
import re
import sys

RESOLUTION = "1920x1080"

if len(sys.argv) != 2:
    exit()

num_of_images = int(sys.argv[1])
current_dir = os.path.dirname(__file__) or os.getcwd()

files = os.listdir(current_dir)

files = [file for file in files if file[-4:] == ".jpg"]


count = ([int(re.search(r"\d+", file)[0]) for file in files])
if not count:
    count = 0
else:
    count = max(count)

files = [open(file, 'rb') for file in files]

url = "https://source.unsplash.com/featured/" + RESOLUTION + "/"

i = count + 1
while(i < count + 1 + int(num_of_images)):

    response = requests.get(url, stream=True)
    if not response.ok:
        print (response)
        continue

    print("Getting image %s" % str(i))

    duplicate = False
    for img in files:
        if img.read() == response.content:
            print("Already have that one. Retrying...")
            duplicate = True
        img.seek(0)

    if duplicate:
        time.sleep(2)
        continue

    handle = open("pic" + str(i) + ".jpg","wb+")
    handle.write(response.content)
    handle.close()

    new_file = open("pic" + str(i) + ".jpg", 'rb')

    files.append(new_file)
    time.sleep(2)
    i += 1
    
for img in files:
    img.close()