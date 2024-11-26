from collections import OrderedDict
import json

with open('api_codes/json_files/allProducts.json', 'r', encoding='UTF-8') as json_read :
    all_drinks = json.load(json_read, object_pairs_hook=OrderedDict)

tempList = []
for drink in all_drinks:
    if drink["name"] not in tempList: tempList.append(drink["name"])

for i in range(0, 90):
    print(tempList[i*5:i*5+10])