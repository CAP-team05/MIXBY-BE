from collections import OrderedDict
import json

with open('backend_codes/new_data/drinks.json', 'r', encoding='UTF-8') as json_read :
    all_drinks = json.load(json_read, object_pairs_hook=OrderedDict)

with open('backend_codes/new_data/recipes.json', 'r', encoding='UTF-8') as json_read :
    all_recipes = json.load(json_read, object_pairs_hook=OrderedDict)


def getalldrinks():
    return all_drinks

def getallrecipes():
    return all_recipes

def getdrink(code):
    print(type(code), code)
    temp_list = []
    for j in all_drinks:
        if code == j["code"]: 
            if j not in temp_list: temp_list.append(j)
        if code in j["name"]: 
            if j not in temp_list: temp_list.append(j)
        if code in j["type"]: 
            if j not in temp_list: temp_list.append(j)
    temp_list.insert(0, "Total result : {}".format(len(temp_list)))
    return temp_list

def getrecipe(code):
    print(type(code), code)
    temp_list = []
    for j in all_recipes:
        if code == j["code"]: 
            if j not in temp_list: temp_list.append(j)
        if code in j["name"]: 
            if j not in temp_list: temp_list.append(j)
        if code in j["technique"]: 
            if j not in temp_list: temp_list.append(j)
        if code in j["base"]: 
            if j not in temp_list: temp_list.append(j)
        for i in j["ingredients"]: 
            if code in i: 
                if j not in temp_list: temp_list.append(j)
    temp_list.insert(0, "Total result : {}".format(len(temp_list)))
    return temp_list