import argparse
import sys
from pathlib import Path

from plox.scanner import Scanner

had_error = False


def run_file(file: Path):
    content = file.read_text()
    run(content)


def run_prompt():
    while True:
        try:
            line = input("> ")
        except EOFError:
            print("Exiting...")
            break

        run(line)


def run(source: str):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    for token in tokens:
        print(token)


def error(line: int, message: str):
    report(line, "", message)


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
