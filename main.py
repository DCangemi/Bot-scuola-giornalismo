import os
import logging
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

# Suppress noisy logs
logging.getLogger("httpx").setLevel(logging.WARNING)

# Load environment
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 8443))
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")  # Must be set in Render's Environment Variables

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I’m your assistant receptionist bot. How can I help you today?")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
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

# Build app and run webhook server
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

webhook_url = f"{RENDER_EXTERNAL_URL}/{TOKEN}"

# This runs the webhook directly without asyncio.run()
app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    webhook_url=webhook_url
)