import unittest
from unittest.mock import MagicMock, PropertyMock, patch

import requests

from openai_cli.client import OpenAIError, generate_response, initialize_session


class TestClient(unittest.TestCase):

    @patch("openai_cli.client.requests.Session.post")
    @patch("openai_cli.client.get_openai_api_key", return_value="test_api_key")
    @patch(
        "openai_cli.client.requests.Session", autospec=True
    )  # Mocking the Session itself to prevent any real network interaction
    def test_generate_response_success(self, mock_session_cls, mock_get_key, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"choices": [{"message": {"content": "Mocked response"}}]}
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        mock_session = mock_session_cls.return_value
        mock_session.post = mock_post

        type(mock_session).headers = PropertyMock(return_value={})

        response = generate_response("Test prompt")
        self.assertEqual(response, "Mocked response")
        mock_post.assert_called_once()

    @patch("openai_cli.client.requests.Session.post")
    @patch("openai_cli.client.get_openai_api_key", return_value="test_api_key")
    @patch("openai_cli.client.requests.Session", autospec=True)
    def test_generate_response_error(self, mock_session_cls, mock_get_key, mock_post):
        mock_post.side_effect = requests.RequestException("API Error")

        mock_session = mock_session_cls.return_value
        mock_session.post = mock_post

        type(mock_session).headers = PropertyMock(return_value={})

        with self.assertRaises(OpenAIError):
            generate_response("Test prompt")

    @patch("openai_cli.client.get_openai_api_key")
    @patch("openai_cli.client.requests.Session", autospec=True)
    def test_initialize_session_success(self, mock_session_cls, mock_get_key):
        mock_get_key.return_value = "test_api_key"

        mock_session = mock_session_cls.return_value
        mock_session.headers = {}

        session = initialize_session()
        mock_session_cls.assert_called_once()
        self.assertEqual(session.headers["Authorization"], "Bearer test_api_key")

    @patch("openai_cli.client.get_openai_api_key")
    def test_initialize_session_no_key(self, mock_get_key):
        mock_get_key.return_value = ""

        with self.assertRaises(OpenAIError):
            initialize_session()


if __name__ == "__main__":
    unittest.main()
