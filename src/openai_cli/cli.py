import io
import click
from typing import Optional
from openai_cli.client import generate_response, OpenAIError
from openai_cli.config import DEFAULT_MODEL, MAX_TOKENS, TEMPERATURE, set_openai_api_key


@click.group()
@click.option('-m', '--model', default=DEFAULT_MODEL, help=f"OpenAI model option. (default: {DEFAULT_MODEL})")
@click.option('-k', '--max-tokens', type=int, default=MAX_TOKENS, help=f"Maximum number of tokens in the response. (default: {MAX_TOKENS})")
@click.option('-p', '--temperature', type=float, default=TEMPERATURE, help=f"Temperature for response generation. (default: {TEMPERATURE})")
@click.option("-t", "--token", help="OpenAI API token")
@click.pass_context
def cli(ctx, model: str, max_tokens: int, temperature: float, token: Optional[str]):
    """CLI for interacting with OpenAI's completion API."""
    ctx.ensure_object(dict)
    ctx.obj['model'] = model
    ctx.obj['max_tokens'] = max_tokens
    ctx.obj['temperature'] = temperature
    ctx.obj['conversation_history'] = []
    if token:
        set_openai_api_key(token)


@cli.command()
@click.argument("source", type=click.File("rt", encoding="utf-8"))
@click.pass_context
def complete(ctx, source: io.TextIOWrapper) -> None:
    """Return OpenAI completion for a prompt from SOURCE."""
    prompt = source.read()
    try:
        result = generate_response(
            prompt, 
            conversation_history=ctx.obj['conversation_history'], 
            model=ctx.obj['model'],
            max_tokens=ctx.obj['max_tokens'],
            temperature=ctx.obj['temperature']
        )
        click.echo(result)
        ctx.obj['conversation_history'].extend([
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": result}
        ])
    except OpenAIError as e:
        click.echo(f"An error occurred: {str(e)}", err=True)


@cli.command()
@click.pass_context
def repl(ctx) -> None:
    """Start interactive shell session for OpenAI completion API."""
    click.echo(f"Interactive shell started. Using model: {ctx.obj['model']}")
    click.echo(f"Max tokens: {ctx.obj['max_tokens']}, Temperature: {ctx.obj['temperature']}")
    click.echo("Type 'exit' or use Ctrl-D to exit.")

    while True:
        try:
            prompt = click.prompt("Prompt", type=str)
            if prompt.lower() == 'exit':
                break
            result = generate_response(
                prompt, 
                conversation_history=ctx.obj['conversation_history'], 
                model=ctx.obj['model'],
                max_tokens=ctx.obj['max_tokens'],
                temperature=ctx.obj['temperature']
            )
            click.echo(f"\nResponse:\n{result}\n")
            ctx.obj['conversation_history'].extend([
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": result}
            ])
        except click.exceptions.Abort:
            break
        except OpenAIError as e:
            click.echo(f"An error occurred: {str(e)}", err=True)

    click.echo("Interactive shell ended.")


if __name__ == "__main__":
    cli()