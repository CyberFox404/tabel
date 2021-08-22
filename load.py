#dict2 = eval(str1)

#import json
#dict = {'one':1, 'two':2, 'three': {'three.1': 3.1, 'three.2': 3.2 }}

#print(dict)
#print(json.dumps(dict))


f = open("main.py", "r")
print(eval(f.read()))