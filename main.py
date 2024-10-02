import getcalories
import getinfo
import json

urls = getinfo.geturls('links.txt')
drinks = []
cnt = 0

for url in urls[0:50]:
    code = getinfo.getcode(url)
    nameKOR = getinfo.getnameKOR(url)
    nameENG = getinfo.searchnameENG(code)
    kcal = getcalories.getcalorie(nameENG)

    # if kcal != -1:
    #     amount = int(nameKOR.split('(')[-1].split(')')[0].strip('ml').strip('ML').replace(',',''))
    #     kcal = int(kcal*amount/100)

    drink = {}
    drink['code'] = code
    drink['kor name'] = nameKOR
    drink['eng name'] = nameENG
    drink['kcal per 100ml'] = str(kcal)+" kcal"
    drinks.append(drink)

    print(cnt)
    cnt += 1

with open('drinks.json', 'w') as f:
    json.dump(drinks, f, indent=4, ensure_ascii = False)

print('\nfile successfully created!\n')