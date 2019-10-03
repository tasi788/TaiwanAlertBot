import requests
from glob import glob

filelist = glob('*.xml')
url = 'http://localhost/post'
print(filelist)
for x in filelist:
    file = open(x, 'rb').read()
    r = requests.post(url, data=file)
