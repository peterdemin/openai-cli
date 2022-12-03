import io
import os

import click
import requests


@click.group()
def cli():
    pass


@cli.command()
@click.argument('source', type=click.File('rt', encoding='utf-8'))
@click.option('-t', '--token', default='', help='OpenAI API token')
def complete(source: io.TextIOWrapper, token: str) -> None:
    """Execute CODE on SOURCE."""
    token = token or os.environ.get('OPENAI_API_TOKEN', '')
    if not token:
        click.exceptions.MissingParameter(
            'Either --token option or OPENAI_API_TOKEN '
            'environment variable must be provided',
        )
    client = ChatGptClient(token)
    prompt = source.read()
    result = client.generate_response(prompt)
    click.echo(result)


@cli.command()
@click.option('-t', '--token', default='', help='OpenAI API token')
def repl(token: str) -> None:
    """Execute CODE on SOURCE."""
    token = token or os.environ.get('OPENAI_API_TOKEN', '')
    if not token:
        click.exceptions.MissingParameter(
            'Either --token option or OPENAI_API_TOKEN '
            'environment variable must be provided',
        )
    client = ChatGptClient(token)
    while True:
        print(client.generate_response(input('Enter prompt: ')))


class ChatGptClient:
    def __init__(self, api_key: str):
        # Set the API key
        self.api_key = api_key

        # Set the API endpoint URL
        self.api_url = 'https://api.openai.com/v1/completions'

    def generate_response(self, prompt: str, model: str = 'text-davinci-003') -> str:
        # Set the request headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
        }

        # Set the request payload
        payload = {
            'prompt': prompt,
            'model': model,
            'temperature': 0.5,
            'max_tokens': 100,
        }

        # Send the request to the API endpoint
        response = requests.post(
            self.api_url,
            headers=headers,
            json=payload,
            timeout=60,
        )

        # Check the response status code
        if response.status_code != 200:
            # Handle the error here
            pass

        # Get the response text
        return response.json()['choices'][0]['text']


if __name__ == '__main__':
    cli()
