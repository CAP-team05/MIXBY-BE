from my_modules import gettype
import cv2, pytesseract, json

# json file 읽기
with open('new_data/drinks.json', 'r', encoding='UTF-8') as json_read :
    json_str = json.load(json_read)

new_list = []
cnt = 0
for j in json_str[:10]:
    code = j['code']
    f = "images_merged/"+code+"_merged.jpg"
    image = cv2.imread(f)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lines = pytesseract.image_to_string(rgb_image, lang='kor', config='--psm 6')
    lines = lines.split('\n')

    cnt += 1
    #print(cnt)

    c = j['code']
    n = j['name']
    v = j['volume']
    a = j['alcohol']
    t = gettype.searchtypeKOR(n)

    print(cnt, n)
    print(t)
    print()

    new_dict = {}
    new_dict['code'] = c
    new_dict['name'] = n
    new_dict['type'] = t
    new_dict['volume'] = v
    new_dict['alcohol'] = a
    
    new_list.append(new_dict)


# with open('new_data/drinks_copy.json', 'w', encoding='utf-8') as f:
#     json.dump(new_list, f, ensure_ascii = False, indent=4)

# print('\nfile successfully created!\n')