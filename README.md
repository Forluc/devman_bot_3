# Боты в телеграм и ВК с нейросетью [DigitalFlow](https://dialogflow.cloud.google.com/#/getStarted)

Боты отвечают на приходящие сообщения. Берут данные из своей БД [DigitalFlow](https://dialogflow.cloud.google.com/#/getStarted). Можно обучать на [Сайте](https://dialogflow.cloud.google.com/#/getStarted) или через скрипт.
- [Ознакомиться](https://t.me/the_game_of_verb_bot) с телеграм ботом
- [Ознакомиться](https://vk.com/club224024972) с ботом Вконтакте

  ![Peek 2024-01-05 01-08](https://github.com/Forluc/devman_bot_3/assets/75582238/90f17f1d-ef87-4d4c-8008-70c0ed06653a)

  ![Peek 2024-01-05 01-13](https://github.com/Forluc/devman_bot_3/assets/75582238/1876b5a2-4dbc-46a4-b5c9-0cd10237f93d)


## Окружение

### Требования к установке

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки
зависимостей:

```bash
pip install -r requirements.txt
```
### Подготовка проекта в [DigitalFlow](https://dialogflow.cloud.google.com/#/getStarted) и получение файла с ключами от Google

1) Создайте проект в [DigitalFlow](https://dialogflow.cloud.google.com/#/getStarted). [Инструкция](https://cloud.google.com/dialogflow/es/docs/quick/setup). Вы получите идентификатор, примерно такой:
`moonlit-dynamo-211973`
2) [Создайте агента](https://cloud.google.com/dialogflow/es/docs/quick/build-agent)(Идентификатор у агента будет как в первом шаге. Выставить нужный язык) 
3) Натренируйте [DigitalFlow](https://dialogflow.cloud.google.com/#/getStarted). Создайте новый `Intent` и добавьте несколько тренировочных фраз
4) [Включите API](https://cloud.google.com/dialogflow/es/docs/quick/setup#api) DialogFlow на вашем Google-аккаунте
5) [Получите файл](https://cloud.google.com/dialogflow/es/docs/quick/setup#sdk) с ключами от вашего Google-аккаунта, credentials.json
6) [Создать токен](https://cloud.google.com/docs/authentication/api-keys) от DialogFlow.(ProjectID, , который вы получили, когда создавали проект)
7) После выполнения всех шагов заполнить файл `.env` нужными переменными(описано ниже). Python-библиотека [google-cloud-dialogflow](https://cloud.google.com/dialogflow/es/docs/reference/libraries/python)(Справочник для [DigitalFlow](https://dialogflow.cloud.google.com/#/getStarted)) 


### Добавление чувствительных данных в `.env`

Создать файл `.env` рядом с `main.py` и добавить следующее:

`GOOGLE_APPLICATION_CREDENTIALS`= Присвоить путь до файла `credentials.json`

`TG_BOT_API` = Присвоить `API-токен` телеграм бота([инструкция](https://robochat.io/docs/kak-sozdat-chat-bota-v-telegram/))

`VK_API_KEY` = Присвоить `API-ключ` группы вконтакте. ([Инструкция](https://pechenek.net/social-networks/vk/api-vk-poluchaem-klyuch-dostupa-token-gruppy/))

`TG_CHAT_ID_LOG'` = Присвоить `ID-аккаунта` телеграм куда будут приходить сообщения о логах

После заполнения данных, можно прочитать файл `.env` можно увидеть примерно следующее:

```bash
$ cat .env
TG_BOT_API='11111111:tgbotapiexample'
GOOGLE_APPLICATION_CREDENTIALS='path/to/credentials.json'
VK_API_KEY='vkapikeyexample'
TG_CHAT_ID_LOG='12345687890'
```

## Запуск ботов

Запуск бота Вконтакте на Linux(Python 3) или Windows:

```bash
$ python vk_bot.py
```

Запуск бота Телеграм на Linux(Python 3) или Windows:

```bash
$ python tg_bot.py
```

## Обучение DigitalFlow через скрипт

- Заполнить файл `questions.json` нужными данными. `Intent: {questions:[question, question, ...], answer}`
- Присвоить переменной `QUESTIONS` путь до файла с вопросами в файле `.env`(по умолчанию создать файл questions.json рядом со скриптом `learning_digitalflow.py`)
- Обязательна к заполнению в `.env` переменная `GOOGLE_APPLICATION_CREDENTIALS`(Присвоить путь до файла `credentials.json`)

### Цель проекта

Скрипт написан в образовательных целях на онлайн-курсе [Devman](https://dvmn.org)
