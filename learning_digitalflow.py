import json

from environs import Env
from google.cloud import dialogflow

from google_dialogflow_api import get_google_credentials


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def main():
    env = Env()
    env.read_env()

    questions = env.str('QUESTIONS', 'questions.json')
    with open(questions, 'r') as file:
        questions_json = file.read()

    questions = json.loads(questions_json)

    for intent, value in questions.items():
        create_intent(
            project_id=get_google_credentials()['quota_project_id'],
            display_name=intent,
            training_phrases_parts=value['questions'],
            message_texts=[value['answer']],
        )


if __name__ == '__main__':
    main()
