import logging
import random

import vk_api as vk
from environs import Env
from google.cloud import dialogflow
from vk_api.longpoll import VkEventType, VkLongPoll

from tg_bot import get_google_credentials
import telegram

env = Env()
env.read_env()

vk_api_key = env.str('VK_API_KEY')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__file__)


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


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

    if not response.query_result.intent.is_fallback:
        return response.query_result.fulfillment_text


def sending_dialogflow_messages(event, vk_api) -> None:
    reply_text = get_detect_intent_texts(
        project_id=get_google_credentials()['quota_project_id'],
        session_id=event.user_id,
        text=event.text,
        language_code='ru'
    )
    if reply_text:
        vk_api.messages.send(
            user_id=event.user_id,
            message=reply_text,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    bot_token = env.str('TG_BOT_API')
    tg_chat_id_log = env.str('TG_CHAT_ID_LOG')

    logger.info('Старт бота Вконтакте')
    logger.addHandler(TelegramLogsHandler(telegram.Bot(token=bot_token), tg_chat_id_log))

    vk_session = vk.VkApi(token=vk_api_key)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            sending_dialogflow_messages(event, vk_api)
