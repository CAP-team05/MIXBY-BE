import requests
from bs4 import BeautifulSoup

def getProduct1(code):
    """
    getProduct1 function work at crawling allproductkorea.or.kr

    @param code: barcode 13-digit number
    @return: name of barcode's product return but if they did't find barcode then return None
    """
    url = "https://www.allproductkorea.or.kr/products/info?q=%7B\"mainKeyword\":\"{}\",\"subKeyword\":\"\"%7D&page=1&size=10".format(code)
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    name = soup.text.split('\n')[206]
    if name == '      ': name = None
    return name

def getProduct2(code):
    """
    getProduct2 function work at crawling koreannet.or.kr

    @param code: barcode 13-digit number
    @return: name of barcode's product return but if they did't find barcode then return None
    """
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
    """
    getProductName function find name of barcode by running getProduct1 and 2 functions

    @param code: barcode 13-digit number
    @return: name of barcode's product return but if they did't find barcode then return None
    """
    name = getProduct1(code)
    if name != None: return name
    name = getProduct2(code)
    if name != None: return name
    name = None


# barcode list for test inputs
barcodes = ["8801128900201", "085246500576", "0082184090442", "5000267024400", "5029704111442", "5010106113127", "5010196092142"]

# here is just a test code
for code in barcodes:
    print(getProductName(code))