import requests, pprint
from bs4 import BeautifulSoup

barcodes = ["8801128900201", "085246500576", "0082184090442", "5000267024400", "5029704111442", "5010106113127", "5010196092142"]


def getProduct1(code):
    url = "https://www.allproductkorea.or.kr/products/info?q=%7B\"mainKeyword\":\"{}\",\"subKeyword\":\"\"%7D&page=1&size=10".format(code)
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    name = soup.text.split('\n')[206]
    if name == '      ': name = None
    return name

def getProduct2(code):
    url = "https://www.koreannet.or.kr/front/koreannet/gtinSrch.do"
    data = {}
    data['gtin'] = code
    response = requests.post(url, data=data)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    name = soup.text.split('\n')[226]
    if name == '': name = None
    return name

def getProductName(code):
    name = getProduct1(code)
    if name != None: return name
    name = getProduct2(code)
    if name != None: return name
    name = None

for code in barcodes:
    print(getProductName(code))