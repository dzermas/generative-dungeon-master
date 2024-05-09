"""CLI entrypoints through ``click`` bindings."""
import logging
import json
from datetime import datetime
from pathlib import Path

import click

import generativedm
from generativedm.llm_engine import LLMEngine
from generativedm.simulate import simulate
from generativedm.pkg_utils.text_generation import generate


@click.group()
@click.option(
    "--log_level",
    type=click.Choice(["DEBUG", "INFO", "WARNING"]),
    default="INFO",
    help="Set logging level for both console and file",
)
def cli(log_level):
    """CLI entrypoint."""
    Path("logs").mkdir(parents=True, exist_ok=True)
    _ = logging.basicConfig(
        filename=f"logs/simulation_log_{datetime.now().strftime('%m-%d-%Y_%H:%M:%S')}.log",
        level=log_level,
    )


@cli.command()
def version():
    """Print application version."""
    print(f"{generativedm.__version__}")


@cli.command()
@click.option(
    "--config_file",
    required=False,
    type=str,
    help="Path to the world initialization configuration file",
    default="config/simulation_config.json",
)
@click.option(
    "--simulation_days",
    required=False,
    type=int,
    help="The number of days to simulate the world. Default is 10.",
    default=10,
)
@click.option("--use_openai", is_flag=True, help="Whether to use OpenAI or not")
@click.option(
    "--model_engine",
    required=False,
    type=str,
    help="Name of the text generation model",
    default="mistralai/Mistral-7B-Instruct-v0.2",
)
def generate_world(config_file, simulation_days, use_openai, model_engine):
    """Execute the Phandalin demo."""
    logger = logging.getLogger(__name__)
    logger.info("Starting simulation...")
    logger.info(f"Using config file: {config_file}")
    logger.info(f"Using simulation days: {simulation_days}")
    logger.info(f"Using OpenAI: {use_openai}")
    logger.info(f"Using model engine: {model_engine}")
    simulate(
        config_file=config_file,
        simulation_days=simulation_days,
        use_openai=use_openai,
        model_engine=model_engine,
    )


@cli.command()
@click.option(
    "--prompt_file",
    required=False,
    type=str,
    help="Path to the world initialization configuration file",
    default="config/prompt_file.json",
)
@click.option(
    "--model_engine",
    required=False,
    type=str,
    help="Name of the text generation model",
    default="mistralai/Mistral-7B-Instruct-v0.2",
)
def generate_text(prompt_file, model_engine):
    """Execute the Phandalin demo."""
    logger = logging.getLogger(__name__)
    logger.info("Starting simulation...")
    logger.info(f"Using prompt file: {prompt_file}")
    logger.info(f"Using model engine: {model_engine}")
    with open(prompt_file) as f:
        json_data = json.load(f)
    llm_engine = LLMEngine(use_openai=False, model_engine=model_engine)
    response = generate(
        prompt=json_data,
        llm_engine=llm_engine,
    )
    print(response)


if __name__ == "__main__":
    cli()
