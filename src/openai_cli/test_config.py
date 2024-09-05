import unittest
from unittest.mock import patch

from openai_cli.config import get_openai_api_key, set_openai_api_key


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


if __name__ == "__main__":
    unittest.main()
