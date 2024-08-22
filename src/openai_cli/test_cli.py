import unittest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from openai_cli.cli import cli

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch('openai_cli.cli.generate_response')
    def test_complete_command(self, mock_generate):
        mock_generate.return_value = "Mocked response"
        result = self.runner.invoke(cli, ['complete', '-'], input='Test prompt')
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Mocked response", result.output)
        mock_generate.assert_called_once_with('Test prompt', 'gpt-4o-mini')

    @patch('openai_cli.cli.generate_response')
    def test_repl_command(self, mock_generate):
        mock_generate.return_value = "Mocked response"
        result = self.runner.invoke(cli, ['repl'], input='Test prompt\nexit\n')
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Mocked response", result.output)
        self.assertIn("Interactive shell ended.", result.output)

    def test_model_option(self):
        with patch('openai_cli.cli.generate_response') as mock_generate:
            mock_generate.return_value = "Mocked response"
            result = self.runner.invoke(cli, ['-m', 'gpt-3.5-turbo', 'complete', '-'], input='Test prompt')
            self.assertEqual(result.exit_code, 0)
            mock_generate.assert_called_once_with('Test prompt', 'gpt-3.5-turbo')

    @patch('openai_cli.cli.set_openai_api_key')
    def test_token_option(self, mock_set_key):
        result = self.runner.invoke(cli, ['-t', 'test_token', 'complete', '-'], input='Test prompt')
        self.assertEqual(result.exit_code, 0)
        mock_set_key.assert_called_once_with('test_token')

if __name__ == '__main__':
    unittest.main()
