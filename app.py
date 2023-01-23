# Import the telegram bot framwork and everythings we need
from telegram import Update
from telegram.ext import Updater,CallbackContext,CommandHandler
#import api key
from decouple import config
# create  api_secret var and assign it to our api code
# you should make all of the global variables here
api_token = config("API_TOKEN")
updater = Updater (api_token)
dispatcher = updater.dispatcher
#Create function that accept a string and returns same string(echo bot)
def start(update:Update,context:CallbackContext):
    chat_id = update.message.chat_id
    message_id = update.message.message_id

    context.bot.send_message(chat_id=chat_id, text="Hello")

dispatcher.add_handler(CommandHandler(['start','s','START'],start))
updater.start_polling()
#don't forget to make if __main__ here
