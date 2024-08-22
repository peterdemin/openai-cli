import unittest
from unittest.mock import patch, MagicMock
import openai
from openai_cli.client import generate_response, initialize_openai_client

class TestClient(unittest.TestCase):
    @patch('openai_cli.client.openai.chat.completions.create')
    def test_generate_response_success(self, mock_create):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Mocked response"
        mock_create.return_value = mock_response

        response = generate_response("Test prompt")
        self.assertEqual(response, "Mocked response")
        mock_create.assert_called_once()

    @patch('openai_cli.client.openai.chat.completions.create')
    def test_generate_response_error(self, mock_create):
        mock_create.side_effect = Exception("API Error")

        with self.assertRaises(Exception):
            generate_response("Test prompt")

    @patch('openai_cli.client.get_openai_api_key')
    def test_initialize_openai_client_success(self, mock_get_key):
        mock_get_key.return_value = "test_api_key"
        initialize_openai_client()
        self.assertEqual(openai.api_key, "test_api_key")

    @patch('openai_cli.client.get_openai_api_key')
    def test_initialize_openai_client_no_key(self, mock_get_key):
        mock_get_key.return_value = ""
        with self.assertRaises(openai.OpenAIError):
            initialize_openai_client()

if __name__ == '__main__':
    unittest.main()
