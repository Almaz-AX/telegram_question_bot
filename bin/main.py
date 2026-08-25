from http.server import BaseHTTPRequestHandler, HTTPServer
import os

import asyncio
import threading

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

# --- 4. ФИКТИВНЫЙ ВЕБ-СЕРВЕР ДЛЯ RENDER ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    """Простой обработчик, который всегда возвращает 'OK'."""
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_http_server():
    """Запускает HTTP-сервер на порту из переменной PORT."""
    port = int(os.environ.get('PORT', 8080))
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, HealthCheckHandler)
    print(f"⚡ Фиктивный HTTP-сервер запущен на порту {port}")
    httpd.serve_forever()

# --- 5. ЗАПУСК ---
async def main():
    print("="*50)
    
    # Запускаем HTTP-сервер как задачу
    import threading
    thread = threading.Thread(target=run_http_server, daemon=True)
    thread.start()
    await asyncio.sleep(0.5)  # Даем время на запуск
    
    print("🚀 Запускаю бота...")
    await dp.start_polling(bot)

# async def main():
#     await dp.start_polling(bot)

if __name__== "__main__":
    asyncio.run(main())
    