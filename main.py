import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery, FSInputFile
from aiogram import F
from aiogram import Router

API_TOKEN = '8077962203:AAHHndkIuMJz__r2nOimrh2CGG8vS8OLCDo'


youtube_video_url = "https://www.youtube.com/watch?v=MunPNYumw6M"
video_duration = 120  # время видео обьяснение после которого отправлять сообщение

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

#  /start
@router.message(Command("start"))
async def start(message: types.Message):
    # видео отправляем
    video_circle_file = FSInputFile("Resources/hello.MP4")
    await bot.send_video(chat_id=message.chat.id, video=video_circle_file)  #send_video чтобы отправить видео

    # задержка перед сообщением
    await asyncio.sleep(12)

    #  кнопка "Получить видеоурок"
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="✅ Получить видеоурок", url=youtube_video_url)]
    ])
    await message.answer("Нажмите на кнопку, чтобы посмотреть видеоурок:", reply_markup=markup)

    # сообщение о том, что после просмотра видео продолжим
    await message.answer("После просмотра видеоурока мы продолжим выбор курса. Не забудьте вернуться сюда, чтобы узнать больше!")

    # Устанавливаем таймер для отправки следующего сообщения
    await asyncio.sleep(video_duration)

    # знакомства
    final_text = (
        "Что вас ждет:\n"
        "- Алгоритмы, стратегии и фишки по ютуб\n"
        "- Пошаговые туториалы для новичков, которые помогут понять основу ведения каналов\n"
        "- Проанализированные детские/взрослые ниши, в которых можно стартовать и выходить на свой первый доход\n"
        "- Видеоуроки по 3D анимации, монтажу, превью и нишам\n"
        "- Мастер классы от лучших креаторов\n"
        "- Созвоны с экспертами в своих нишах, которые зарабатывают более 500к$+ с ютуб\n"
        "- Лучшие Аі сервисы для упрощения работы с ютубом + расширения которыми мы пользуемся\n"
        "- Материалы для улучшения вашего контента\n"
        "- Общий чат для общения\n"
        "- Бизнес-вечеринки в разных городах мира\n"
        "Присоединяйся"
    )
    # кнопки 3
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="💸 Оплатить доступ", callback_data="pay")],
        [types.InlineKeyboardButton(text="📊 Подробнее о канале", callback_data="details")],
        [types.InlineKeyboardButton(text="❤️ Задать вопрос", callback_data="ask_question")]
    ])
    await message.answer(final_text, reply_markup=markup)

# Кнопка "Оплатить доступ"
@router.callback_query(F.data == "pay")
async def handle_payment(call: CallbackQuery):
    payment_text = (
        "Стоимость курса:\n"
        "49.900 тенге\n"
        "9.900 рублей\n"
        "1.000.000 сомов\n"
        "20.000 сумов\n"
        "Выбери удобный способ оплаты."
    )
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="💳 Оплатить с Каспи", url="https://pay.kaspi.kz/pay/9oemyufr")],
        [types.InlineKeyboardButton(text="💳 Оплатить картой", callback_data="pay_card")],
        [types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_details")]
    ])
    await call.message.edit_text(payment_text, reply_markup=markup)

# Кнопка "Оплатить картой"
@router.callback_query(F.data == "pay_card")
async def handle_pay_card(call: CallbackQuery):
    await call.message.answer("Этот способ оплаты пока не доступен. Пожалуйста, выберите другой способ оплаты.")

# Кнопка "Назад"
@router.callback_query(F.data == "back_to_details")
async def handle_back_to_details(call: CallbackQuery):
    # Сообщение с информацией "Что вас ждет"
    final_text = (
        "Что вас ждет:\n"
        "- Алгоритмы, стратегии и фишки по ютуб\n"
        "- Пошаговые туториалы для новичков, которые помогут понять основу ведения каналов\n"
        "- Проанализированные детские/взрослые ниши, в которых можно стартовать и выходить на свой первый доход\n"
        "- Видеоуроки по 3D анимации, монтажу, превью и нишам\n"
        "- Мастер классы от лучших креаторов\n"
        "- Созвоны с экспертами в своих нишах, которые зарабатывают более 500к$+ с ютуб\n"
        "- Лучшие Аі сервисы для упрощения работы с ютубом + расширения которыми мы пользуемся\n"
        "- Материалы для улучшения вашего контента\n"
        "- Общий чат для общения\n"
        "- Бизнес-вечеринки в разных городах мира\n"
        "Присоединяйся"
    )

    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="💸 Оплатить доступ", callback_data="pay")],
        [types.InlineKeyboardButton(text="📊 Подробнее о канале", callback_data="details")],
        [types.InlineKeyboardButton(text="❤️ Задать вопрос", callback_data="ask_question")]
    ])
    await call.message.edit_text(final_text, reply_markup=markup)

# кнопки "Подробнее о канале"
@router.callback_query(F.data == "details")
async def handle_details(call: CallbackQuery):
    await call.message.answer("Вы можете узнать больше, перейдя по ссылке:")
    await call.message.answer("https://t.me/c/2455787583/7")
# кнопки "Задать вопрос"
@router.callback_query(F.data == "ask_question")
async def handle_question(call: CallbackQuery):
    await call.message.answer("Вы можете задать вопрос, написав нам перейдя по ссылке:")
    await call.message.answer("https://t.me/c/2455787583/2")

# Запуск бота
async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
