import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Echo the user message."""

    await update.message.reply_text(update.message.text)

async def echo_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Echo the user photo."""
    
    await update.message.reply_photo(update.message.photo)


if __name__ == '__main__':
    application = ApplicationBuilder().token('5800137374:AAFszl4NSS7k_O7FEwk2fBB-c67uRbqXMzw').build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.PHOTO, echo_photo))
    application.run_polling()