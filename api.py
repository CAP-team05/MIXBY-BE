import requests, pprint
from bs4 import BeautifulSoup

def getProduct1(code):
    """
    getProduct1 function work for crawling allproductkorea.or.kr

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
    getProduct2 function work for crawling koreannet.or.kr

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

def getProduct3(code):
    """
    getProduct3 function work for crawling google.com
    
    @param code: barcode 13-digit number
    @return: name of barcode's product return but if they did't find barcode then return None
    """
    url = "https://www.google.com/search?q=product+"+code
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    name = str(soup.select('h3')).split('>')[2].split('<')[0]

    splits = ['-','|']
    for s in splits:
        try:
            name = name.split(s)[0]
        except:
            name = name
    return name

def getProductName(code):
    """
    getProductName function find name of barcode by running all of getProductX functions

    @param code: barcode 13-digit number
    @return: name of barcode's product return but if they did't find barcode then return None
    """
    name = getProduct1(code)
    if name != None: return "from1: "+name
    '''
    name = getProduct2(code)
    if name != None: return "from2: "+name
    '''
    name = getProduct3(code)
    if name != None: return "from3: "+name

    return None


# barcode list for test inputs
barcodes = ["8801128900201", "0085246500576", "0082184090442", "5000267024400", "5029704111442", "5010106113127", "5010196092142"]

# here is just a test code
for code in barcodes:
    print(getProductName(code))