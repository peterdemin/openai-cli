import requests


class CompletionClient:
    API_URL = "https://api.openai.com/v1/completions"
    MAX_TOKENS = 1000
    TEMPERATURE = 0.1
    TIMEOUT = 60

    def __init__(self, token: str, session: requests.Session) -> None:
        self._headers = {"Authorization": f"Bearer {token}"}
        self._session = session

    def generate_response(self, prompt: str, model: str) -> str:
        """Generates response from a given prompt using a specified model.

        Args:
            prompt: The prompt to generate a response for.
            model: The model to use for generating the response.
                   Defaults to "text-davinci-003".

        Returns:
            The generated response.
        """
        response = self._session.post(
            self.API_URL,
            headers=self._headers,
            json={
                "prompt": prompt,
                "model": model,
                "max_tokens": self.MAX_TOKENS,
                "temperature": self.TEMPERATURE,
            },
            timeout=self.TIMEOUT,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["text"].strip()


def build_completion_client(token: str) -> CompletionClient:
    return CompletionClient(token=token, session=requests.Session())
