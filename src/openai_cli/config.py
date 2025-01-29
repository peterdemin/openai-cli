import os

DEFAULT_MODEL = "gpt-4o-mini"
MAX_TOKENS = 500
TEMPERATURE = 0.23
SYSTEM_MESSAGE = "You are a helpful assistant."
DEFAULT_API_BASE_URL = "https://api.openai.com/v1/chat/completions"


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


def get_openai_api_url() -> str:
    """
    Retrieves the OpenAI API URL from the environment.

    Returns:
        str: The OpenAI API URL, or the default URL if not set.
    """
    return os.getenv("OPENAI_API_URL") or DEFAULT_API_BASE_URL


def set_openai_api_url(api_url: str) -> None:
    """
    Sets the OpenAI API URL in the environment.

    Args:
        api_url (str): The API URL to set.
    """
    os.environ["OPENAI_API_URL"] = api_url
