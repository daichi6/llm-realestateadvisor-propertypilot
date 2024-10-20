import vertexai
from vertexai.preview.generative_models import GenerativeModel, ChatSession
import vertexai.preview.generative_models as generative_models

vertexai.init(project = "adsp-capstone-property-pilot", location = "us-central1")
model = GenerativeModel("gemini-1.5-pro")


def start_chat_session() -> ChatSession:
    """
    Starts and returns a new chat session with the generative model.

    :return: ChatSession - An active chat session with the generative model.
    """
    return model.start_chat(response_validation=False)


def get_chat_response(chat: ChatSession, prompt: str) -> str:
    """
    Sends a prompt to the chat session and returns the full response.

    :param chat: ChatSession - An active chat session with the generative model.
    :param prompt: str - The user's input or query for which a response is requested.
    :return: str - The full concatenated response from the chat model.
    """
    text_response = []
    responses = chat.send_message(prompt, stream=True)
    for chunk in responses:
        text_response.append(chunk.text)
    return "".join(text_response)
