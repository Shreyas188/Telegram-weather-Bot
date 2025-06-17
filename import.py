import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Replace this with your actual Telegram bot token
TELEGRAM_BOT_TOKEN = '8176071921:AAHM6EweVPu5MzTrhHpPMvnXjTY3CAjWUmA'

# Replace this with your weather API token
WEATHER_API_KEY = 'd31649ea604848b382a90721251305'

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        city = " ".join(context.args)
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            temp_c = data['current']['temp_c']
            condition = data['current']['condition']['text']
            location = data['location']['name']
            await update.message.reply_text(f"Weather in {location}:\n{temp_c}°C, {condition}")
        else:
            await update.message.reply_text("Sorry, I couldn't retrieve the weather.")
    else:
        await update.message.reply_text("Please provide a city name like this:\n/weather London")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Use /weather <city> to get the current weather.")

# Main function
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("weather", weather))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()