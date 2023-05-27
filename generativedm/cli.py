"""CLI entrypoints through ``click`` bindings."""

import logging

import click

import generativedm

logger = logging.basicConfig()


@click.group()
@click.option(
    "--log_level",
    type=click.Choice(["DEBUG", "INFO", "WARNING"]),
    default="INFO",
    help="Set logging level for both console and file",
)
def cli(log_level):
    """CLI entrypoint."""
    logger(log_level)


@cli.command()
def version():
    """Print application version."""
    print(f"{generativedm.__version__}")


if __name__ == "__main__":
    cli()
