import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot Online")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI"
    data = requests.get(url).json()
    price = data['chart']['result'][0]['meta']['regularMarketPrice']
    await update.message.reply_text(f"NIFTY: {price}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("nifty", price))

print("Bot running...")
app.run_polling()
