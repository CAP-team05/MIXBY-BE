from collections import OrderedDict
import json

with open('datas/recipes.json', 'r', encoding='UTF-8') as json_read :
    all_recipes = json.load(json_read, object_pairs_hook=OrderedDict)


def getallrecipes():
    return all_recipes

def getrecipe_byname(name):
    temp_list = []
    for j in all_recipes:
        if name in j["name"] and j not in temp_list: temp_list.append(j)
    temp_list.insert(0, "Total result : {}".format(len(temp_list)))
    return temp_list

def getrecipe_bycode(code):
    temp_list = []
    for j in all_recipes:
        if code == j["code"] and j not in temp_list: temp_list.append(j)
    temp_list.insert(0, "Total result : {}".format(len(temp_list)))
    return temp_list

def getrecipe_byings(ing):
    temp_list = []
    for j in all_recipes:
        for i in j["ingredients"]: 
            if ing in i and j not in temp_list: temp_list.append(j)
    temp_list.insert(0, "Total result : {}".format(len(temp_list)))
    return temp_list