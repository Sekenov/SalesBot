import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery, FSInputFile
from aiogram import F
from aiogram import Router
import os
import subprocess

API_TOKEN = '7936044043:AAEx6DZbLVeafjfT-729Nh9oA-H2wvak2Io'

youtube_video_url = "https://www.youtube.com/watch?v=MunPNYumw6M"
video_duration = 20

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

# Функция для отправки сообщения "Что вас ждет"
async def send_details_message(chat_id):
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
        [types.InlineKeyboardButton(text="📈 Подробнее о канале", url="https://t.me/c/2455787583/7")],
        [types.InlineKeyboardButton(text="❤️ Задать вопрос", url="https://t.me/c/2455787583/2")]
    ])
    await bot.send_message(chat_id, final_text, reply_markup=markup)
# Обработчик команды /start
@router.message(Command("start"))
async def start(message: types.Message):
    input_video = "C:/Users/temoh/PycharmProjects/ittalker/Resources/hello.mp4"
    output_video = "C:/Users/temoh/PycharmProjects/ittalker/Resources/hello_converted.mp4"

    # Преобразование видео в формат кругляшка с помощью FFmpeg, если выходное видео еще не существует
    if not os.path.exists(output_video):
        try:
            ffmpeg_command = [
                'ffmpeg', '-i', input_video, '-vf', 'scale=320:320:force_original_aspect_ratio=increase,crop=320:320', output_video
            ]
            subprocess.run(ffmpeg_command, check=True)
            print(f"Видео сохранено: {output_video}")
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при выполнении FFmpeg: {e}")
            return

    # Отправка кругляшка в Telegram
    if os.path.exists(output_video):
        video_circle_file = FSInputFile(output_video)
        await bot.send_video_note(chat_id=message.chat.id, video_note=video_circle_file)

    await asyncio.sleep(12)

    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="✅ Получить видеоурок", url=youtube_video_url)]
    ])
    await message.answer("Нажмите на кнопку, чтобы посмотреть видеоурок:", reply_markup=markup)

    # сообщение о том, что после просмотра видео продолжим
    await message.answer("После просмотра видеоурока мы продолжим выбор курса. Не забудьте вернуться сюда, чтобы узнать больше!")

    # таймер
    await asyncio.sleep(video_duration)

    # Отправка сообщения "Что вас ждет"
    await send_details_message(message.chat.id)

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
    await call.message.delete()  # Удаляем сообщение о стоимости курса
    await send_details_message(call.message.chat.id)  # Отправляем обратно меню "Что вас ждет"

# Запуск бота
async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
