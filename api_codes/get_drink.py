from collections import OrderedDict
import json

with open('datas/drinks.json', 'r', encoding='UTF-8') as json_read :
    all_drinks = json.load(json_read, object_pairs_hook=OrderedDict)


def getalldrinks():
    return all_drinks

def getdrink_byname(name):
    temp_list = []
    for j in all_drinks:
        if name in j["name"] and j not in temp_list: temp_list.append(j)
    temp_list.insert(0, "Total result : {}".format(len(temp_list)))
    return temp_list

def getdrink_bycode(code):
    temp_list = []
    for j in all_drinks:
        if code == j["code"] and j not in temp_list: temp_list.append(j)
    temp_list.insert(0, "Total result : {}".format(len(temp_list)))
    return temp_list
