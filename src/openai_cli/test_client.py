import unittest
from unittest import mock

import requests

from openai_cli.client import CompletionClient, build_completion_client


class TestCompletionClient(unittest.TestCase):
    def setUp(self):
        self._token = "token"
        self._session = mock.Mock(spec_set=requests.Session)
        self._completion_client = CompletionClient(token=self._token, session=self._session)

    def test_generate_response(self):
        # Set up mock response
        self._session.post.return_value.json.return_value = {"choices": [{"text": "response"}]}

        prompt = "prompt"
        model = "model"
        response = self._completion_client.generate_response(prompt=prompt, model=model)
        self.assertEqual(response, "response")

        # Verify that the request was made with the correct parameters
        self._session.post.assert_called_with(
            self._completion_client.API_URL,
            headers={"Authorization": "Bearer token"},
            json={
                "prompt": prompt,
                "model": model,
                "max_tokens": self._completion_client.MAX_TOKENS,
                "temperature": self._completion_client.TEMPERATURE,
            },
            timeout=self._completion_client.TIMEOUT,
        )


class TestBuildCompletionClient(unittest.TestCase):
    def test_build_completion_client(self):
        completion_client = build_completion_client("token")
        self.assertIsInstance(completion_client, CompletionClient)


if __name__ == "__main__":
    unittest.main()
