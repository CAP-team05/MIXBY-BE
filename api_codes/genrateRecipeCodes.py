from collections import OrderedDict
import json

with open('api_codes/json_files/allBases.json', 'r', encoding='UTF-8') as json_read :
    all_bases = json.load(json_read, object_pairs_hook=OrderedDict)



allBases = []




with open('api_codes/json_files/allRecipes.json', 'r', encoding='UTF-8') as json_read :
    all_recipes = json.load(json_read, object_pairs_hook=OrderedDict)

allRecipesList =[]
cnt = 0
for recipe in all_recipes:
    tempDict = {}

    recipe_base = recipe["base"]
    base_code = 999

    for base in all_bases:
        if recipe_base in base["types"]:
            base_code = base["code"] + base["types"].index(recipe_base)
            cnt += 1

    tempDict["english_name"] = recipe["english_name"]
    tempDict["korean_name"] = recipe["korean_name"]
    tempDict["code"] = base_code
    tempDict["base"] = recipe_base
    tempDict["ingredients"] = recipe["ingredients"]
    tempDict["instructions"] = recipe["instructions"]

    allRecipesList.append(tempDict)

print(cnt, len(allRecipesList))



with open('api_codes/json_files/recipes.json', 'w', encoding='utf-8') as f:
    json.dump(allRecipesList, f, ensure_ascii = False, indent=4)


print('\nfile successfully created!\n')