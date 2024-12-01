from collections import OrderedDict
import json

with open('api_codes/json_files/oldRecipes.json', 'r', encoding='UTF-8') as json_read :
    allRecipes = json.load(json_read, object_pairs_hook=OrderedDict)


with open('api_codes/json_files/allIngredients.json', 'r', encoding='UTF-8') as json_read :
    allIngredients = json.load(json_read, object_pairs_hook=OrderedDict)


resultList = []

for recipe in allRecipes:
    tempDict = {}

    tempDict["english_name"] = recipe["english_name"]
    tempDict["korean_name"] = recipe["korean_name"]


    ingList = []
    for recipeIng in recipe["ingredients"]:
        for ing in allIngredients:
            ingDict = {}
            if recipeIng["name"] == ing["name"]:
                ingDict["name"] = ing["name"]
                ingDict["code"] = ing["code"]
                ingDict["amount"] = recipeIng["amount"]
                ingDict["unit"] = recipeIng["unit"]
                ingList.append(ingDict)

    code = ""
    for ing in ingList:
        code = code + ing["code"]

    tempDict["code"] = code
    tempDict["ingredients"] = ingList

    

    tempDict["instructions"] = recipe["instructions"]
    tempDict["tag1"] = recipe["tag1"]
    tempDict["tag2"] = recipe["tag2"]

    resultList.append(tempDict)


with open('api_codes/json_files/allRecipes.json', 'w', encoding='utf-8') as f:
    json.dump(resultList, f, ensure_ascii = False, indent=4)

print('\nfile successfully created!\n')