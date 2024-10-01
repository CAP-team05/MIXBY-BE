import requests, pprint
from bs4 import BeautifulSoup
import getname

codes = ["0085246500576", "0082184090442", "5000267024400", "5029704111442", "5010106113127", "5010196092142", "0080244009236"]
#codes = ["0085246500576", "0082184090442", "5000267024400"]

def strip_name(name):
    x = name.find('(')
    if x != -1: name = name[0:x]
    name = name.strip(' ')
    name = name.replace(" ","+")
    name = name.replace("\'","")
    name = name.strip('.')
    return name

def get_nutracheck(name):
    url = "https://www.google.com/search?q=nutracheck+calories+per+oz+in+"+strip_name(name)
    #print(url)
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        res = soup.text
        #res = res.split('Nutracheck')
        res = res.split('Energy:')
        if len(res) >= 3: i=len(res)-1
        else: i=1
        res = int(res[i].split('calories')[0].strip(' '))
        res = int(res)#*3.3814
    except:
        res = -1
    return int(res)

def get_eatthismuch(name):
    url = "https://www.google.com/search?q=eatthismuch+calories+per+shot+in+"+strip_name(name)
    #print(url)
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        res = soup.text
        res = res.split('There are ')[1]
        res = res.split(' of')[0]
        cal = int(res.split('calories')[0].strip(' '))
        shot = res.split('(')[1].strip(')')

        if 'oz' in shot:
            num = float(shot.split(' ')[0])
            cal = cal*3.3814/num
        elif 'ml' in shot:
            num = float(shot.split(' ')[0])
            cal = cal*100/num
        else: cal = -1
    except: cal = -1

    return int(cal)

def get_fatsecret(name):
    url = "https://www.google.com/search?q=fatsecret+calories+per+oz+in+"+strip_name(name)
    #print(url)
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        res = soup.text
        res = res.split('There are ')[1]
        res = res.split(' of')[0]
        cal = int(res.split('calories')[0].strip(' '))
        shot = res.split('(')[1].strip(')')

        if 'oz' in shot:
            num = float(shot.split(' ')[0])
            cal = cal*3.3814/num
        elif 'ml' in shot:
            num = float(shot.split(' ')[0])
            cal = cal*100/num
        else: cal = -1
    except: cal = -1

    return int(cal)

def get_calorieking(name):
    url = "https://www.google.com/search?q=calorieking+calories+per+oz+in+"+strip_name(name)
    #print(url)
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    try:
        res = soup.text
        res = res.split('There are ')[1]
        res = res.split(' of')[0]
        cal = int(res.split('calories')[0].strip(' '))
        shot = res.split('(')[1].strip(')')

        if 'oz' in shot:
            num = float(shot.split(' ')[0])
            cal = cal*3.3814/num
        elif 'ml' in shot:
            num = float(shot.split(' ')[0])
            cal = cal*100/num
        else: cal = -1
    except: cal = -1

    return int(cal)


def get_calorie(name):
    a = get_nutracheck(name)
    b = get_eatthismuch(name)
    c = get_fatsecret(name)
    d = get_calorieking(name)

    total = 4
    cals =  [a, b, c, d]
    cnt = total - cals.count(-1)
    avg = sum(cals)/cnt
    n = 0
    for i in cals:
        if i != -1:
            x = i/avg*100
            if 90.0 <= x and x <= 110.0:
                n += 1
            #print(x,n)
    return int(avg)


for code in codes:
    name = getname.getProductName(code)
    cal = get_calorie(name)
    print()
    print(name, cal)
    print()