import json, csv

lines = []
f = open('origin_data\\recipes.csv', 'rt', encoding='UTF8')
lines = csv.reader(f)

recipes = []
bb= []
code = 0

for line in lines:    
    i = line[1]
    i = i.split(',')
    ings = []
    for x in i:
        ings.append(x.strip(' '))

    for ing in ings:
        if 'or' in ing:
            for _ in range(0, ing.count('or')):
                ing = ing.split('or')[0].strip(' ')+' or '+ing.split('or')[1].strip(' ')
        if '스카치 위스키' in ing and '혼합' != line[3]:
            line[3] = '스카치 위스키'
            
    bs = []
    if 'or' in line[3]:
        for i in range(0, line[3].count('or')):
            bs.append(line[3].split('or')[i].strip(' '))
        line[3] = line[3].split('or')[0].strip(' ')+' or '+line[3].split('or')[1].strip(' ')
    else:
        if line[3] != '': bs.append(line[3].strip(' '))
    for b in bs:
        if b not in bb: bb.append(b)
    
    recipe = {}
    recipe['code'] = code
    recipe['name'] = line[0]
    recipe['technique'] = line[2]
    recipe['base'] = line[3]
    recipe['ingredients'] = ings

    recipes.append(recipe)

def liquorclasses(bb):
    base = {}
    gin = []
    rum = []
    teq = []
    whi = []
    vod = []
    bra = []
    liq = []
    gui = []
    for b in bb:
        if '진' in b:
            gin.append(b)
        elif '럼' in b:
            rum.append(b)
        elif '테킬라' in b:
            teq.append(b)
        elif '위스키' in b:
            whi.append(b)
        elif '보드카' in b:
            vod.append(b)
        elif '브랜디' in b:
            bra.append(b)
        elif '리큐르' in b:
            liq.append(b)
        else:
            gui.append(b)
            
    base['진'] = sorted(gin)
    base['럼'] = sorted(rum)
    base['테킬라'] = sorted(teq)
    base['위스키'] = sorted(whi)
    base['보드카'] = sorted(vod)
    base['브랜디'] = sorted(bra)
    base['리큐르'] = sorted(liq)
    base['기타'] = sorted(gui)

    return base

with open('new_data\\recipes.json', 'w', encoding='utf-8') as f:
    json.dump(recipes, f, ensure_ascii = False, indent=4)

with open('new_data\\bases.json', 'w', encoding='utf-8') as f:
    json.dump(liquorclasses(bb), f, ensure_ascii = False, indent=4)

print('\nfile successfully created!\n')