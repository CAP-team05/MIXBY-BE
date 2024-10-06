from my_modules import gettype
import json

# json file 읽기
with open('new_data/drinks.json', 'r', encoding='UTF-8') as json_read :
    json_str = json.load(json_read)

cnt = 1
new_list = []
codes = []

for j in json_str:
    code = j['code']
    codes.append(code)

codes = sorted(codes)

for c in codes:
    for j in json_str:
        if c == j['code']:
            c = j['code']
            n = j['name']
            v = j['volume']
            a = j['alcohol']
            t = gettype.searchtypeKOR(n)
            
            new_dict = {}
            new_dict['code'] = c
            new_dict['name'] = n
            new_dict['type'] = t
            new_dict['volume'] = v
            new_dict['alcohol'] = a
            
            new_list.append(new_dict)

with open('new_data/drinks_copy.json', 'w', encoding='utf-8') as f:
    json.dump(new_list, f, ensure_ascii = False, indent=4)

print('\nfile successfully created!\n')