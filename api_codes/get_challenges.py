from collections import OrderedDict
import json

with open('api_codes/json_files/allChallenges.json', 'r', encoding='UTF-8') as json_read :
    all_challenges = json.load(json_read, object_pairs_hook=OrderedDict)
