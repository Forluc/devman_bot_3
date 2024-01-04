import random

import vk_api as vk
from environs import Env
from vk_api.longpoll import VkEventType, VkLongPoll

from tg_bot import get_detect_intent_texts, get_google_credentials

env = Env()
env.read_env()

vk_api_key = env.str('VK_API_KEY')


def sending_dialogflow_messages(event, vk_api):
    reply_text = get_detect_intent_texts(
        project_id=get_google_credentials()['quota_project_id'],
        session_id=event.user_id,
        text=event.text,
        language_code='ru'
    )

    vk_api.messages.send(
        user_id=event.user_id,
        message=reply_text,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    vk_session = vk.VkApi(token=vk_api_key)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            sending_dialogflow_messages(event, vk_api)
