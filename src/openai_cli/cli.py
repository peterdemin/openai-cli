import io
import click
from typing import Optional
from openai_cli.client import generate_response
from openai_cli.config import DEFAULT_MODEL, set_openai_api_key


@click.group()
@click.option('-m', '--model', default=DEFAULT_MODEL, help=f"OpenAI model option. (default: {DEFAULT_MODEL})")
@click.option("-t", "--token", help="OpenAI API token")
@click.pass_context
def cli(ctx, model: str, token: Optional[str]):
    """CLI for interacting with OpenAI's completion API."""
    ctx.ensure_object(dict)
    ctx.obj['model'] = model
    if token:
        set_openai_api_key(token)


@cli.command()
@click.argument("source", type=click.File("rt", encoding="utf-8"))
@click.pass_context
def complete(ctx, source: io.TextIOWrapper) -> None:
    """Return OpenAI completion for a prompt from SOURCE."""
    prompt = source.read()
    result = generate_response(prompt, ctx.obj['model'])
    click.echo(result)


@cli.command()
@click.pass_context
def repl(ctx) -> None:
    """Start interactive shell session for OpenAI completion API."""
    click.echo(f"Interactive shell started. Using model: {ctx.obj['model']}")
    click.echo("Type 'exit' or use Ctrl-D to exit.")

    while True:
        try:
            prompt = click.prompt("Prompt", type=str)
            if prompt.lower() == 'exit':
                break
            result = generate_response(prompt, ctx.obj['model'])
            click.echo(f"\nResponse:\n{result}\n")
        except click.exceptions.Abort:
            break
        except Exception as e:
            click.echo(f"An error occurred: {str(e)}", err=True)

    click.echo("Interactive shell ended.")


if __name__ == "__main__":
    cli()
