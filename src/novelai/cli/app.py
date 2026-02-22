"""CLI application entrypoint."""

from __future__ import annotations

import sys

from dotenv import load_dotenv

from novelai import NovelAI

from .generation import (
    generate_from_request_json,
    generate_standard,
    generate_streaming,
)
from .interactive import interactive_loop
from .output import fail
from .parser import build_parser, parse_args


def main() -> None:
    """Main entry point."""
    load_dotenv()

    parser = build_parser()
    args = parse_args(parser)

    try:
        client = NovelAI()
    except Exception as e:
        fail(f"Error: Failed to initialize NovelAI client: {e}")
        fail("Make sure NOVELAI_API_KEY is set in your environment or .env file")
        sys.exit(1)

    try:
        if args.interactive:
            interactive_loop(client, args, parser)
            return

        if args.request_json or args.request_json_stdin:
            generate_from_request_json(client, args)
            return

        if args.stream:
            generate_streaming(client, args)
        else:
            generate_standard(client, args)
    finally:
        client.close()
