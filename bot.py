import json
import logging

from environs import Env
from google.cloud import dialogflow
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

env = Env()
env.read_env()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__file__)


def get_detect_intent_texts(project_id: str, session_id: str, text: str, language_code: str) -> str:
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    logger.info(f'Session path: {session}')

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={'session': session, 'query_input': query_input})

    logger.info(f'Query text: {response.query_result.query_text}')
    logger.info(
        f'Detected intent: {response.query_result.intent.display_name}'
        f'(Confidence: {response.query_result.intent_detection_confidence})'
    )
    logger.info(f'Fulfillment text: {response.query_result.fulfillment_text}')

    return response.query_result.fulfillment_text


def get_google_credentials() -> dict:
    with open(env.str('GOOGLE_APPLICATION_CREDENTIALS'), 'r') as file:
        return json.loads(file.read())


def start_handler(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Здравствуйте, {update.effective_user.full_name}')


def text_handler(update: Update, context: CallbackContext) -> None:
    reply_text = get_detect_intent_texts(
        project_id=get_google_credentials()['quota_project_id'],
        session_id=update.effective_user.id,
        text=update.message.text,
        language_code=update.effective_user.language_code
    )

    update.message.reply_text(reply_text)


def main() -> None:
    bot_token = env.str('TG_BOT_API')

    updater = Updater(bot_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_handler))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), text_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
