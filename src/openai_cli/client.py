from typing import Any

import openai

from .config import DEFAULT_MODEL, MAX_TOKENS, SYSTEM_MESSAGE, TEMPERATURE, get_openai_api_key


def initialize_openai_client() -> None:
    """
    Initialize the OpenAI client with the API key from the environment.

    Raises:
        openai.OpenAIError: If no API key is found in the environment.
    """
    api_key = get_openai_api_key()
    if not api_key:
        raise openai.OpenAIError(
            "The API key must be set in the OPENAI_API_KEY environment variable"
        )
    openai.api_key = api_key


def generate_response(
    prompt: str,
    model: str = DEFAULT_MODEL,
    max_tokens: int = MAX_TOKENS,
    temperature: float = TEMPERATURE,
    system_message: str = SYSTEM_MESSAGE,
) -> str:
    """
    Generates a response from a given prompt using a specified model.

    Args:
        prompt (str): The prompt to generate a response for.
        model (str): The model to use for generating the response.
        max_tokens (int): The maximum number of tokens in the response.
        temperature (float): Controls randomness in the response.
        system_message (str): The system message to set the context.

    Returns:
        str: The generated response.

    Raises:
        openai.OpenAIError: If there's an error with the OpenAI API call.
    """
    if not openai.api_key:
        initialize_openai_client()

    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return _extract_content(response)
    except openai.OpenAIError as e:
        raise openai.OpenAIError(f"Error generating response: {str(e)}") from e


def _extract_content(response: Any) -> str:
    """
    Extracts the content from the API response.

    Args:
        response (Any): The API response object.

    Returns:
        str: The extracted content.

    Raises:
        ValueError: If the response format is unexpected.
    """
    try:
        return response.choices[0].message.content.strip()
    except AttributeError as e:
        raise ValueError(f"Unexpected response format: {str(e)}") from e
