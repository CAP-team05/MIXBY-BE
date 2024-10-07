import requests
from bs4 import BeautifulSoup

def geturls(filename):
    urls = []
    f = open(filename, 'r')
    urls = f.readlines()
    return urls

def getcode(url):
    url = url.split('LM')[1]
    code = url.split('?')[0]
    return code

def getbrand(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    line = soup.text.split('\n')[10]
    brand = line.split(']')[0].strip('[]')
    return brand

def getnameKOR(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    line = soup.text.split('\n')[10]
    if ']' in line:
        line = line.split(']')[1]
    name = line.split(':')[0].strip(' ')
    size = name.split('(')[-1]
    name = name.replace(size, '')
    for _ in (0, name.count('(')):
        name = name.replace('(', '')
        name = name.replace(')', '')
    size = size.replace(',', '')
    name = name + '(' + size
    return name

def getimageurl(url):
    response = requests.get(url)
    html = response.text
    spl = html.split('src=')
    links = []
    for i in range(5, len(spl)):
        n = spl[i].split('\"')[1]
        links.append(n)
    
    return links

def getpageurl(code):
    full_code = code
    num = []
    for _ in range(0,6):
        num.append(code[:2])
        code = code[2:]
    num.append(code[0])

    url = 'https://red.lotteon.com/goodsdetail?view=type1-raw&model=itemdetail%2FLM'
    for n in num:
        url = url+'%2F'+n
    url = url+'%2FDSCRP_LM'+full_code
    return url
    
def searchnameENG(code):
    url = "https://www.google.com/search?q=product+"+code
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    name = soup.text
    try:
        name = name.split('결과완전일치')[1]
        for p in ['-','|']:
            if p in name:
                name = name.split(p)[0]
                if '.' in name:
                    name = name.split('.')[-1]
        name = name.strip(' ')
    except: name = None
    return name