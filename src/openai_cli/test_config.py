import unittest
from unittest.mock import patch

from openai_cli.config import (
    DEFAULT_API_BASE_URL,
    get_openai_api_key,
    get_openai_api_url,
    set_openai_api_key,
    set_openai_api_url,
)


class TestConfig(unittest.TestCase):
    @patch("os.getenv")
    def test_get_openai_api_key_set(self, mock_getenv):
        mock_getenv.return_value = "test_api_key"
        self.assertEqual(get_openai_api_key(), "test_api_key")

    @patch("os.getenv")
    def test_get_openai_api_key_not_set(self, mock_getenv):
        mock_getenv.return_value = ""
        self.assertEqual(get_openai_api_key(), "")

    @patch("os.environ")
    def test_set_openai_api_key(self, mock_environ):
        set_openai_api_key("new_api_key")
        mock_environ.__setitem__.assert_called_once_with("OPENAI_API_KEY", "new_api_key")

    @patch("os.getenv")
    def test_get_openai_api_url_set(self, mock_getenv):
        custom_url = "https://custom.openai.api/v1"
        mock_getenv.return_value = custom_url
        self.assertEqual(get_openai_api_url(), custom_url)

    @patch("os.getenv")
    def test_get_openai_api_url_not_set(self, mock_getenv):
        mock_getenv.return_value = None
        self.assertEqual(get_openai_api_url(), DEFAULT_API_BASE_URL)

    @patch("os.environ")
    def test_set_openai_api_url(self, mock_environ):
        custom_url = "https://custom.openai.api/v1"
        set_openai_api_url(custom_url)
        mock_environ.__setitem__.assert_called_once_with("OPENAI_API_URL", custom_url)


if __name__ == "__main__":
    unittest.main()
