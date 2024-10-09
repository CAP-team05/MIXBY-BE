from my_modules import getinfo
import searchimage
import json

urls = getinfo.geturls('old_data/urls.txt')

drinks = []

cnt = 1
for url in urls:
    code = getinfo.getcode(url)
    name = getinfo.getnameKOR(url)
    volume = name.split('(')[-1]
    name = name.replace('('+volume, '').strip(' ')
    volume = volume.strip(' ').strip(')')

    al = searchimage.getalcohol(code)

    drink = {}
    drink['code'] = code
    drink['name'] = name
    drink['volume'] = volume
    drink['alcohol'] = al
    drinks.append(drink)

    print(cnt)
    cnt += 1

with open('new_data/drinks.json', 'w', encoding='utf-8') as f:
    json.dump(drinks, f, ensure_ascii = False, indent=4)

print('\nfile successfully created!\n')