import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ---- nifty price ----
def get_nifty():
    url = "https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI"
    data = requests.get(url).json()
    price = data['chart']['result'][0]['meta']['regularMarketPrice']
    prev = data['chart']['result'][0]['meta']['chartPreviousClose']
    return price, round(price-prev,2)

# ---- commands ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot Online")

async def nifty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price, ch = get_nifty()
    await update.message.reply_text(f"NIFTY: {price}\nChange: {ch}")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price, ch = get_nifty()
    strike = round(price/50)*50
    if ch > 0:
        msg = f"🟢 BUY CE {strike}"
    else:
        msg = f"🔴 BUY PE {strike}"
    await update.message.reply_text(msg)

# ---- run ----
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("nifty", nifty))
app.add_handler(CommandHandler("signal", signal))

print("Bot running...")
app.run_polling()
