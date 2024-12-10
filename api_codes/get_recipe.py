from collections import OrderedDict
import json

with open('api_codes/json_files/allRecipes.json', 'r', encoding='UTF-8') as json_read :
    all_recipes = json.load(json_read, object_pairs_hook=OrderedDict)

def search_byname(name):
    for j in all_recipes:
        if name == j["korean_name"].replace(" ", ""):
            return j
    return "no result found"

def search_bycode(code):
    for j in all_recipes:
        if code == j["code"]: return j
    return "no result found"

def search_byings(codes):
    temp_list = []
    
    for recipe in all_recipes:
        rc = recipe["code"]
        recipe_codes = [rc[i:i+3] for i in range(0, len(rc), 3)]
        input_codes = [codes[i:i+3] for i in range(0, len(codes), 3)]

        matching_chunks = set(recipe_codes) & set(input_codes)
        cnt = len(matching_chunks)
                
        if cnt > 0:
            tempDict = {}
            tempDict["code"] = recipe["code"]
            tempDict["english_name"] = recipe["english_name"]
            tempDict["korean_name"] = recipe["korean_name"]
            tempDict["tag1"] = recipe["tag1"]
            tempDict["tag2"] = recipe["tag2"]
            tempDict["have"] = "{}-{}".format(cnt, len(recipe_codes))
            
            temp_list.append(tempDict)

    return temp_list