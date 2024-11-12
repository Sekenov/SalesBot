import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery, FSInputFile
from aiogram import F
from aiogram import Router

API_TOKEN = '8077962203:AAHHndkIuMJz__r2nOimrh2CGG8vS8OLCDo'

# Параметры, которые можно легко менять
youtube_video_url = "https://www.youtube.com/watch?v=MunPNYumw6M"
video_duration = 120  # Длительность видео в секундах, которую можно менять

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

# Хранение данных о пользователях в оперативной памяти
user_data = {}


# Обработчик команды /start
@router.message(Command("start"))
async def start(message: types.Message):
    # Имитируем "печатает" через типичное ожидание
    typing_duration = 10  # Время, которое бот "печатает" (в секундах)
    await bot.send_chat_action(message.chat.id, action=types.ChatActions.TYPING)
    await asyncio.sleep(typing_duration)

    # Отправка кнопки "Получить видеоурок"
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="✅ Получить видеоурок", url=youtube_video_url)]
    ])
    await message.answer("Нажмите на кнопку, чтобы посмотреть видеоурок:", reply_markup=markup)

    # Устанавливаем таймер для отправки следующего сообщения
    await asyncio.sleep(video_duration)

    # Сообщение после просмотра видео с тремя кнопками
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
        "- Материалы для улучшения вашего контента\n"
        "- Общий чат для общения\n"
        "- Бизнес-вечеринки в разных городах мира\n"
        "Присоединяйся"
    )

    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="💸 Оплатить доступ", callback_data="pay")],
        [types.InlineKeyboardButton(text="📈 Подробнее о канале", callback_data="details")],
        [types.InlineKeyboardButton(text="❤️ Задать вопрос", callback_data="ask_question")]
    ])
    await message.answer(final_text, reply_markup=markup)


# Обработчик кнопки "Оплатить доступ"
@router.callback_query(F.data == "pay")
async def handle_payment(call: CallbackQuery):
    await call.message.answer("Платежная система пока не реализована. Пожалуйста, подождите дальнейших обновлений.")


# Обработчик кнопки "Подробнее о канале"
@router.callback_query(F.data == "details")
async def handle_details(call: CallbackQuery):
    await call.message.answer("Этот канал посвящен системному анализу и улучшению вашего контента на YouTube.")


# Обработчик кнопки "Задать вопрос"
@router.callback_query(F.data == "ask_question")
async def handle_question(call: CallbackQuery):
    await call.message.answer("Вы можете задать вопрос, написав нам напрямую в личные сообщения.")


# Запуск бота
async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
