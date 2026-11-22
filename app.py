import os
import threading
from datetime import date
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask

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

# Создаём Flask-приложение
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    # Запускаем Flask в фоновом потоке (он не капризный)
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    # Запускаем Flask в фоне, чтобы Render видел порт
    threading.Thread(target=run_flask).start()
    
    # А бота запускаем в ГЛАВНОМ потоке
    print("Бот запущен и ждет сообщений...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("days", days_left))
    app.run_polling()
