import json

with open('data/drinks.json', 'r', encoding='UTF-8') as json_read :
    json_str = json.load(json_read)


def getall():
    return json_str

def getinfo(code):
    for j in json_str:
        if j["code"] == code:
            return j