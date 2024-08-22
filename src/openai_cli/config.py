import os

DEFAULT_MODEL = "gpt-4o-mini"
MAX_TOKENS = 500
TEMPERATURE = 0.23
SYSTEM_MESSAGE = "You are a helpful assistant."


def get_openai_api_key() -> str:
    """
    Retrieves the OpenAI API key from the environment.

    Returns:
        str: The OpenAI API key, or an empty string if not set.
    """
    return os.getenv("OPENAI_API_KEY", "")


def set_openai_api_key(api_key: str) -> None:
    """
    Sets the OpenAI API key in the environment.

    Args:
        api_key (str): The API key to set.
    """
    os.environ["OPENAI_API_KEY"] = api_key
