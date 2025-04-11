import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
from config import TELEGRAM_BOT_TOKEN
from generator import generate_coloring_image


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привіт! Це бот, що створює розмальовки за обраними критеріями 🖍️\n\n"
        "1. Обери вік дитини\n"
        "2. Обери тему\n"
        "3. Вкажи кількість та формат\n"
        "4. Отримай розмальовки!\n\n"
        "⬇️ Обери вік:"
    )
    keyboard = [["2-3 роки", "4 роки"], ["5 років", "6 років"]]
    await update.message.reply_text("Вік дитини:", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))


async def handle_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["age"] = update.message.text
    keyboard = [["Дісней", "Тварини"], ["Машинки", "Динозаври"], ["Казкові", "Їжа"]]
    await update.message.reply_text("⬆️ Обери тему:", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))


async def handle_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["topic"] = update.message.text
    keyboard = [["1", "3", "5"], ["10"]]
    await update.message.reply_text("🔢 Обери кількість зображень:", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))


async def handle_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["amount"] = update.message.text
    keyboard = [["A4", "A5"]]
    await update.message.reply_text("🔤 Обери формат:", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))


async def handle_format(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["format"] = update.message.text
    age = context.user_data.get("age")
    topic = context.user_data.get("topic")
    amount = int(context.user_data.get("amount"))
    user_id = update.effective_chat.id

    await update.message.reply_text("🔧 Генеруємо розмальовки...")

    for i in range(amount):
        prompt = f"{topic} for children {age}"
        image_url = generate_coloring_image(prompt)
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("👍 Подобається", callback_data=f"like|{image_url}"), InlineKeyboardButton("👎 Не подобається", callback_data=f"dislike|{image_url}")]])

        try:
            await context.bot.send_photo(chat_id=user_id, photo=image_url, caption=f"🖼 Розмальовка {i+1}/{amount}", reply_markup=keyboard)
        except Exception as e:
            await context.bot.send_message(chat_id=user_id, text="❌ Не вдалося надіслати зображення.")

    await update.message.reply_text("✅ Усі розмальовки надіслані! Дякуємо за оцінки!")


async def handle_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action, image_url = query.data.split("|")
    await query.edit_message_caption(caption=f"{query.message.caption}\n\n✅ Ви оцінили: {'👍' if action == 'like' else '👎'}")

import asyncio

async def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("^(2-3 роки|4 роки|5 років|6 років)$"), handle_age))
    app.add_handler(MessageHandler(filters.Regex("^(Дісней|Тварини|Машинки|Динозаври|Казкові|Їжа)$"), handle_topic))
    app.add_handler(MessageHandler(filters.Regex("^(1|3|5|10)$"), handle_amount))
    app.add_handler(MessageHandler(filters.Regex("^(A4|A5)$"), handle_format))
    app.add_handler(CallbackQueryHandler(handle_rating))

    await app.bot.delete_webhook(drop_pending_updates=True)

    PORT = int(os.environ.get("PORT", 8443))
    BASE_URL = os.environ.get("RENDER_EXTERNAL_URL")

    await app.initialize()
    await app.start()
    await app.updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="webhook",
        webhook_url=f"{BASE_URL}/webhook"
    )

    await app.updater.wait_for_stop()


if __name__ == "__main__":
    asyncio.run(main())

