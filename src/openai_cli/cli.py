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
def complete(source: io.TextIOWrapper, token: str) -> None:
    """Return OpenAI completion for a prompt from SOURCE."""
    client = build_completion_client(get_token(token))
    prompt = source.read()
    result = client.generate_response(prompt)
    click.echo(result)


@cli.command()
@click.option("-t", "--token", default="", help="OpenAI API token")
def repl(token: str) -> None:
    """Start interactive shell session for OpenAI completion API."""
    client = build_completion_client(get_token(token))
    while True:
        print(client.generate_response(input("Prompt: ")))


def get_token(token: str) -> str:
    if not token:
        token = os.environ.get("OPENAI_API_TOKEN", "")
    if not token:
        raise click.exceptions.UsageError(
            message=(
                "Either --token option or OPENAI_API_TOKEN "
                "environment variable must be provided",
            )
        )
    return token


if __name__ == "__main__":
    cli()
