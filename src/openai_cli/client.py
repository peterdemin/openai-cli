from typing import List, Dict, Any, Optional
import requests
import json

from .config import DEFAULT_MODEL, MAX_TOKENS, SYSTEM_MESSAGE, TEMPERATURE, API_BASE_URL, get_openai_api_key

class OpenAIError(Exception):
    pass

def initialize_session() -> requests.Session:
    """
    Initialize a requests Session with the API key from the environment.

    Returns:
        requests.Session: Initialized session with API key in headers.

    Raises:
        OpenAIError: If no API key is found in the environment.
    """
    api_key = get_openai_api_key()
    if not api_key:
        raise OpenAIError("The API key must be set in the OPENAI_API_KEY environment variable")
    
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    })
    return session

def generate_response(
    prompt: str,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    model: str = DEFAULT_MODEL,
    max_tokens: int = MAX_TOKENS,
    temperature: float = TEMPERATURE,
    system_message: str = SYSTEM_MESSAGE,
) -> str:
    """
    Generates a response from a given prompt using a specified model.

    Args:
        prompt (str): The prompt to generate a response for.
        conversation_history (Optional[List[Dict[str, str]]]): Previous conversation messages.
        model (str): The model to use for generating the response.
        max_tokens (int): The maximum number of tokens in the response.
        temperature (float): Controls randomness in the response.
        system_message (str): The system message to set the context.

    Returns:
        str: The generated response.

    Raises:
        OpenAIError: If there's an error with the OpenAI API call.
    """
    session = initialize_session()

    messages = [{"role": "system", "content": system_message}]
    if conversation_history:
        messages.extend(conversation_history)
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    try:
        response = session.post(API_BASE_URL, data=json.dumps(payload))
        response.raise_for_status()
        return _extract_content(response.json())
    except requests.RequestException as e:
        raise OpenAIError(f"Error generating response: {str(e)}") from e

def _extract_content(response: Dict[str, Any]) -> str:
    """
    Extracts the content from the API response.

    Args:
        response (Dict[str, Any]): The API response object.

    Returns:
        str: The extracted content.

    Raises:
        ValueError: If the response format is unexpected.
    """
    try:
        return response['choices'][0]['message']['content'].strip()
    except (KeyError, IndexError) as e:
        raise ValueError(f"Unexpected response format: {str(e)}") from e