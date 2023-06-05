"""Dataclass to hold information about the LLM engine to use."""
from dataclasses import dataclass


@dataclass
class LLMEngine:
    """Hold information about the LLM engine to use."""

    use_openai: bool
    model_engine: str

    def __init__(
        self, use_openai: bool = False, model_engine: str = "declare-lab/flan-alpaca-xl"
    ):
        """Initialize the LLMEngine dataclass.

        Args:
            use_openai (bool, optional): Whether to use OpenAI's API or not. Defaults to False.
            model_engine (str, optional): Name of the hugginface model to use. Defaults to "declare-lab/flan-alpaca-xl".
        """
        self.use_openai = use_openai
        if self.use_openai:
            model_engine = "text-davinci-002"  # ChatGPT4
        else:
            self.model_engine = model_engine
