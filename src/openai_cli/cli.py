import io
import os

import click
import requests


@click.group()
def cli():
    pass


@cli.command()
@click.argument("source", type=click.File("rt", encoding="utf-8"))
@click.option("-t", "--token", default="", help="OpenAI API token")
def complete(source: io.TextIOWrapper, token: str) -> None:
    """Return OpenAI completion for a prompt from SOURCE."""
    token = token or os.environ.get("OPENAI_API_TOKEN", "")
    if not token:
        click.exceptions.MissingParameter(
            "Either --token option or OPENAI_API_TOKEN "
            "environment variable must be provided",
        )
    client = CompletionClient(token)
    prompt = source.read()
    result = client.generate_response(prompt)
    click.echo(result)


@cli.command()
@click.option("-t", "--token", default="", help="OpenAI API token")
def repl(token: str) -> None:
    """Start interactive shell session for OpenAI completion API."""
    token = token or os.environ.get("OPENAI_API_TOKEN", "")
    if not token:
        click.exceptions.MissingParameter(
            "Either --token option or OPENAI_API_TOKEN "
            "environment variable must be provided",
        )
    client = CompletionClient(token)
    while True:
        print(client.generate_response(input("Prompt: ")))


class CompletionClient:
    API_URL = "https://api.openai.com/v1/completions"
    MAX_TOKENS = 1000
    TEMPERATURE = 0.1

    def __init__(self, api_key: str) -> None:
        self._headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

    def generate_response(self, prompt: str, model: str = "text-davinci-003") -> str:
        response = requests.post(
            self.API_URL,
            headers=self._headers,
            json={
                "prompt": prompt,
                "model": model,
                "max_tokens": self.MAX_TOKENS,
                "temperature": self.TEMPERATURE,
            },
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["text"]


if __name__ == "__main__":
    cli()
