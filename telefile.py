import telebot
import imdb_request
import random
import imdb_request_random
import theaters
import datetime

bot = telebot.TeleBot('2087138924:AAG2HjUxV-CK2HpbMOAbOgdPw03A9p9MudE')
searching_buttons = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
searching_button_more = telebot.types.KeyboardButton(text='Еще 5')
theathers_button = telebot.types.KeyboardButton(text='Что идёт в кино?')
searching_button_again = telebot.types.KeyboardButton(text='Новая подборка фильмов')
random_film_button = telebot.types.KeyboardButton(text='Случайный фильм\сериал')
main_menu_button = telebot.types.KeyboardButton(text='Главное меню')
searching_buttons.add(searching_button_again, searching_button_more, main_menu_button)
hello_button = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
hello_button.add(searching_button_again, random_film_button, theathers_button)
cinema_message = ''  # костыль, не удалять


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(chat_id=message.from_user.id, text=f'Cделай выбор',
                     reply_markup=hello_button)


@bot.message_handler(commands=['stop'])
def stop(message):
    bot.send_message(chat_id=message.from_user.id, text='Ой всё')


@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == 'Новая подборка фильмов':  # К запросу подборки 5 фильмов
        msg = bot.send_message(message.chat.id, text='Напиши ключевое слово на английском языке',
                               reply_markup=searching_buttons)
        bot.register_next_step_handler(msg, cinema_finder)
    elif message.text == 'Еще 5':  # Для повторного вызова 5 фильмов
        cinema_finder(cinema_message)  # Костыль. Вкладываем первый результат работы функции в ту же функцию, что бы можно было использовать повторно. Предупреждение некорректное, string там будет после первого использования функции.
    elif message.text == 'Случайный фильм\сериал':
        random_film(message)
    elif message.text == 'Главное меню':
        start(message)
    elif message.text == 'Что идёт в кино?':
        find_in_theaters(message)

def find_in_theaters(message):
    a = theaters.get_current_cinemas()
    for key, value in reversed(a.items()):  # переворачиваем что бы внизу получить более популярные фильмы
        bot.send_photo(message.chat.id, photo=f'https://multiplex.ua/{value}', reply_markup=hello_button, caption=f'{key}')
    bot.send_message(message.chat.id, text=f'Данные актуальны на {datetime.date.today()}, расписание на ближайшие 7 дней. Кинотеатр Multiplex Respublika.')

def random_film(message):
    a = imdb_request_random.first_request()
    try:
        bot.send_photo(message.chat.id, photo=f'{a[4]}',
                       caption=f'{a[0]}, год {a[1]}, рейтинг imdb ⭐ {a[2]}, место в рейтинге {a[3]}',
                       reply_markup=hello_button)
    except:  # на случай если вес фото больше 10-ти мб
        b = imdb_request_random.first_request()  # Создаём новый запрос
        bot.send_photo(message.chat.id, photo=f'{b[4]}',
                       caption=f'{b[0]}, год {b[1]}, рейтинг imdb ⭐ {b[2]}, место в рейтинге {b[3]}',
                       reply_markup=hello_button)


def cinema_finder(message):
    global cinema_message  # костыль
    cinema_message = message
    if (message.text not in 'Новая подборка фильмов') and (message.text not in 'Еще 5') and (message.text not in 'Главное меню'):
        try:
            loc = imdb_request.first_request(message.text)  # вкладываем сообщение в запрос imdb
            if len(loc) > 10:  # проверка на длину списка с фильмами
                ri = random.randint(1, len(loc) - 5)  # минус 5 - запас для количества сообщений
                for i in range(0, 5):  # кол-во итераций = кол-во сообщений
                    try:  # пытаемся отправить настоящее фото
                        bot.send_photo(message.chat.id, photo=loc[ri + i][3])
                    except:  # если вес фото больше 10 мб отправляем фейк-постер
                        bot.send_photo(message.chat.id, photo='https://kinomaiak.ru/wp-content/uploads/2018/02/noposter-223x300.png')
                bot.send_message(message.chat.id,  # По оконачанию цикла отправки постеров - отправляем инфо о фильмах, одним сообщением
                                 text=f'1. - {loc[ri][0]}, {loc[ri][1]},⭐️ {loc[ri][2]},\n'
                                      f'2. - {loc[ri + 1][0]},  {loc[ri + 1][1]},⭐️ {loc[ri + 1][2]},\n'
                                      f'3. - {loc[ri + 2][0]},  {loc[ri + 2][1]},⭐️ {loc[ri + 2][2]},\n'
                                      f'4. - {loc[ri + 3][0]},  {loc[ri + 3][1]},⭐️ {loc[ri + 3][2]},\n'
                                      f'5. - {loc[ri + 4][0]},  {loc[ri + 4][1]},⭐️ {loc[ri + 4][2]},\n',
                                 reply_markup=searching_buttons)
            else:  # Если список слишком мал или пуст
                raise IndexError
        except IndexError:  # на случай если список пуст или мал, т.е. резульата поиска нет
            msg = bot.send_message(message.chat.id, text='Не удалось обработать запрос, попробуйте другое слово')
            bot.register_next_step_handler(msg, cinema_finder)  # запускаем работу функции по новой
    elif message.text in 'Главное меню':
        start(message)
    elif message.text in 'Еще 5':
        msg = bot.send_message(message.chat.id, text='Сначала введите слово для подборки!')
        bot.register_next_step_handler(msg, cinema_finder)
    elif message.text in 'Новая подборка фильмов':
        msg = bot.send_message(message.chat.id, text='Напиши ключевое слово на английском языке')
        bot.register_next_step_handler(msg, cinema_finder)
bot.polling(none_stop=True)
