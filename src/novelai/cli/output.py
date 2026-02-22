"""Rich output helpers for the CLI."""

from rich.console import Console

console = Console()
err_console = Console(stderr=True)


def info(message: str) -> None:
    console.print(message)


def success(message: str) -> None:
    console.print(f"[bold green]{message}[/bold green]")


def warn(message: str) -> None:
    console.print(f"[yellow]{message}[/yellow]")


def fail(message: str) -> None:
    err_console.print(f"[bold red]{message}[/bold red]")
