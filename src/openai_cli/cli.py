import io
import os

import click

from openai_cli.client import build_completion_client


@click.group()
def cli():
    pass


@cli.command()
@click.argument("source", type=click.File("rt", encoding="utf-8"))
@click.option("-t", "--token", default="", help="OpenAI API token")
@click.option('-m', "--model", default="", help="OpenAI model option")
def complete(source: io.TextIOWrapper, token: str, model: str) -> None:
    """Return OpenAI completion for a prompt from SOURCE."""
    client = build_completion_client(token = get_token(token), model = get_model(model))
    prompt = source.read()
    result = client.generate_response(prompt)
    click.echo(result)


@cli.command()
@click.option("-t", "--token", default="", help="OpenAI API token")
@click.option('-m', "--model", default="", help="OpenAI model option")
def repl(token: str, model: str) -> None:
    """Start interactive shell session for OpenAI completion API."""
    client = build_completion_client(token = get_token(token), model = get_model(model))
    while True:
        print(client.generate_response(input("Prompt: ")))
        print()

def get_model(model: str) -> str:
    if not model:
        model = os.environ.get("OPENAI_MODEL", "")
    if not model: 
        print("OPENAI_MODEL environment variable not set. Defaulting to text-davinci-003")
    return model

def get_token(token: str) -> str:
    if not token:
        token = os.environ.get("OPENAI_API_TOKEN", "")
    if not token:
        raise click.exceptions.UsageError(
            message=(
                "Either --token option or OPENAI_API_TOKEN environment variable must be provided"
            )
        )
    return token


if __name__ == "__main__":
    cli()
