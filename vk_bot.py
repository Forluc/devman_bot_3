import logging
import random

import telegram
import vk_api as vk
from environs import Env
from vk_api.longpoll import VkEventType, VkLongPoll

from google_dialogflow_api import (get_detect_intent_texts,
                                   get_google_credentials)
from logger import TelegramLogsHandler

logger = logging.getLogger(__file__)


def sending_dialogflow_messages(event, vk_api) -> None:
    reply_text = get_detect_intent_texts(
        project_id=get_google_credentials()['quota_project_id'],
        session_id=event.user_id,
        text=event.text,
        language_code='ru',
        need_fallback=False
    )

    if not reply_text.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=reply_text.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


if __name__ == "__main__":
    env = Env()
    env.read_env()

    bot_token = env.str('TG_BOT_API')
    tg_chat_id_log = env.str('TG_CHAT_ID_LOG')
    vk_api_key = env.str('VK_API_KEY')

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger.info('Старт бота Вконтакте')
    logger.addHandler(TelegramLogsHandler(telegram.Bot(token=bot_token), tg_chat_id_log))

    vk_session = vk.VkApi(token=vk_api_key)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            sending_dialogflow_messages(event, vk_api)
