import logging

import telegram
from environs import Env
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from google_dialogflow_api import (get_detect_intent_texts,
                                   get_google_credentials)
from logger import TelegramLogsHandler

logger = logging.getLogger(__file__)


def start_handler(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Здравствуйте, {update.effective_user.full_name}')


def text_handler(update: Update, context: CallbackContext) -> None:
    reply_text = get_detect_intent_texts(
        project_id=get_google_credentials()['quota_project_id'],
        session_id=update.effective_user.id,
        text=update.message.text,
        language_code=update.effective_user.language_code,
    )

    update.message.reply_text(reply_text.reply_text.query_result.fulfillment_text)


def main() -> None:
    env = Env()
    env.read_env()

    bot_token = env.str('TG_BOT_API')
    tg_chat_id_log = env.str('TG_CHAT_ID_LOG')

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger.addHandler(TelegramLogsHandler(telegram.Bot(token=bot_token), tg_chat_id_log))

    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_handler))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), text_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
