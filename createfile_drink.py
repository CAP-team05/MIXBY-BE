import my_modules.getinfo, json

urls = my_modules.getinfo.geturls('old_data\\links.txt')
drinks = []

drinks = []

for url in urls:
    code = my_modules.getinfo.getcode(url)
    name = my_modules.getinfo.getnameKOR(url)
    volume = name.split('(')[-1]
    name = name.replace('('+volume, '').strip(' ')
    volume = volume.strip(' ').strip(')')

    drink = {}
    drink['code'] = code
    drink['name'] = name
    drink['volume'] = volume
    drinks.append(drink)

    print(len(code))

with open('new_data\\drinks.json', 'w', encoding='utf-8') as f:
    json.dump(drinks, f, ensure_ascii = False, indent=4)

print('\nfile successfully created!\n')