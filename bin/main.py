import os

import asyncio

from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_CHAT_ID = os.environ["ADMIN_CHAT_ID"]



bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

start_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚀 START")]
    ],
    resize_keyboard=True  # Автоматически подгоняет размер кнопки
)

@dp.message(Command("start"))
async def handle_start(message: Message):
    await message.answer(
        "👋 **Добро пожаловать в бот для сбора вопросов по психологии!**\n\n"
        "📝 Отправьте свой вопрос, и он будет передан организаторам подкаста.\n"
        "🔒 Вопросы анонимные.\n\n",
        reply_markup=start_button)
    
@dp.message(Command("getid"))
async def get_chat_id(message: types.Message):
    chat_id = message.chat.id
    await message.answer(f"ID этого чата: `{chat_id}`")

@dp.message()
async def handle_question(message: Message):
    # Проверяем, что это не команда
    if message.text and not message.text.startswith('/'):
        # Выводим только вопрос в консоль
        print("\n" + "="*60)
        print(f"📨 НОВЫЙ ВОПРОС!")
        print("="*60)
        print(f"❓ {message.text}")
        print("="*60 + "\n")
        
        # Отправляем анонимный вопрос в чат
        try:
            await bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=f"📝 **Вопрос для подкаста:**\n\n{message.text}\n\n---\n💭 Ждем ваш ответ в эфире!"
            )
            
            # Подтверждаем пользователю
            await message.answer(
                "✅ Ваш анонимный вопрос отправлен в чат подкаста!\n"
                "Спасибо за участие! 🙏\n\n"
                "📝 Если хотите задать ещё вопрос - просто напишите его."
            )
        except Exception as e:
            await message.answer(
                "❌ Произошла ошибка при отправке вопроса в чат.\n"
                "Пожалуйста, попробуйте позже."
            )
            print(f"❌ Ошибка: {e}")
async def handle_health_check(reader, writer):
    """Обработчик для фиктивного HTTP-запроса."""
    writer.write(b"HTTP/1.1 200 OK\r\n\r\nOK")
    await writer.drain()
    writer.close()
    await writer.wait_closed()
                
async def run_http_server_async():
    """Запускает HTTP-сервер асинхронно."""
    port = int(os.environ.get('PORT', 8080))
    server = await asyncio.start_server(handle_health_check, '0.0.0.0', port)
    print(f"⚡ Асинхронный HTTP-сервер запущен на порту {port}")
    async with server:
        await server.serve_forever()

async def main():
    asyncio.create_task(run_http_server_async())
    await dp.start_polling(bot)

if __name__== "__main__":
    asyncio.run(main())
    