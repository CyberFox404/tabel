#dict2 = eval(str1)

#import json
#dict = {'one':1, 'two':2, 'three': {'three.1': 3.1, 'three.2': 3.2 }}

#print(dict)
#print(json.dumps(dict))


https://raw.githubusercontent.com/CyberFox404/tabel/main/main.py?token=ABY4NHTZ4LFN5TBK6Q73QFLBEIMNM


import urllib
content=urllib.request.urlopen("https://wordpress.org/plugins/about/readme.txt")
for line in content:
    print (line)


f = open("main.py", "r")
print(eval(f.read()))