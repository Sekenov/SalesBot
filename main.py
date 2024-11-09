import telebot
from telebot import types

# Создаем экземпляр бота
bot = telebot.TeleBot('8077962203:AAHHndkIuMJz__r2nOimrh2CGG8vS8OLCDo')

# Словарь для хранения данных пользователей
user_data = {}


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Создаем кнопки для выбора
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_start = types.KeyboardButton("Start")
    markup.add(btn_start)

    # Отправляем приветственное сообщение с кнопкой "Start"
    bot.send_message(message.chat.id,
                     "Привет! Я бот, который поможет вам выбрать курс и оформить оплату. Нажмите 'Start', чтобы начать.",
                     reply_markup=markup)


# Обработчик нажатия на кнопку "Start"
@bot.message_handler(func=lambda message: message.text == "Start")
def handle_start(message):
    # Приветствие и вопрос о стране
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_kz = types.KeyboardButton("Казахстан")
    btn_ru = types.KeyboardButton("Россия")
    btn_az = types.KeyboardButton("Азербайджан")
    markup.add(btn_kz, btn_ru, btn_az)

    bot.send_message(message.chat.id,
                     "Из какой вы страны? Это нужно, чтобы показать цену курса в вашей валюте.",
                     reply_markup=markup)


# Обработчик выбора страны
@bot.message_handler(func=lambda message: message.text in ["Казахстан", "Россия", "Азербайджан"])
def handle_country(message):
    country = message.text

    # Сохраняем страну пользователя
    user_data[message.chat.id] = {"country": country}

    # Отправляем сообщение с информацией и кнопками "Вопросы" и "Перейти к курсам"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_questions = types.KeyboardButton("Вопросы")
    btn_courses = types.KeyboardButton("Перейти к курсам")
    markup.add(btn_questions, btn_courses)

    bot.send_message(message.chat.id,
                     f"Отлично, вы выбрали {country}. Если у вас есть вопросы, нажмите кнопку 'Вопросы'. Либо можете перейти к выбору курсов.",
                     reply_markup=markup)


# Обработчик кнопки "Вопросы"
@bot.message_handler(func=lambda message: message.text == "Вопросы")
def questions(message):
    # Создаем кнопки с вопросами
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_q1 = types.KeyboardButton("Точно ли вы скинете курс после оплаты?")
    btn_q2 = types.KeyboardButton("Как долго длится курс?")
    btn_q3 = types.KeyboardButton("Есть ли поддержка после покупки?")
    btn_q4 = types.KeyboardButton("Можно ли вернуть деньги?")
    btn_q5 = types.KeyboardButton("Какие материалы я получу?")
    btn_courses = types.KeyboardButton("Перейти к курсам")
    markup.add(btn_q1, btn_q2, btn_q3, btn_q4, btn_q5, btn_courses)

    bot.send_message(message.chat.id, "Выберите ваш вопрос:", reply_markup=markup)


# Обработчик ответов на вопросы
@bot.message_handler(func=lambda message: message.text in [
    "Точно ли вы скинете курс после оплаты?",
    "Как долго длится курс?",
    "Есть ли поддержка после покупки?",
    "Можно ли вернуть деньги?",
    "Какие материалы я получу?"
])
def handle_questions(message):
    answers = {
        "Точно ли вы скинете курс после оплаты?": "Да, сразу после оплаты вы получите доступ к курсу.",
        "Как долго длится курс?": "Курс длится 4 недели, включая все необходимые материалы и задания.",
        "Есть ли поддержка после покупки?": "Да, мы предоставляем поддержку в течение 3 месяцев после покупки.",
        "Можно ли вернуть деньги?": "Да, вы можете вернуть деньги в течение 7 дней после покупки, если курс вам не подошел.",
        "Какие материалы я получу?": "Вы получите видеоуроки, PDF-материалы и доступ к сообществу.",
    }
    bot.send_message(message.chat.id, answers[message.text])


# Обработчик нажатия на "Перейти к курсам"
@bot.message_handler(func=lambda message: message.text == "Перейти к курсам")
def handle_courses(message):
    # Отправляем список курсов
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_ds = types.KeyboardButton("Data Science")
    btn_da = types.KeyboardButton("Data Analytics")
    markup.add(btn_ds, btn_da)

    bot.send_message(message.chat.id, "Выберите курс:", reply_markup=markup)


# Обработчик выбора курса
@bot.message_handler(func=lambda message: message.text in ["Data Science", "Data Analytics"])
def handle_selected_course(message):
    course = message.text
    # Отправляем фото и видео о курсе
    if course == "Data Science":
        bot.send_photo(message.chat.id, open("Resources/dataSciencePhoto.jpeg", 'rb'))
        bot.send_video(message.chat.id, open("Resources/videoDataScience.mp4", 'rb'))
    elif course == "Data Analytics":
        bot.send_photo(message.chat.id, open("Resources/dataAnalysticsPhoto.jpeg", 'rb'))
        bot.send_video(message.chat.id, open("Resources/videoDataAnalystics.mp4", 'rb'))

    bot.send_message(message.chat.id, f"Вы выбрали курс {course}. Вот немного информации о курсе.")

    # Кнопка "Оплатить"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_pay = types.KeyboardButton("Оплатить")
    markup.add(btn_pay)
    bot.send_message(message.chat.id, "Если хотите купить этот курс, нажмите 'Оплатить'.", reply_markup=markup)


# Обработчик нажатия на "Оплатить"
@bot.message_handler(func=lambda message: message.text == "Оплатить")
def handle_payment(message):
    # Получение страны пользователя
    country = user_data.get(message.chat.id, {}).get("country", "Казахстан")

    # В зависимости от страны показываем цену
    if country == "Казахстан":
        price = "20,000 тг"
    elif country == "Россия":
        price = "3900 рублей"
    elif country == "Азербайджан":
        price = "68 манат"
    else:
        price = "20,000 тг"  # Значение по умолчанию

    bot.send_message(message.chat.id, f"Стоимость курса: {price}. Курс был оплачен. Спасибо!")


# Запуск бота
bot.polling(none_stop=True)