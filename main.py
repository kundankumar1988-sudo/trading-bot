import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ---------- NIFTY DATA ----------
def get_nifty_price():
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI"
        data = requests.get(url, timeout=5).json()
        price = data['chart']['result'][0]['meta']['regularMarketPrice']
        prev = data['chart']['result'][0]['meta']['chartPreviousClose']
        change = price - prev
        return price, change
    except:
        return None, None


# ---------- SIGNAL ENGINE ----------
def generate_signal(price, change):

    atm = round(price / 50) * 50

    # Trend
    if change > 40:
        trend = "UP"
    elif change < -40:
        trend = "DOWN"
    else:
        trend = "SIDE"

    # Momentum (fake breakout logic)
    if abs(change) > 70:
        momentum = "STRONG"
    elif abs(change) > 25:
        momentum = "MEDIUM"
    else:
        momentum = "WEAK"

    # Decision
    if trend == "UP" and momentum == "STRONG":
        return f"🟢 STRONG BUY CE\nStrike: {atm}\nSL: -20pts\nTarget: +40pts\nValid: 10 min"

    if trend == "UP":
        return f"🟢 BUY CE\nStrike: {atm}\nSL: -15pts\nTarget: +25pts\nValid: 10 min"

    if trend == "DOWN" and momentum == "STRONG":
        return f"🔴 STRONG BUY PE\nStrike: {atm}\nSL: -20pts\nTarget: +40pts\nValid: 10 min"

    if trend == "DOWN":
        return f"🔴 BUY PE\nStrike: {atm}\nSL: -15pts\nTarget: +25pts\nValid: 10 min"

    return "⚪ NO TRADE — Market sideways"


# ---------- COMMANDS ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 NIFTY PRO BOT READY\n\n"
        "/nifty - Live price\n"
        "/signal - Trade signal"
    )

async def nifty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price, change = get_nifty_price()
    if price:
        await update.message.reply_text(f"📊 NIFTY: {price}\nChange: {round(change,2)}")
    else:
        await update.message.reply_text("Market data error")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price, change = get_nifty_price()
    if price:
        msg = generate_signal(price, change)
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text("Signal unavailable")


# ---------- RUN ----------
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("nifty", nifty))
app.add_handler(CommandHandler("signal", signal))

print("Bot running...")
app.run_polling()
