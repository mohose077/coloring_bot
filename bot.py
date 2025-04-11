from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_BOT_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привіт! Це бот, який створює унікальні розмальовки для дітей 🖍️\n\n"
        "📌 Як це працює?\n"
        "1. Обери вік дитини — ми підберемо складність малюнків\n"
        "2. Обери тематику — мультики, тварини, машинки та інше\n"
        "3. Вкажи формат і кількість зображень\n"
        "4. Отримай готові розмальовки у зручному форматі для друку (A4 або A5)\n\n"
        "🚀 Давай почнемо! Обери вік дитини:"
    )

    keyboard = [["2-3 роки", "4 роки"], ["5 років", "6 років"]]
    await update.message.reply_text(
        "⬇️ Обери вік:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
