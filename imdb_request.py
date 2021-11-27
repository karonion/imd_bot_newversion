import requests

apikey = 'k_sdf9asjq'  # k_4te7tj19


def get_info(keyword):  # формируем данные
    dict_data = eval(requests.get(f'https://imdb-api.com/en/API/Keyword/k_4te7tj19/{keyword.lower()}').text)
    return dict_data


def get_movie_info(dict_data):  # Получаем данные из json
    ls = list()
    global dict_len
    if len(dict_data['items']) >= 6:
        dict_len = len(dict_data['items']) - 5
    else:
        return ls
    for i in range(len(dict_data['items'])):
        if dict_data['items'][i]['imDbRating'] == '-':  # Если рейтинг фильма не сформирован - следующая итерация
            continue
        elif dict_data['items'][i]['imDbRating'] == '0':
            continue
        title = dict_data['items'][i]['title']
        year = dict_data['items'][i]['year']
        image = dict_data['items'][i]['image']
        rating = dict_data['items'][i]['imDbRating']
        x = title, year, rating, image  # сохраняем данные, которые будем передавать
        ls.append(x)  # Сохранение итога каждой итерации в список
    ls = sorted(ls, key=lambda movie: movie[2], reverse=True)  # сортировка локального списка по рейтингу
    return ls


def first_request(keyword):  # Формируем запрос ключевым словом
    dict_data = get_info(keyword)
    data = get_movie_info(dict_data)
    textlist = []
    for i in list(data):
        textlist.append(list(i))
    return textlist

