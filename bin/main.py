import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command


BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_CHAT_ID = os.environ["ADMIN_CHAT_ID"]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def handle_start(message: Message):
    await message.answer("Привет!")

async def main():
    await dp.start_polling(bot)

if __name__== "__main__":
    asyncio.run(main())

# class Handler(BaseHTTPRequestHandler):
#     def do_POST(self):
#         if self.path != "/webhook":
#             self.send_response(404)
#             self.end_headers()
#             return

#         content_length = int(self.headers.get("Content-Length", 0))
#         body = self.rfile.read(content_length)
#         update = json.loads(body)

#         message = update.get("message")
#         if message and "text" in message:
#             text = message["text"]
#             date = message["date"]
#             chat_id = message["chat"]["id"]

#             # Время для красоты
#             from datetime import datetime
#             time_str = datetime.fromtimestamp(date).strftime("%Y-%m-%d %H:%M")

#             # Пересылка тебе в канал
#             requests.post(
#                 f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
#                 json={
#                     "chat_id": ADMIN_CHAT_ID,
#                     "text": f"📬 Анонимный вопрос ({time_str})\n\n{text}"
#                 }
#             )

#             # Ответ пользователю
#             requests.post(
#                 f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
#                 json={
#                     "chat_id": chat_id,
#                     "text": "Спасибо, вопрос принят. Разберу на этой неделе."
#                 }
#             )

#         self.send_response(200)
#         self.end_headers()
#         self.wfile.write(b'{"ok": true}')

#     def log_message(self, format, *args):
#         print(f"[HTTP] {format % args}")

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 8080))
#     server = HTTPServer(("0.0.0.0", port), Handler)
#     print(f"Server running on port {port}")
#     server.serve_forever()
