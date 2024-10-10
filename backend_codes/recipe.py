import json

# json file 읽기
with open('backend_codes/new_data/recipes.json', 'r', encoding='UTF-8') as json_read :
    json_str = json.load(json_read)

l = []
for j in json_str:
    l.append(j["name"])

with open('backend_codes/new_data/recipe_names.json', 'w', encoding='utf-8') as f:
    json.dump(l, f, ensure_ascii = False, indent=4)