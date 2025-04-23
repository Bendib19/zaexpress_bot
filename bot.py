import os
import logging
from flask import Flask, request
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)
from aliexpress_api import get_product_info

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
APP_URL = os.getenv("APP_URL")  # مثل https://zaexpress-bot.koyeb.app

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
telegram_app = ApplicationBuilder().token(TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبا! أرسل رابط منتج من AliExpress.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "aliexpress.com/item" in text:
        info = get_product_info(text)
        await update.message.reply_text(info)
    else:
        await update.message.reply_text("أرسل رابط منتج من AliExpress.")


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    await telegram_app.update_queue.put(Update.de_json(data, telegram_app.bot))
    return "OK"


@app.route("/")
def home():
    return "Bot is running."


if __name__ == "__main__":
    import asyncio
    asyncio.run(telegram_app.bot.set_webhook(f"{APP_URL}/{TOKEN}"))
    app.run(host="0.0.0.0", port=8080)
