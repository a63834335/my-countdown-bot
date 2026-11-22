from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask

TOKEN = os.environ.get("TELEGRAM_TOKEN")
TARGET_DATE = date(2027, 3, 28)  # Ваша главная дата

# 🛠 ЗДЕСЬ НАСТРАИВАЕМ ОСОБЫЕ ДНИ ДО СОБЫТИЯ
# Формат: {количество_дней_до_события: "Текст сообщения"}
SPECIAL_DAYS_BEFORE = {
    1: "🚴‍♀️ ВСЁ, ЗАВТРА КАТАЦА!",
    2: "🔥 ПОСЛЕЗАВТРА, НУ ЁМАЁ, ЧО ТАК ДОЛГО ТО",
    3: "⏳ Осталось всего 3 дня. Самое время купить покрышки.",
    67:"Сикс севен дней до веорсезона (боже, какой позор...)",
    69:"69 дней до велосезона, число красивое, повод отметить",
    125:"125 дней до велосезона, дни тянуться слишком медленно...."
    126:"126 дней до велосезона, я создала этого бота, ломка капец..."
    
    # Сюда можно добавлять другие дни:
    # 10: "Осталось 10 дней, начинаем разминку!",
}


async def days_left(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = date.today()
    delta = (TARGET_DATE - today).days

    # 1. Проверяем, не наступил ли какой-то из особых дней
    if delta in SPECIAL_DAYS_BEFORE:
        text = SPECIAL_DAYS_BEFORE[delta]

    # 2. Если особого дня нет, работает стандартная логика
    elif delta > 0:
        text = f"📅 До велосезона осталось: {delta} дней"
    elif delta == 0:
        text = "🎉 СЕГОДНЯ СТАРТ ВЕЛОСЕЗОНА, УРА, ДОЖИЛИ!!!"
    else:
        text = f"Этот день прошёл {abs(delta)} дней назад."

    await update.message.reply_text(text)


# --- ВЕБ-СЕРВЕР ДЛЯ RENDER ---
web_app = Flask(__name__)


@web_app.route('/')
def home():
    return "Bot is running!"


def run_flask():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    threading.Thread(target=run_flask).start()

    print("Бот запущен и ждет сообщений...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("days", days_left))
    app.run_polling()
