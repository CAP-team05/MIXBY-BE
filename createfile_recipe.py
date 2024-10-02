import json, csv

lines = []
f = open('origin_data\\recipes.csv', 'rt', encoding='UTF8')
lines = csv.reader(f)

recipes = []
bases = []

for line in lines:    
    i = line[1]
    i = i.split(',')
    ings = []
    for x in i:
        ings.append(x.strip(' '))

    recipe = {}
    recipe['name'] = line[0]
    recipe['technique'] = line[2]
    recipe['base'] = line[3]
    recipe['ingredients'] = ings

    # for i in range(0, len(ings)):
    #     recipe['ingredient{}'.format(i+1)] = (ings[i].replace(ings[i].split(' ')[-1],'')).strip(' ')
    # recipe['ingredient{}'.format(len(ings))] = str(None)

    # for i in range(0, len(ings)):
    #     recipe['measure{}'.format(i+1)] = ings[i].split(' ')[-1].strip(' ')
    # recipe['measure{}'.format(len(ings))] = str(None)
    
    if line[3] not in bases: bases.append(line[3])

    recipes.append(recipe)

with open('new_data\\recipes.json', 'w', encoding='utf-8') as f:
    json.dump(recipes, f, ensure_ascii = False, indent=4)

with open('new_data\\bases.json', 'w', encoding='utf-8') as f:
    json.dump(bases, f, ensure_ascii = False, indent=4)

print('\nfile successfully created!\n')