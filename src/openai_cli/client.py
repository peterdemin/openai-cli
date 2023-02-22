import requests

class CompletionClient:
    MAX_TOKENS = 1000
    TEMPERATURE = 0.1
    TIMEOUT = 60

    def __init__(self, token: str, session: requests.Session, proxy: str, api_url: str) -> None:
        self._headers = {"Authorization": f"Bearer {token}"}
        self._session = session
        self._api_url = api_url
        self._proxy = proxy

        if len(self._proxy) > 0:
            self._session.proxies = {
                "http": f"http://{self._proxy}",
                "https": f"http://{self._proxy}",
            }


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
            self._api_url,
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


def build_completion_client(token: str, api_url: str, proxy: str) -> CompletionClient:
    return CompletionClient(token=token, session=requests.Session(), proxy=proxy, api_url=api_url)
