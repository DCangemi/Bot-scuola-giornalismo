import asyncio
import os
import logging
import nest_asyncio
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)
#from stay_alive import keep_alive

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

# Suppress httpx logs
logging.getLogger("httpx").setLevel(logging.WARNING)

# Load token from .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Define command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Received /start")
    await update.message.reply_text(
        "👋 Hello! I’m your assistant receptionist bot. How can I help you today?"
    )

# Define message handler
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    logging.info(f"Received message: {text}")

    if "hours" in text:
        await update.message.reply_text("🕒 We're open from 9:00 AM to 6:00 PM.")
    elif "location" in text:
        await update.message.reply_text("📍 We're located at 123 Sunshine Ave, Palermo.")
    elif "book" in text:
        await update.message.reply_text("📅 You can book a tour at https://example.com/book")
    else:
        await update.message.reply_text("🤖 I'm still learning! Try asking about hours or booking.")

# Build app
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

# Make it run in Replit
nest_asyncio.apply()

async def run():
    await app.run_polling()
    logging.info("Bot polling started.")

asyncio.run(run())
