import logging
import os
import pathlib
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import cv2 as cv


# Enable logging
logging.basicConfig(
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
  level=logging.INFO)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  """Send a message when the command /start is issued."""
  user = update.effective_user
  await update.message.reply_html(
    rf"Hi {user.mention_html()}!",
    reply_markup=ForceReply(selective=True),
  )


async def help_command(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
  """Send a message when the command /help is issued."""
  await update.message.reply_text("Hamma Gyan!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  """Echo the user message."""
  await update.message.reply_text(update.message.text)

class ImageEdit:
  def edge_dection(self,image):
    FILE_NAME = 'geeks.png'
    # Read image from disk.
    img = cv.imread(FILE_NAME)
    # Canny edge detection.
    edges = cv.Canny(img, 100, 200) 
    #Write image back to disk.
    cv.imshow('Edges', edges)
    cv.waitKey(0)
    cv.destroyAllWindows()

async def echo_image(update, context):
  user = update.message.from_user
  image_file = await update.message.photo[-1].get_file()
  await image_file.download_to_drive("userphoto.jpg")
  logger.info("Photo of %s: %s", user.first_name, "userphoto.jpg")
  path = 'userphoto.jpg'
  image = cv.imread(path)
  window_name = 'Image'
  font = cv.FONT_HERSHEY_SIMPLEX
  org = (50, 50)
  fontScale = 1
  color = (255, 0, 0)
  thickness = 2
  image = cv.putText(image, 'hamma gyan', org, font,fontScale, color, thickness, cv.LINE_AA)
  cv.imwrite('userphoto.jpg', image)
  # cv.imshow(window_name, image)
  # cv.waitKey(0)
  await context.bot.send_photo(chat_id=update.message.chat_id,
                               photo=open('userphoto.jpg' , "rb"))


def main() -> None:
  """Start the bot."""
  # Create the Application and pass it your bot's token.
  application = Application.builder().token(Token).build()

  # on different commands - answer in Telegram
  application.add_handler(CommandHandler("start", start))
  application.add_handler(CommandHandler("help", help_command))

  # on non command i.e message - echo the message on Telegram
  application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,
                                         echo))
  application.add_handler(MessageHandler(filters.PHOTO, echo_image))

  # Run the bot until the user presses Ctrl-C
  application.run_polling()


if __name__ == "__main__":
  main()