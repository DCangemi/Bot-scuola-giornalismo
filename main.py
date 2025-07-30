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
from stay_alive import keep_alive

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

# Suppress httpx logs
logging.getLogger("httpx").setLevel(logging.WARNING)

# Load token from environment
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Create Telegram app
app = ApplicationBuilder().token(TOKEN).build()

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I’m your assistant receptionist bot. How can I help you today?")

# Generic message handler
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    logging.info(f"User said: {text}")

    if "hours" in text:
        await update.message.reply_text("🕒 We're open from 9:00 AM to 6:00 PM.")
    elif "location" in text:
        await update.message.reply_text("📍 We're located at 123 Sunshine Ave, Palermo.")
    elif "book" in text:
        await update.message.reply_text("📅 You can book a tour at https://example.com/book")
    elif "palla" in text:
        await update.message.reply_text("yeah should be working")
    elif "joker" in text:
        await update.message.reply_text("what we doin")
    else:
        await update.message.reply_text("🤖 I'm still learning! Try asking about hours or booking.")

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

# Keep server alive on Render
keep_alive()

# Patch nested loop behavior (Render-safe)
nest_asyncio.apply()

# Start the bot (use current loop directly)
loop = asyncio.get_event_loop()
loop.create_task(app.run_polling())
loop.run_forever()
