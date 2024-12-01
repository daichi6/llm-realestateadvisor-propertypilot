import vertexai
from vertexai.preview.generative_models import GenerativeModel, ChatSession
import vertexai.preview.generative_models as generative_models
from vertexai.generative_models import SafetySetting, HarmCategory, HarmBlockThreshold

# Configure safety settings
safety_config = [
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=HarmBlockThreshold.OFF,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=HarmBlockThreshold.OFF,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=HarmBlockThreshold.OFF,
    ),
]

vertexai.init(project = "adsp-capstone-property-pilot", location = "us-central1")
model = GenerativeModel("gemini-1.5-flash-002", safety_settings=safety_config)


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
    try:
        text_response = []
        responses = chat.send_message(prompt, stream=True)
        for chunk in responses:
            if hasattr(chunk, 'text'):
                text_response.append(chunk.text)
        return "".join(text_response)
    except ValueError as e:
        print(f"Error occurred: {e}")
        # Return a fallback response
        return "I'm sorry, but your question was detected to contain harmful or personally identifiable information. To protect our users and your privacy, I cannot provide an answer to that specific query. Please remove any harmful or personally identifiable information and try again."
