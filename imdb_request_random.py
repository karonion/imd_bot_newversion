import requests
import random

apikey = 'k_4te7tj19'  # 'k_sdf9asjq'


def get_info():  # формируем данные
    dict_data = eval(requests.get(
        f'https://imdb-api.com/en/API/Top250Movies/k_4te7tj19').text)  # Преобразование в словарь
    return dict_data


def get_movie_info(dict_data):  # Получаем данные из json
    randominteger = random.randint(1, 250)
    r = randominteger  # Сокращение
    title = dict_data['items'][r]['title']
    year = dict_data['items'][r]['year']
    rating = dict_data['items'][r]['imDbRating']
    rank = dict_data['items'][r]['rank']
    id = dict_data['items'][r]['id']
    image = find_poster(id)
    return title, year, rating, rank, image

def find_poster(id):  # Поиск фото с нормальным разрешением. По дефолту из топа выгружаются фото +- 150Х150.
    data_posters = eval(requests.get(
        f'https://imdb-api.com/en/API/Posters/k_4te7tj19/{id}').text)
    first_poster = data_posters['posters'][0]['link']
    return first_poster



def first_request():  # Формируем запрос ключевым словом
    dict_data = get_info()
    data = get_movie_info(dict_data)
    return data

