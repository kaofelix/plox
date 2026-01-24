import argparse
import sys
from functools import singledispatch
from pathlib import Path

from packaging.tags import interpreter_name

from plox import interpreter
from plox.ast_printer import ast_printer
from plox.parser import Parser
from plox.scanner import Scanner, Token, TokenType

had_error = False
had_runtime_error = False


def run_file(file: Path):
    content = file.read_text()
    run(content)
    if had_error:
        sys.exit(65)

    if had_runtime_error:
        sys.exit(70)


def run_prompt():
    while True:
        try:
            line = input("> ")
        except EOFError:
            print("Exiting...")
            break

        run(line)
        had_error = False


def run(source: str):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens)
    expression = parser.parse()

    if had_error or expression is None:
        return

    interpreter.interpret(expression)


def runtime_error(error: RuntimeError):
    token, message = error.args
    print(message + "\n[line " + token.line + "]")
    had_runtime_error = True


@singledispatch
def error(line: int, message: str):
    report(line, "", message)


@error.register
def _(token: Token, message: str):
    if token.type == TokenType.EOF:
        report(token.line, "at end", message)
    else:
        report(token.line, f"at '{token.lexeme}'", message)


def report(line: int, where: str, message: str):
    print(f"[line {line}] Error {where}: {message}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(description="Process a single file")
    parser.add_argument("file", nargs="?", type=str, help="Path to the input file")

    args = parser.parse_args()

    if args.file:
        run_file(args.file)
    else:
        run_prompt()


if __name__ == "__main__":
    main()
