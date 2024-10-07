from bs4 import BeautifulSoup
import requests, json

nums = range(1000, 99999)

new_list = []

for num in nums:
    url = 'https://dailyshot.co/m/item/'+str(num)
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    txt = soup.text

    if txt != '':
        try:
            name = txt.split('전국')[0].strip(' ')
            txt = txt.split('Information')[1].split('%')[0]
            tp = txt.split('종류')[1].split('용량')[0]
            vol = txt.split('용량')[1].split('도수')[0]
            al = txt.split('도수')[1]
            
            for liq in ['위스키', '보드카', '데킬라', '리큐르', '럼', '진']:
                if liq in tp:
                    new_dict = {}
                    new_dict['name'] = name
                    new_dict['type'] = tp
                    new_dict['volume'] = vol
                    new_dict['alcohol'] = al
                    new_list.append(new_dict)
                print("added!")
        except: print("not added")
    print()

with open('new_data/drinks_copy.json', 'w', encoding='utf-8') as f:
    json.dump(new_list, f, ensure_ascii = False, indent=4)

print('\nfile successfully created!\n')