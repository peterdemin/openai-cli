OpenAI command-line client
==========================

Installation
------------

To install OpenAI CLI in Python virtual environment, run::

    pip install openai-cli

Token authentication
--------------------

OpenAI API requires authentication token, which can be obtained on this page:
https://beta.openai.com/account/api-keys

Provide token to the CLI either through a command-line argument (``-t/--token <TOKEN>``)
or through an environment variable (``OPENAI_API_TOKEN``).

Usage
-----

Currently only text completion API is supported.

Example usage::

    $ echo "Are cats faster than dogs?" | openai complete -
    It depends on the breed of the cat and dog. Generally,
    cats are faster than dogs over short distances,
    but dogs are better at sustained running.

Interactive mode supported (Press Ctrl+C to exit)::

    $ openai repl
    Prompt: Can generative AI replace humans?

    No, generative AI cannot replace humans.
    While generative AI can be used to automate certain tasks,
    it cannot replace the creativity, intuition, and problem-solving
    skills that humans possess.
    Generative AI can be used to supplement human efforts,
    but it cannot replace them.

    Prompt: ^C

Run without arguments to get a short help message::

    $ openai
    Usage: openai [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      complete  Return OpenAI completion for a prompt from SOURCE.
      repl      Start interactive shell session for OpenAI completion API.
