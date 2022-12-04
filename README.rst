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

Build a standalone binary using pex and move it into PATH::

    $ make openai && mv openai ~/bin/
    $ openai repl
    Prompt:

Example usage
-------------

Here's an example usage scenario, where we first create a Python module
with a Fibonacci function implementation, and then generate a unit test for it:

.. code:: bash

    $ mkdir examples
    $ touch examples/__init__.py
    $ echo "Write Python function to calculate Fibonacci numbers" | openai complete - | black - > examples/fib.py
    $ (echo 'Write unit tests for this Python module named "fib":\n'; cat examples/fib.py) | openai complete - | black - > examples/test_fib.py
    $ pytest -v examples/test_fib.py
    ============================== test session starts ==============================

    examples/test_fib.py::TestFibonacci::test_eighth_fibonacci_number PASSED                                 [ 10%]
    examples/test_fib.py::TestFibonacci::test_fifth_fibonacci_number PASSED                                  [ 20%]
    examples/test_fib.py::TestFibonacci::test_first_fibonacci_number PASSED                                  [ 30%]
    examples/test_fib.py::TestFibonacci::test_fourth_fibonacci_number PASSED                                 [ 40%]
    examples/test_fib.py::TestFibonacci::test_negative_input PASSED                                          [ 50%]
    examples/test_fib.py::TestFibonacci::test_ninth_fibonacci_number PASSED                                  [ 60%]
    examples/test_fib.py::TestFibonacci::test_second_fibonacci_number PASSED                                 [ 70%]
    examples/test_fib.py::TestFibonacci::test_seventh_fibonacci_number PASSED                                [ 80%]
    examples/test_fib.py::TestFibonacci::test_sixth_fibonacci_number PASSED                                  [ 90%]
    examples/test_fib.py::TestFibonacci::test_third_fibonacci_number PASSED                                  [100%]

    =============================== 10 passed in 0.02s ==============================

    $ cat examples/fib.py

.. code:: python

    def Fibonacci(n):
        if n < 0:
            print("Incorrect input")
        # First Fibonacci number is 0
        elif n == 1:
            return 0
        # Second Fibonacci number is 1
        elif n == 2:
            return 1
        else:
            return Fibonacci(n - 1) + Fibonacci(n - 2)

.. code:: bash

    $ cat examples/test_fib.py

.. code:: python

    import unittest
    from .fib import Fibonacci


    class TestFibonacci(unittest.TestCase):
        def test_negative_input(self):
            self.assertEqual(Fibonacci(-1), None)

        def test_first_fibonacci_number(self):
            self.assertEqual(Fibonacci(1), 0)

        def test_second_fibonacci_number(self):
            self.assertEqual(Fibonacci(2), 1)

        def test_third_fibonacci_number(self):
            self.assertEqual(Fibonacci(3), 1)

        def test_fourth_fibonacci_number(self):
            self.assertEqual(Fibonacci(4), 2)

        def test_fifth_fibonacci_number(self):
            self.assertEqual(Fibonacci(5), 3)

        def test_sixth_fibonacci_number(self):
            self.assertEqual(Fibonacci(6), 5)

        def test_seventh_fibonacci_number(self):
            self.assertEqual(Fibonacci(7), 8)

        def test_eighth_fibonacci_number(self):
            self.assertEqual(Fibonacci(8), 13)

        def test_ninth_fibonacci_number(self):
            self.assertEqual(Fibonacci(9), 21)


    if __name__ == "__main__":
        unittest.main()

.. code:: bash

    $ (echo "Add type annotations for this Python code"; cat examples/fib.py) | openai complete - | black - | tee tmp && mv tmp examples/fib.py

.. code:: python

    def Fibonacci(n: int) -> int:
        if n < 0:
            print("Incorrect input")
        # First Fibonacci number is 0
        elif n == 1:
            return 0
        # Second Fibonacci number is 1
        elif n == 2:
            return 1
        else:
            return Fibonacci(n - 1) + Fibonacci(n - 2)

.. code:: bash

    $ mypy examples/fib.py
    examples/fib.py:1: error: Missing return statement  [return]
    Found 1 error in 1 file (checked 1 source file)

.. code:: bash

    $ (echo "Fix mypy warnings in this Python code"; cat examples/fib.py; mypy examples/fib.py) | openai complete - | black - | tee tmp && mv tmp examples/fib.py

.. code:: python

    def Fibonacci(n: int) -> int:
        if n < 0:
            print("Incorrect input")
        # First Fibonacci number is 0
        elif n == 1:
            return 0
        # Second Fibonacci number is 1
        elif n == 2:
            return 1
        else:
            return Fibonacci(n - 1) + Fibonacci(n - 2)
        return None  # Added return statement

.. code:: bash

    $ mypy examples/fib.py
    examples/fib.py:12: error: Incompatible return value type (got "None", expected "int")  [return-value]
    Found 1 error in 1 file (checked 1 source file)

.. code:: bash

    $ (echo "Fix mypy warnings in this Python code"; cat examples/fib.py; mypy examples/fib.py) | openai complete - | black - | tee tmp && mv tmp examples/fib.py

.. code:: python

    def Fibonacci(n: int) -> int:
        if n < 0:
            print("Incorrect input")
        # First Fibonacci number is 0
        elif n == 1:
            return 0
        # Second Fibonacci number is 1
        elif n == 2:
            return 1
        else:
            return Fibonacci(n - 1) + Fibonacci(n - 2)
        return 0  # Changed return statement to return 0

.. code:: bash

    $ mypy examples/fib.py
    Success: no issues found in 1 source file

.. code:: bash

    $ (echo "Rewrite these tests to use pytest.parametrized"; cat examples/test_fib.py) | openai complete - | black - | tee tmp && mv tmp examples/test_fib.py

.. code:: python

    import pytest
    from .fib import Fibonacci


    @pytest.mark.parametrize(
        "n, expected",
        [(1, 0), (2, 1), (3, 1), (4, 2), (5, 3), (6, 5), (7, 8), (8, 13), (9, 21), (10, 34)],
    )
    def test_fibonacci(n, expected):
        assert Fibonacci(n) == expected
