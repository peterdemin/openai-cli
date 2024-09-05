import unittest
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from openai_cli.cli import cli
from openai_cli.config import DEFAULT_MODEL, MAX_TOKENS, TEMPERATURE


# Mock the API_BASE_URL to prevent actual API calls
@patch("openai_cli.client.API_BASE_URL", "http://mock-api-url")
@patch("openai_cli.client.requests.Session", autospec=True)
class TestCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch("openai_cli.cli.generate_response")
    def test_complete_command(self, mock_generate, mock_session):
        mock_generate.return_value = "Mocked response"
        result = self.runner.invoke(cli, ["complete", "-"], input="Test prompt")
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Mocked response", result.output)
        mock_generate.assert_called_once_with(
            "Test prompt",
            conversation_history=[
                {"role": "user", "content": "Test prompt"},
                {"role": "assistant", "content": "Mocked response"},
            ],
            model=DEFAULT_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
        )

    @patch("openai_cli.cli.generate_response")
    def test_repl_command(self, mock_generate, mock_session):
        mock_generate.return_value = "Mocked response"
        result = self.runner.invoke(cli, ["repl"], input="Test prompt\nexit\n")
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Mocked response", result.output)
        self.assertIn("Interactive shell ended.", result.output)
        mock_generate.assert_called_once_with(
            "Test prompt",
            conversation_history=[
                {"role": "user", "content": "Test prompt"},
                {"role": "assistant", "content": "Mocked response"},
            ],
            model=DEFAULT_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
        )

    @patch("openai_cli.cli.generate_response")
    def test_model_option(self, mock_generate, mock_session):
        mock_generate.return_value = "Mocked response"
        result = self.runner.invoke(
            cli, ["-m", "gpt-3.5-turbo", "complete", "-"], input="Test prompt"
        )
        self.assertEqual(result.exit_code, 0)
        mock_generate.assert_called_once_with(
            "Test prompt",
            conversation_history=[
                {"role": "user", "content": "Test prompt"},
                {"role": "assistant", "content": "Mocked response"},
            ],
            model="gpt-3.5-turbo",
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
        )

    @patch("openai_cli.cli.generate_response")
    def test_max_tokens_option(self, mock_generate, mock_session):
        mock_generate.return_value = "Mocked response"
        result = self.runner.invoke(cli, ["-k", "100", "complete", "-"], input="Test prompt")
        self.assertEqual(result.exit_code, 0)
        mock_generate.assert_called_once_with(
            "Test prompt",
            conversation_history=[
                {"role": "user", "content": "Test prompt"},
                {"role": "assistant", "content": "Mocked response"},
            ],
            model=DEFAULT_MODEL,
            max_tokens=100,
            temperature=TEMPERATURE,
        )

    @patch("openai_cli.cli.generate_response")
    def test_temperature_option(self, mock_generate, mock_session):
        mock_generate.return_value = "Mocked response"
        result = self.runner.invoke(cli, ["-p", "0.8", "complete", "-"], input="Test prompt")
        self.assertEqual(result.exit_code, 0)
        mock_generate.assert_called_once_with(
            "Test prompt",
            conversation_history=[
                {"role": "user", "content": "Test prompt"},
                {"role": "assistant", "content": "Mocked response"},
            ],
            model=DEFAULT_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=0.8,
        )

    @patch("openai_cli.cli.set_openai_api_key")
    @patch("openai_cli.cli.generate_response")
    def test_token_option(self, mock_generate, mock_set_key, mock_session):
        mock_generate.return_value = "Mocked response"
        result = self.runner.invoke(cli, ["-t", "test_token", "complete", "-"], input="Test prompt")
        self.assertEqual(result.exit_code, 0)
        mock_set_key.assert_called_once_with("test_token")
        mock_generate.assert_called_once_with(
            "Test prompt",
            conversation_history=[
                {"role": "user", "content": "Test prompt"},
                {"role": "assistant", "content": "Mocked response"},
            ],
            model=DEFAULT_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
        )
        self.assertIn("Mocked response", result.output)


if __name__ == "__main__":
    unittest.main()
