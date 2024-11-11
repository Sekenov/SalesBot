import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram import F
import json
from aiogram import Router

API_TOKEN = '8077962203:AAHHndkIuMJz__r2nOimrh2CGG8vS8OLCDo'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

# Хранение данных о пользователях в оперативной памяти
user_data = {}

# Обработчик команды /start
@router.message(Command("start"))
async def start(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    btn_start = types.InlineKeyboardButton("🚀 Start", callback_data="start")
    markup.add(btn_start)
    await message.answer("Привет! Я бот, который поможет вам выбрать курс и оформить оплату. Нажмите 'Start', чтобы начать.", reply_markup=markup)

# Обработчик callback для кнопки Start
@router.callback_query(F.data == "start")
async def handle_start(call: CallbackQuery):
    markup = types.InlineKeyboardMarkup()
    btn_kz = types.InlineKeyboardButton("🇰🇿 Казахстан", callback_data="country_kz")
    btn_ru = types.InlineKeyboardButton("🇷🇺 Россия", callback_data="country_ru")
    btn_az = types.InlineKeyboardButton("🇦🇿 Азербайджан", callback_data="country_az")
    markup.add(btn_kz, btn_ru, btn_az)

    await call.message.edit_text("Из какой вы страны? Это нужно, чтобы показать цену курса в вашей валюте.", reply_markup=markup)

# Обработчик выбора страны
@router.callback_query(F.data.startswith("country_"))
async def handle_country(call: CallbackQuery):
    country_code = call.data.split("_")[1]
    countries = {"kz": "Казахстан", "ru": "Россия", "az": "Азербайджан"}
    country = countries.get(country_code, "Казахстан")

    user_data[call.message.chat.id] = {"country": country}

    markup = types.InlineKeyboardMarkup()
    btn_questions = types.InlineKeyboardButton("❓ Вопросы", callback_data="questions")
    btn_courses = types.InlineKeyboardButton("📚 Перейти к курсам", callback_data="courses")
    markup.add(btn_questions, btn_courses)

    await call.message.edit_text(f"Отлично, вы выбрали {country}. Если у вас есть вопросы, нажмите кнопку 'Вопросы'. Либо можете перейти к выбору курсов.", reply_markup=markup)

# Обработчик вопросов
@router.callback_query(F.data == "questions")
async def questions(call: CallbackQuery):
    markup = types.InlineKeyboardMarkup()
    btn_q1 = types.InlineKeyboardButton("Точно ли вы скинете курс после оплаты?", callback_data="question_1")
    btn_q2 = types.InlineKeyboardButton("Как долго длится курс?", callback_data="question_2")
    btn_q3 = types.InlineKeyboardButton("Есть ли поддержка после покупки?", callback_data="question_3")
    btn_q4 = types.InlineKeyboardButton("Можно ли вернуть деньги?", callback_data="question_4")
    btn_q5 = types.InlineKeyboardButton("Какие материалы я получу?", callback_data="question_5")
    markup.add(btn_q1, btn_q2)
    markup.add(btn_q3, btn_q4)
    markup.add(btn_q5)

    await call.message.edit_text("Выберите ваш вопрос:", reply_markup=markup)

# Обработчик ответов на вопросы
@router.callback_query(F.data.startswith("question_"))
async def handle_questions(call: CallbackQuery):
    answers = {
        "question_1": "Да, сразу после оплаты вы получите доступ к курсу.",
        "question_2": "Курс длится 4 недели, включая все необходимые материалы и задания.",
        "question_3": "Да, мы предоставляем поддержку в течение 3 месяцев после покупки.",
        "question_4": "Да, вы можете вернуть деньги в течение 7 дней после покупки, если курс вам не подошел.",
        "question_5": "Вы получите видеоуроки, PDF-материалы и доступ к сообществу."
    }
    await call.message.answer(answers[call.data])

# Обработчик выбора курсов
@router.callback_query(F.data == "courses")
async def handle_courses(call: CallbackQuery):
    markup = types.InlineKeyboardMarkup()
    btn_ds = types.InlineKeyboardButton("🧪 Data Science", callback_data="course_ds")
    btn_da = types.InlineKeyboardButton("📊 Data Analytics", callback_data="course_da")
    markup.add(btn_ds, btn_da)

    await call.message.edit_text("Выберите курс:", reply_markup=markup)

# Обработчик выбора конкретного курса
@router.callback_query(F.data.startswith("course_"))
async def handle_selected_course(call: CallbackQuery):
    course_code = call.data.split("_")[1]
    courses = {"ds": "Data Science", "da": "Data Analytics"}
    course = courses.get(course_code, "Data Science")

    if course == "Data Science":
        await bot.send_photo(call.message.chat.id, open("Resources/dataSciencePhoto.jpeg", 'rb'))
        await bot.send_video(call.message.chat.id, open("Resources/videoDataScience.mp4", 'rb'))
    elif course == "Data Analytics":
        await bot.send_photo(call.message.chat.id, open("Resources/dataAnalysticsPhoto.jpeg", 'rb'))
        await bot.send_video(call.message.chat.id, open("Resources/videoDataAnalystics.mp4", 'rb'))

    await asyncio.sleep(1)
    await call.message.answer(f"Вы выбрали курс {course}. Вот немного информации о курсе.")

    markup = types.InlineKeyboardMarkup()
    btn_pay = types.InlineKeyboardButton("💳 Оплатить", callback_data="pay")
    markup.add(btn_pay)
    await call.message.answer("Если хотите купить этот курс, нажмите 'Оплатить'.", reply_markup=markup)

# Обработчик оплаты
@router.callback_query(F.data == "pay")
async def handle_payment(call: CallbackQuery):
    country = user_data.get(call.message.chat.id, {}).get("country", "Казахстан")

    if country == "Казахстан":
        price = "20,000 тг"
    elif country == "Россия":
        price = "3900 рублей"
    elif country == "Азербайджан":
        price = "68 манат"
    else:
        price = "20,000 тг"

    await call.message.answer(f"💵 Стоимость курса: {price}. Курс был оплачен. Спасибо!")

# Запуск бота
async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())