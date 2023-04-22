import telebot
from telebot import types
import config
import deezer
import json
import requests

client = deezer.Client(app_id='598904', app_secret='2a8c1faffcb9590bf1c67a51712f447b')
bot = telebot.TeleBot(config.Token)

#Кнопки для начала работы с ботом и создания главного меню.
@bot.message_handler(commands = ["start"])
def start(message):
   markup = types.ReplyKeyboardMarkup(resize_keyboard= True)
   Hello = types.KeyboardButton('🔊 Что ты такое?')
   Find = types.KeyboardButton('🎧 Найти песню или трек')
   Help = types.KeyboardButton('💬 Помощь')
   Information = types.KeyboardButton('📃 Информация')
   markup.add(Hello, Find, Help, Information)


   bot.send_message(message.chat.id, 'Привет, {0.first_name}'.format(message.from_user), reply_markup = markup)

#Кнопки для раздела помощь.
@bot.message_handler(commands = ['help'])
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    InfAb = types.KeyboardButton('💻 Информация обо мне')
    Write = types.KeyboardButton('🔧 Баг репорт')
    Back = types.KeyboardButton('⬅ Назад')
    markup.add(InfAb, Write, Back)


    bot.send_message(message.chat.id, 'Здесь Вы можете узнать всю информацию и если что, написать разработчику', reply_markup=markup)

#Кнопки для реализации поиска песен и треков.
@bot.message_handler(commands = ['find'])
def find(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    FindMus = types.KeyboardButton(' Найти песню по названию')
    RecordMus = types.KeyboardButton(' Ну если не по названию, хоть звук запишем, тыкай на микрофон')
    Back = types.KeyboardButton('⬅ Назад')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add(FindMus, RecordMus, Back)


    bot.send_message(message.chat.id, 'Меню:', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Найти песню по названию')
def find_music_by_name(message):
    bot.send_message(message.chat.id, 'Введите название песни, которую хотите найти:')
    bot.register_next_step_handler(message, search_music_by_name)

def search_music_by_name(message):
    song_name = message.text
    response = requests.get(f'https://api.deezer.com/search?q={song_name}&limit=1')
    data = response.json()
    if 'data' in data:
        track = data['data'][0]
        artist = track['artist']['name']
        title = track['title']
        audio_url = track['preview']
        bot.send_message(message.chat.id, f'Нашел песню "{title}" исполнителя {artist}. Отправляю...')
        bot.send_audio(message.chat.id, audio=audio_url)
    else:
        bot.send_message(message.chat.id, 'По вашему запросу ничего не найдено')

#Кнопки для получения инфорации.
@bot.message_handler(commands = ['information'])
def informationbot(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    Inf = types.KeyboardButton('💻 Информация о разработке и будущих обновлениях')
    PatchNote = types.KeyboardButton('📝 Патч нот обновлений бота')
    Back = types.KeyboardButton('⬅ Назад')
    markup.add(Inf, PatchNote, Back)


    bot.send_message(message.chat.id, 'Информация о боте и обновлениях: ', reply_markup=markup)

#Оформление связи с разработчиком.
@bot.message_handler(commands = ['contact'])
def contact(message):
    markup = types.InlineKeyboardMarkup()
    buttoncont = types.InlineKeyboardButton('Оформи баг репорт:', url='https://t.me/HellCuteCorgi')
    markup.add(buttoncont)


    bot.send_message(message.chat.id,'Тыкай сюда и расскажи о проблемах)'.format(message.from_user), reply_markup=markup)

@bot.message_handler(command = ['patchnote'])
def patchnote(message):
    bot.send_message(message.chat.id, 'Version 1.1 \n - Добавлен поиск песен по названию')

#Реализация работы кнопок, ответов.
@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '🔊 Что ты такое?':
            bot.send_message(message.chat.id, 'Кожанный, я просто машина для поиска песен. \n Ты мне название - я тебе результат, но в благародство играть не стану, найду тебе пару песен и иди своей дорогой)')
        elif message.text == '🎧 Найти песню или трек':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                FindMus = types.KeyboardButton(' Найти песню по названию')
                RecordMus = types.KeyboardButton(' Ну если не по названию, хоть звук запишем, тыкай на микрофон')
                Back = types.KeyboardButton('⬅ Назад')
                markup.add(FindMus, RecordMus, Back)


                bot.send_message(message.chat.id, 'Меню:', reply_markup=markup)

        elif message.text == '💬 Помощь':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                InfAb = types.KeyboardButton('💻 Информация обо мне')
                Write = types.KeyboardButton('🔧 Баг репорт')
                Back = types.KeyboardButton('⬅ Назад')
                markup.add(InfAb, Write, Back)


                bot.send_message(message.chat.id, 'Здесь Вы можете узнать всю информацию', reply_markup=markup)

        elif message.text == '📃 Информация':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                Inf = types.KeyboardButton('💻 Информация о разработке и будущих обновлениях')
                PatchNote = types.KeyboardButton('📝 Патч ноут обновлений бота')
                Back = types.KeyboardButton('⬅ Назад')
                markup.add(Inf, PatchNote, Back)


                bot.send_message(message.chat.id, 'Информация о боте и обновлениях: ', reply_markup=markup)

        elif message.text == '⬅ Назад':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                Hello = types.KeyboardButton('🔊 Что ты такое?')
                Find = types.KeyboardButton('🎧 Найти песню или трек')
                Help = types.KeyboardButton('💬 Помощь')
                Information = types.KeyboardButton('📃 Информация')
                markup.add(Hello, Find, Help, Information)


                bot.send_message(message.chat.id, 'Главное меню', reply_markup=markup)

        elif message.text == '💻 Информация обо мне':
                bot.send_message(message.chat.id, text = 'Я просто машина, ищу песенки и в будущем буду присылать мемы с котиками). \nМеня создал чел с ником @HellCuteCorgi как свой первый оконченный проект, надеюсь. \nДата создания: 02.12.2022, а дата задумки вообще тьма. \nБуду рад с тобой познакомиться и сотрудничать в плане развития своего плейлиста)')

        elif message.text == '🔧 Баг репорт':
            markup = types.InlineKeyboardMarkup()
            buttoncont = types.InlineKeyboardButton('Оформи баг репорт:', url='https://t.me/HellCuteCorgi')
            markup.add(buttoncont)


            bot.send_message(message.chat.id, 'Тыкай сюда и расскажи о проблемах)'.format(message.from_user), reply_markup=markup)

        elif message.text == '💻 Информация о разработке и будущих обновлениях':
            bot.send_message(message.chat.id, 'Version 1.1 \n - Дата создания бота: 02.12.2022 \n - Разработчик: @HellCuteCorgi \n - Основное предназначение: Помощь пользователям в поиске песен и треков, используя их названия \n - Анонс будущей версии: \n 1. В будущем будет добавлена возможность поиска песен при помощи записи через микрофон. \n 2. Также бот будет присылать гифки и фоточки котиков из интернета по нажатию кнопки. \n 3. И последнее поиск музыки на вики по названию')

        elif message.text == '📝 Патч нот обновлений бота':
            bot.send_message(message.chat.id, 'Version 1.1 \n - Добавлен поиск музыки по названию')

bot.polling(none_stop = True)