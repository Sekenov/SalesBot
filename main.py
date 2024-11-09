import telebot
from telebot import types

# Создаем экземпляр бота
bot = telebot.TeleBot('8077962203:AAHHndkIuMJz__r2nOimrh2CGG8vS8OLCDo')

# Словарь для хранения данных пользователей
user_data = {}


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Создаем кнопку "Start"
    markup = types.InlineKeyboardMarkup()
    btn_start = types.InlineKeyboardButton("Start", callback_data="start")
    markup.add(btn_start)

    # Отправляем приветственное сообщение с кнопкой "Start"
    bot.send_message(message.chat.id,
                     "Привет! Я бот, который поможет вам выбрать курс и оформить оплату. Нажмите 'Start', чтобы начать.",
                     reply_markup=markup)


# Обработчик нажатия на кнопку "Start"
@bot.callback_query_handler(func=lambda call: call.data == "start")
def handle_start(call):
    # Приветствие и вопрос о стране
    markup = types.InlineKeyboardMarkup()
    btn_kz = types.InlineKeyboardButton("Казахстан", callback_data="country_kz")
    btn_ru = types.InlineKeyboardButton("Россия", callback_data="country_ru")
    btn_az = types.InlineKeyboardButton("Азербайджан", callback_data="country_az")
    markup.add(btn_kz, btn_ru, btn_az)

    bot.send_message(call.message.chat.id,
                     "Из какой вы страны? Это нужно, чтобы показать цену курса в вашей валюте.",
                     reply_markup=markup)


# Обработчик выбора страны
@bot.callback_query_handler(func=lambda call: call.data.startswith("country_"))
def handle_country(call):
    country_code = call.data.split("_")[1]
    countries = {"kz": "Казахстан", "ru": "Россия", "az": "Азербайджан"}
    country = countries.get(country_code, "Казахстан")

    # Сохраняем страну пользователя
    user_data[call.message.chat.id] = {"country": country}

    # Отправляем сообщение с информацией и кнопками "Вопросы" и "Перейти к курсам"
    markup = types.InlineKeyboardMarkup()
    btn_questions = types.InlineKeyboardButton("Вопросы", callback_data="questions")
    btn_courses = types.InlineKeyboardButton("Перейти к курсам", callback_data="courses")
    markup.add(btn_questions, btn_courses)

    bot.send_message(call.message.chat.id,
                     f"Отлично, вы выбрали {country}. Если у вас есть вопросы, нажмите кнопку 'Вопросы'. Либо можете перейти к выбору курсов.",
                     reply_markup=markup)


# Обработчик кнопки "Вопросы"
@bot.callback_query_handler(func=lambda call: call.data == "questions")
def questions(call):
    # Создаем Inline кнопки с вопросами
    markup = types.InlineKeyboardMarkup()
    btn_q1 = types.InlineKeyboardButton("Точно ли вы скинете курс после оплаты?", callback_data="question_1")
    btn_q2 = types.InlineKeyboardButton("Как долго длится курс?", callback_data="question_2")
    btn_q3 = types.InlineKeyboardButton("Есть ли поддержка после покупки?", callback_data="question_3")
    btn_q4 = types.InlineKeyboardButton("Можно ли вернуть деньги?", callback_data="question_4")
    btn_q5 = types.InlineKeyboardButton("Какие материалы я получу?", callback_data="question_5")
    markup.add(btn_q1, btn_q2, btn_q3, btn_q4, btn_q5)

    bot.send_message(call.message.chat.id, "Выберите ваш вопрос:", reply_markup=markup)


# Обработчик ответов на вопросы
@bot.callback_query_handler(func=lambda call: call.data.startswith("question_"))
def handle_questions(call):
    answers = {
        "question_1": "Да, сразу после оплаты вы получите доступ к курсу.",
        "question_2": "Курс длится 4 недели, включая все необходимые материалы и задания.",
        "question_3": "Да, мы предоставляем поддержку в течение 3 месяцев после покупки.",
        "question_4": "Да, вы можете вернуть деньги в течение 7 дней после покупки, если курс вам не подошел.",
        "question_5": "Вы получите видеоуроки, PDF-материалы и доступ к сообществу."
    }
    bot.send_message(call.message.chat.id, answers[call.data])


# Обработчик нажатия на "Перейти к курсам"
@bot.callback_query_handler(func=lambda call: call.data == "courses")
def handle_courses(call):
    # Отправляем список курсов
    markup = types.InlineKeyboardMarkup()
    btn_ds = types.InlineKeyboardButton("Data Science", callback_data="course_ds")
    btn_da = types.InlineKeyboardButton("Data Analytics", callback_data="course_da")
    markup.add(btn_ds, btn_da)

    bot.send_message(call.message.chat.id, "Выберите курс:", reply_markup=markup)


# Обработчик выбора курса
@bot.callback_query_handler(func=lambda call: call.data.startswith("course_"))
def handle_selected_course(call):
    course_code = call.data.split("_")[1]
    courses = {"ds": "Data Science", "da": "Data Analytics"}
    course = courses.get(course_code, "Data Science")

    # Отправляем фото и видео о курсе
    if course == "Data Science":
        bot.send_photo(call.message.chat.id, open("Resources/dataSciencePhoto.jpeg", 'rb'))
        bot.send_video(call.message.chat.id, open("Resources/videoDataScience.mp4", 'rb'))
    elif course == "Data Analytics":
        bot.send_photo(call.message.chat.id, open("Resources/dataAnalysticsPhoto.jpeg", 'rb'))
        bot.send_video(call.message.chat.id, open("Resources/videoDataAnalystics.mp4", 'rb'))

    bot.send_message(call.message.chat.id, f"Вы выбрали курс {course}. Вот немного информации о курсе.")

    # Кнопка "Оплатить"
    markup = types.InlineKeyboardMarkup()
    btn_pay = types.InlineKeyboardButton("Оплатить", callback_data="pay")
    markup.add(btn_pay)
    bot.send_message(call.message.chat.id, "Если хотите купить этот курс, нажмите 'Оплатить'.", reply_markup=markup)


# Обработчик нажатия на "Оплатить"
@bot.callback_query_handler(func=lambda call: call.data == "pay")
def handle_payment(call):
    # Получение страны пользователя
    country = user_data.get(call.message.chat.id, {}).get("country", "Казахстан")

    # В зависимости от страны показываем цену
    if country == "Казахстан":
        price = "20,000 тг"
    elif country == "Россия":
        price = "3900 рублей"
    elif country == "Азербайджан":
        price = "68 манат"
    else:
        price = "20,000 тг"  # Значение по умолчанию

    bot.send_message(call.message.chat.id, f"Стоимость курса: {price}. Курс был оплачен. Спасибо!")


# Запуск бота
bot.polling(none_stop=True)
