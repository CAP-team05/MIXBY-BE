from bs4 import BeautifulSoup
import requests, pprint

def searchtypeKOR(name):
    name = name.replace(' ', '+')
    url = "https://www.google.com/search?q="+name+"+\'종류\'+site:dailyshot.co"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    txt_list = soup.text.split('종류.')

    if len(txt_list) > 1:
        return (txt_list[1].split(';')[0].strip(' '))
    else: return ('none')
