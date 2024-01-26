import logging
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_html(
        f"Привіт, {user.mention_html()}!",
        reply_markup=get_keyboard(),
    )
    logger.info("Command /start processed.")

# Function to handle the /exchange command
def exchange(update: Update, context: CallbackContext) -> None:
    try:
        logger.info("Exchange command received")
        url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            logger.debug(f"Exchange data received: {data}")
            exchange_rates = "\n".join([f"{rate['txt']} ({rate['cc']}): {rate['rate']}" for rate in data])
            update.message.reply_text(f"Офіційний курс гривні щодо іноземних валют на сьогодні:\n{exchange_rates}")
        else:
            update.message.reply_text(f"Error fetching data: {response.status_code}")
            logger.warning(f"Error fetching exchange data. Status code: {response.status_code}")
    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")
        logger.error(f"Error in exchange command: {str(e)}")

# Function to get the keyboard
def get_keyboard():
    keyboard = [
        ["Офіційний курс гривні щодо іноземних валют на сьогодні."]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Main function
def main() -> None:
    updater = Updater("XXXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXX")  # Replace 'YOUR_BOT_TOKEN' with your bot token

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("exchange", exchange))
    dp.add_handler(MessageHandler(Filters.regex(r'Офіційний курс гривні щодо іноземних валют на сьогодні.'), exchange))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
