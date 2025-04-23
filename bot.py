import os
import logging
from dotenv import load_dotenv
load_dotenv()
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from aliexpress_api import get_product_info
from keep_alive import keep_alive

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! أرسل رابط منتج من AliExpress وسأعطيك التفاصيل.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "aliexpress.com/item" in text:
        info = get_product_info(text)
        await update.message.reply_text(info)
    else:
        await update.message.reply_text("أرسل رابط منتج من AliExpress فقط.")

if __name__ == '__main__':
    keep_alive()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
