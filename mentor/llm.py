from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

_client = None

def get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
    return _client



def get_response(messages: list[dict]) -> str:
    """
    Get a response from the Gemini API using the provided messages.
    
    Args:
        messages (list[dict]): The list of messages to send to the model.

    Returns:
        str: The response from the Gemini API.
    """
    client = get_client()

    response = client.chat.completions.create(
        model="gemini-3.1-flash-lite",
        messages= messages
    )

    return response.choices[0].message.content
