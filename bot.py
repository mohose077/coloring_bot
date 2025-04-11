from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)
from config import TELEGRAM_BOT_TOKEN

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привіт! Це бот, який створює унікальні розмальовки для дітей 🖍️\n\n"
        "📌 Як це працює?\n"
        "1. Обери вік дитини — ми підберемо складність\n"
        "2. Обери тему — мультики, тварини, машинки тощо\n"
        "3. Вкажи формат і кількість зображень\n"
        "4. Отримай розмальовки у форматі A4 або A5\n\n"
        "⬇️ Обери вік:"
    )
    keyboard = [["2-3 роки", "4 роки"], ["5 років", "6 років"]]
    await update.message.reply_text(
        "Вік дитини:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )

# ОБРОБКА ВІКУ
async def handle_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    age = update.message.text
    context.user_data["age"] = age

    keyboard = [["Дісней", "Тварини"], ["Машинки", "Динозаври"], ["Казкові", "Їжа"]]
    await update.message.reply_text(
        f"✅ Вік обрано: {age}\n⬇️ Тепер обери тематику розмальовок:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )

# ОБРОБКА ТЕМИ
async def handle_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = update.message.text
    context.user_data["topic"] = topic

    await update.message.reply_text(
        f"✅ Тематика обрана: {topic}\n🔜 Наступний крок — обрати кількість зображень (це зробимо далі)"
    )

# MAIN
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("^(2-3 роки|4 роки|5 років|6 років)$"), handle_age))
    app.add_handler(MessageHandler(filters.Regex("^(Дісней|Тварини|Машинки|Динозаври|Казкові|Їжа)$"), handle_topic))

    app.run_polling()

if __name__ == "__main__":
    main()
