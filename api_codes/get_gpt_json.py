from collections import OrderedDict
import json

with open('api_codes/json_files/recipes.json', 'r', encoding='UTF-8') as json_read :
    all_recipes = json.load(json_read, object_pairs_hook=OrderedDict)


temp_list = []
for i in range(0, len(all_recipes)-4):
    r0 = all_recipes[i]['name']
    r1 = all_recipes[i+1]['name']
    r2 = all_recipes[i+2]['name']
    r3 = all_recipes[i+3]['name']
    r4 = all_recipes[i+4]['name']

    line = '<요청> {}, {}, {}, {}, {}'.format(r0, r1, r2, r3, r4)
    temp_list.append(line)

with open('api_codes/json_files/gpt.json', 'w', encoding='utf-8') as f:
    json.dump(temp_list, f, ensure_ascii = False, indent=4)