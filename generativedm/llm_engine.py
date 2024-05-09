"""Dataclass to hold information about the LLM engine to use."""
import os
import torch
from dataclasses import dataclass
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig


hf_token = os.getenv("HF_TOKEN")


@dataclass
class LLMEngine:
    """Hold information about the LLM engine to use."""

    use_openai: bool
    model_engine: str

    def __init__(
        self, use_openai: bool = False, model_engine: str = "mistralai/Mistral-7B-Instruct-v0.2"
    ):
        """Initialize the LLMEngine dataclass.

        Args:
            use_openai (bool, optional): Whether to use OpenAI's API or not. Defaults to False.
            model_engine (str, optional): Name of the hugginface model to use. Defaults to "mistralai/Mistral-7B-Instruct-v0.2".
        """
        self.use_openai = use_openai
        if self.use_openai:
            self.model = "text-davinci-002"  # ChatGPT4
        else:
            self.torch_device = "cuda" if torch.cuda.is_available() else "cpu"
            self.tokenizer = AutoTokenizer.from_pretrained(model_engine)
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                model_engine, 
                device_map=self.torch_device, 
                quantization_config=bnb_config, 
                token=hf_token
            )