#dict2 = eval(str1)

#import json
#dict = {'one':1, 'two':2, 'three': {'three.1': 3.1, 'three.2': 3.2 }}

#print(dict)
#print(json.dumps(dict))

import requests
import json
import requests
import re
from bs4 import BeautifulSoup

target_url = "https://raw.githubusercontent.com/CyberFox404/tabel/main/main.py"
r = requests.get(target_url, allow_redirects=True)

open('tabel_calendar_2021_load.py', 'wb').write(r.content)


f = open("tabel_calendar_2021_load.py", "r")
print(eval(f.read()))

exit()



try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

content = urllib2.urlopen(target_url)


print(content)
print()

for line in content:
    print (line)
#content=urllib.request.urlopen("https://raw.githubusercontent.com/CyberFox404/tabel/main/main.py")

#import urllib.request  # the lib that handles the url stuff


#content=urllib.urlopen(url)
#print(content)
#print()
#for line in content:
#    print (line)


#f = open("main.py", "r")
#print(eval(f.read()))