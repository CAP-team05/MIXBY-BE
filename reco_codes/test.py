import json

with open('api_codes/json_files/allRecipes.json') as f1:
    data = json.load(f1)

print(len(data))
for item in data:
    print(item['korean_name'] + "\t\t" + item['english_name'] + "\t" + item['code'])