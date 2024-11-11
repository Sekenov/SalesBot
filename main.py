import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram import F
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
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🚀 Start", callback_data="start")]
    ])
    await message.answer("Привет! Я бот, который поможет вам выбрать курс и оформить оплату. Нажмите 'Start', чтобы начать.", reply_markup=markup)

# Обработчик callback для кнопки Start
@router.callback_query(F.data == "start")
async def handle_start(call: CallbackQuery):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🇰🇿 Казахстан", callback_data="country_kz"),
         types.InlineKeyboardButton(text="🇷🇺 Россия", callback_data="country_ru"),
         types.InlineKeyboardButton(text="🇦🇿 Азербайджан", callback_data="country_az")]
    ])
    await call.message.edit_text("Из какой вы страны? Это нужно, чтобы показать цену курса в вашей валюте.", reply_markup=markup)

# Обработчик выбора страны
@router.callback_query(F.data.startswith("country_"))
async def handle_country(call: CallbackQuery):
    country_code = call.data.split("_")[1]
    countries = {"kz": "Казахстан", "ru": "Россия", "az": "Азербайджан"}
    country = countries.get(country_code, "Казахстан")

    user_data[call.message.chat.id] = {"country": country}

    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="❓ Вопросы", callback_data="questions")],
        [types.InlineKeyboardButton(text="📚 Перейти к курсам", callback_data="courses")]
    ])
    await call.message.edit_text(f"Отлично, вы выбрали {country}. Если у вас есть вопросы, нажмите кнопку 'Вопросы'. Либо можете перейти к выбору курсов.", reply_markup=markup)

# Обработчик вопросов
@router.callback_query(F.data == "questions")
async def questions(call: CallbackQuery):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Точно ли вы скинете курс после оплаты?", callback_data="question_1")],
        [types.InlineKeyboardButton(text="Как долго длится курс?", callback_data="question_2")],
        [types.InlineKeyboardButton(text="Есть ли поддержка после покупки?", callback_data="question_3")],
        [types.InlineKeyboardButton(text="Можно ли вернуть деньги?", callback_data="question_4")],
        [types.InlineKeyboardButton(text="Какие материалы я получу?", callback_data="question_5")]
    ])
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
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🧪 Data Science", callback_data="course_ds")],
        [types.InlineKeyboardButton(text="📊 Data Analytics", callback_data="course_da")]
    ])
    await call.message.edit_text("Выберите курс:", reply_markup=markup)

# Обработчик выбора конкретного курса
@router.callback_query(F.data.startswith("course_"))
async def handle_selected_course(call: CallbackQuery):
    course_code = call.data.split("_")[1]
    courses = {"ds": "Data Science", "da": "Data Analytics"}
    course = courses.get(course_code, "Data Science")

    try:
        if course == "Data Science":
            with open("Resources/dataSciencePhoto.jpeg", 'rb') as photo:
                await bot.send_photo(call.message.chat.id, photo)
            with open("Resources/videoDataScience.mp4", 'rb') as video:
                await bot.send_video(call.message.chat.id, video)
        elif course == "Data Analytics":
            with open("Resources/dataAnalysticsPhoto.jpeg", 'rb') as photo:
                await bot.send_photo(call.message.chat.id, photo)
            with open("Resources/videoDataAnalystics.mp4", 'rb') as video:
                await bot.send_video(call.message.chat.id, video)
    except FileNotFoundError:
        await call.message.answer("Извините, материалы для выбранного курса временно недоступны.")

    await asyncio.sleep(1)
    await call.message.answer(f"Вы выбрали курс {course}. Вот немного информации о курсе.")

    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="💳 Оплатить", callback_data="pay")]
    ])
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
