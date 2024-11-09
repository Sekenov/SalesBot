import os
import requests
import telebot
from telebot import types
from urllib.parse import urlencode
import time

# Создаем экземпляр бота
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

# Словарь для хранения данных пользователей
user_data = {}

# PayPal API credentials
PAYPAL_API_USERNAME = os.getenv('PAYPAL_API_USERNAME')
PAYPAL_API_PASSWORD = os.getenv('PAYPAL_API_PASSWORD')
PAYPAL_API_SIGNATURE = os.getenv('PAYPAL_API_SIGNATURE')


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Создаем кнопку "Start"
    markup = types.InlineKeyboardMarkup()
    btn_start = types.InlineKeyboardButton("🚀 Start", callback_data="start")
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
    btn_kz = types.InlineKeyboardButton("🇰🇿 Казахстан", callback_data="country_kz")
    btn_ru = types.InlineKeyboardButton("🇷🇺 Россия", callback_data="country_ru")
    btn_az = types.InlineKeyboardButton("🇦🇿 Азербайджан", callback_data="country_az")
    markup.add(btn_kz, btn_ru, btn_az)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Из какой вы страны? Это нужно, чтобы показать цену курса в вашей валюте.",
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
    btn_questions = types.InlineKeyboardButton("❓ Вопросы", callback_data="questions")
    btn_courses = types.InlineKeyboardButton("📚 Перейти к курсам", callback_data="courses")
    markup.add(btn_questions, btn_courses)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"Отлично, вы выбрали {country}. Если у вас есть вопросы, нажмите кнопку 'Вопросы'. Либо можете перейти к выбору курсов.",
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
    btn_courses = types.InlineKeyboardButton("📚 Перейти к курсам", callback_data="courses")
    markup.add(btn_q1, btn_q2)
    markup.add(btn_q3, btn_q4)
    markup.add(btn_q5)
    markup.add(btn_courses)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Выберите ваш вопрос:", reply_markup=markup)

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

    # Добавляем кнопку "Перейти к курсам" после ответа на вопрос
    markup = types.InlineKeyboardMarkup()
    btn_courses = types.InlineKeyboardButton("📚 Перейти к курсам", callback_data="courses")
    markup.add(btn_courses)
    bot.send_message(call.message.chat.id, "Если хотите перейти к выбору курсов, нажмите кнопку ниже.",
                     reply_markup=markup)

# Обработчик нажатия на "Перейти к курсам"
@bot.callback_query_handler(func=lambda call: call.data == "courses")
def handle_courses(call):
    # Отправляем список курсов
    markup = types.InlineKeyboardMarkup()
    btn_ds = types.InlineKeyboardButton("🧪 Data Science", callback_data="course_ds")
    btn_da = types.InlineKeyboardButton("📊 Data Analytics", callback_data="course_da")
    markup.add(btn_ds, btn_da)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Выберите курс:", reply_markup=markup)

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

    # Добавляем небольшую задержку перед следующим сообщением для улучшения восприятия
    time.sleep(1)
    bot.send_message(call.message.chat.id, f"Вы выбрали курс {course}. Вот немного информации о курсе.")

    # Кнопка "Оплатить"
    markup = types.InlineKeyboardMarkup()
    btn_pay = types.InlineKeyboardButton("💳 Оплатить", callback_data="pay")
    markup.add(btn_pay)
    bot.send_message(call.message.chat.id, "Если хотите купить этот курс, нажмите 'Оплатить'.", reply_markup=markup)

# Обработчик нажатия на "Оплатить"
@bot.callback_query_handler(func=lambda call: call.data == "pay")
def handle_payment(call):
    # Получение страны пользователя
    country = user_data.get(call.message.chat.id, {}).get("country", "Казахстан")

    # В зависимости от страны показываем сумму в USD (так как PayPal работает с USD)
    if country == "Казахстан":
        amount = "20.00"
    elif country == "Россия":
        amount = "50.00"
    elif country == "Азербайджан":
        amount = "30.00"
    else:
        amount = "20.00"  # Значение по умолчанию

    # Проверка на наличие учетных данных PayPal
    if not all([PAYPAL_API_USERNAME, PAYPAL_API_PASSWORD, PAYPAL_API_SIGNATURE]):
        bot.send_message(call.message.chat.id, "Ошибка: учетные данные PayPal не найдены. Пожалуйста, проверьте настройки.")
        return

    # PayPal API URL для тестовой среды
    url = "https://api-3t.sandbox.paypal.com/nvp"

    # Параметры для создания платежного запроса
    params = {
        'USER': PAYPAL_API_USERNAME,
        'PWD': PAYPAL_API_PASSWORD,
        'SIGNATURE': PAYPAL_API_SIGNATURE,
        'METHOD': 'SetExpressCheckout',
        'VERSION': '204.0',
        'PAYMENTREQUEST_0_PAYMENTACTION': 'Sale',
        'PAYMENTREQUEST_0_AMT': amount,
        'PAYMENTREQUEST_0_CURRENCYCODE': 'USD',
        'RETURNURL': 'https://google.com',       # Замените на рабочую ссылку после успешной оплаты
        'CANCELURL': 'https://google.com',       # Замените на рабочую ссылку при отмене оплаты
    }

    # Выполняем POST-запрос к PayPal API
    response = requests.post(url, data=urlencode(params))

    # Обрабатываем ответ от PayPal
    if response.status_code == 200:
        response_data = dict(x.split('=') for x in response.text.split('&'))
        if response_data.get('ACK') == 'Success':
            token = response_data.get('TOKEN')
            payment_url = f"https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token={token}"
            bot.send_message(call.message.chat.id, f"Перейдите по ссылке для оплаты: {payment_url}")
        else:
            error_message = response_data.get('L_LONGMESSAGE0', 'Произошла ошибка при создании платежа. Попробуйте позже.')
            bot.send_message(call.message.chat.id, f"Ошибка: {error_message}")
    else:
        bot.send_message(call.message.chat.id, "Произошла ошибка при подключении к PayPal. Попробуйте позже.")

# Запуск бота
bot.polling(none_stop=True)
