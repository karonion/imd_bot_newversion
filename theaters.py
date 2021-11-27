import requests
from bs4 import BeautifulSoup
import datetime
import re

current_date = datetime.date.today().strftime('%d %m')
cd = current_date
url = f'https://multiplex.ua/ru/cinema/kyiv/respublika#{cd[0:2]}{cd[3:5]}2021'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
films = soup.find_all('div', class_='film')
title_list = []  # промежуточный список для названий
image_list = []  # промежуточный список для изображений
cinema_dict = {}  # словарь для конечного списка
pattern = '\/images\/\w*/\w*/\w*.jpeg'  # Регулярка для поиска изображений


def get_current_cinemas():
    global cinema_dict
    for i in soup.select('div.film a'):
        a = re.findall(pattern, str(i))
        if i['title'] not in title_list and len(a) > 0:
            title_list.append(i['title'])
            image_list.append(a[0])
    cinema_dict = dict(zip(title_list, image_list))
    return cinema_dict


