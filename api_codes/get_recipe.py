from collections import OrderedDict
import json

with open('api_codes/json_files/allRecipes.json', 'r', encoding='UTF-8') as json_read :
    all_recipes = json.load(json_read, object_pairs_hook=OrderedDict)


def getallrecipes():
    return all_recipes

def search_byname(name):
    temp_list = []
    for j in all_recipes:
        if name in j["name"] and j not in temp_list: temp_list.append(j)
    temp_list.insert(0, "Total result found : {}".format(len(temp_list)))
    return temp_list

def search_bycode(code):
    temp_list = []
    for j in all_recipes:
        if code == j["code"]: return j
    return "no result found"

def search_byings(codes):
    temp_list = []

    input_codes = list(map(''.join, zip(*[iter(codes)]*3)))
    print(input_codes)

    for recipe in all_recipes:
        recipe_codes = list(map(''.join, zip(*[iter(recipe["code"])]*3)))
        cnt = 0
        for i in input_codes:
            if i[:2] == recipe_codes[:2]:
                cnt += 1
                print(cnt)
                
        if cnt > 0:
            tempDict = {}
            tempDict["code"] = recipe["code"]
            tempDict["english_name"] = recipe["english_name"]
            tempDict["korean_name"] = recipe["korean_name"]
            tempDict["tag1"] = recipe["tag1"]
            tempDict["tag2"] = recipe["tag2"]
            tempDict["have"] = "{}/{}".format(cnt, len(recipe_codes))
            
            temp_list.append(tempDict)

    return temp_list