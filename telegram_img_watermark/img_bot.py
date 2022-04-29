import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, \
    Filters, CallbackContext, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from img_playground import make_watermark
import io

# TestImage78bot

TOKEN = '5025388636:AAGYoKcekA651jA65C6gLIDiMaWGal9-GiA'


class Image_handler:
    flag = None
    text_for_image = None
    image_stream = None
    image_name = None

    @staticmethod
    def get_updated_photo(text):
        Image_handler.text_for_image = text
        return make_watermark(Image_handler.image_stream, Image_handler.image_name, Image_handler.text_for_image)




def start(update, context):
    keyboard = [
        [KeyboardButton("Create watermark on image", callback_data='1')],
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard)

    update.message.reply_text('Hello', reply_markup=reply_markup)


def image_handler(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter a text for watermark")

    file = update.message.photo[-1].file_id
    img = context.bot.getFile(file)
    Image_handler.image_stream = img.download_as_bytearray()
    Image_handler.image_name = img.file_path.split('.')[-1]

    Image_handler.flag = 'watermark'

    context.bot.send_message(chat_id=update.effective_chat.id, text="The watermark is successful installed")


def text_handler(update: Update, context: CallbackContext):
    if Image_handler.flag == 'watermark' and update.message.text:
        if len(update.message.text) <= 15:
            context.bot.send_photo(chat_id=update.effective_chat.id,
                                   photo=Image_handler.get_updated_photo(update.message.text))
            Image_handler.flag = ''
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Текст не доджен превышать 15 символов. Попробуй еще раз.")


def img_button(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please choose an image")

    query = update.callback_query
    query.answer()


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    updater = Updater(token=TOKEN)
    disp = updater.dispatcher

    disp.add_handler(CallbackQueryHandler(img_button))
    disp.add_handler(CommandHandler('start', start))
    disp.add_handler(MessageHandler(Filters.photo | Filters.attachment, image_handler))
    disp.add_handler(MessageHandler(Filters.text, text_handler))

    updater.start_polling()


if __name__ == '__main__':
    main()
