from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import date
import os
from flask import Flask
import threading

# --- ВАШ КОД БОТА ---
# Токен теперь берем из переменных окружения хостинга (об этом ниже)
TOKEN = os.environ.get("TELEGRAM_TOKEN")
TARGET_DATE = date(2027, 3, 28)

async def days_left(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = date.today()
    delta = (TARGET_DATE - today).days
    if delta > 0:
        text = f"📅 До 28 марта 2027 года осталось: {delta} дней"
    elif delta == 0:
        text = "🎉 Сегодня 28 марта 2027 года!"
    else:
        text = f"Этот день прошёл {abs(delta)} дней назад."
    await update.message.reply_text(text)

def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("days", days_left))
    print("Бот запущен и ждет сообщений...")
    app.run_polling()

# --- ВЕБ-СЕРВЕР ДЛЯ RENDER ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running!"

if __name__ == '__main__':
    # Запускаем бота в отдельном потоке, чтобы он не мешал веб-серверу
    threading.Thread(target=run_bot).start()
    # Запускаем веб-сервер на порту, который даст Render
    port = int(os.environ.get("PORT", 5000))
    web_app.run(host='0.0.0.0', port=port)