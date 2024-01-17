import logging

import telegram
from environs import Env
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from google_dialogflow_api import (get_detect_intent_texts,
                                   get_google_credentials)
from logger import TelegramLogsHandler

logger = logging.getLogger(__file__)


class DialogFlowFlowBot:

    def __init__(self, token, google_application_credentials):
        self.google_creds = google_application_credentials

        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher

        self.dispatcher.add_handler(CommandHandler('start', self.start_handler))
        self.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), self.text_handler))

    def start_handler(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'Здравствуйте, {update.effective_user.full_name}')

    def text_handler(self, update, context):
        reply_text = get_detect_intent_texts(
            project_id=get_google_credentials(self.google_creds)['quota_project_id'],
            session_id=update.effective_user.id,
            text=update.message.text,
            language_code=update.effective_user.language_code,
        )

        context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text.query_result.fulfillment_text)


if __name__ == '__main__':
    env = Env()
    env.read_env()

    bot_token = env.str('TG_BOT_API')
    tg_chat_id_log = env.str('TG_CHAT_ID_LOG')
    google_application_credentials = env.str('GOOGLE_APPLICATION_CREDENTIALS')

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger.addHandler(TelegramLogsHandler(telegram.Bot(token=bot_token), tg_chat_id_log))

    bot = DialogFlowFlowBot(token=bot_token, google_application_credentials=google_application_credentials)
    bot.updater.start_polling()
    bot.updater.idle()
