import json
import logging

from google.cloud import dialogflow

logger = logging.getLogger(__file__)


def get_google_credentials(google_application_credentials) -> dict:
    with open(google_application_credentials, 'r') as file:
        return json.loads(file.read())


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

    return response
