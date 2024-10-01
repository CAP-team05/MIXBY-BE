import requests, pprint
from bs4 import BeautifulSoup
import getname

#barcodes = ["8801128900201", "0085246500576", "0082184090442", "5000267024400", "5029704111442", "5010106113127", "5010196092142"]

code = "0080244009236"

name = getname.getProductName(code)

while name[-1]==" ":
    name = name[0:-2]
name = name.replace(" ","+")
url = "https://www.google.com/search?q=total+calories+in+"+name
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')
x = soup.text.split('calories')
print(x)