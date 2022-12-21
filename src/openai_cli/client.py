import requests


class CompletionClient:
    API_URL = "https://api.openai.com/v1/completions"
    MAX_TOKENS = 1000
    TEMPERATURE = 0.1
    TIMEOUT = 60

    def __init__(self, token: str, model:str, session: requests.Session) -> None:
        self._headers = {"Authorization": f"Bearer {token}"}
        self._session = session
        self.model = model

    def generate_response(self, prompt: str, model: str = "text-davinci-003") -> str:
        if self.model:
            model = self.model
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
