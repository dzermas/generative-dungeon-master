"""Text interaction with OpenAI API and Hugging Face models.""" ""
import os
import re

import openai
import torch
from dotenv import load_dotenv
from transformers import pipeline

# Load environment variables from .env file
load_dotenv("config/.env")

# Get OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate(prompt, llm_engine):
    """
    Generate a text completion for a given prompt using either the OpenAI GPT-3 API or the Hugging Face GPT-3 model.

    Args:
    - prompt (str): The text prompt to generate a completion for.
    - llm_engine (LLMEngine): A boolean flag indicating whether to use the OpenAI API (True) or the Hugging Face GPT-3 model (False).

    Returns:
    - str: The generated text completion.
    """
    if llm_engine.use_openai:
        response = openai.Completion.create(
            engine=llm_engine.model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        message = response.choices[0].text
        return message.strip()

    else:
        torch_device = "cuda" if torch.cuda.is_available() else "cpu"
        hf_generator = pipeline(
            "text-generation", model=llm_engine.model_engine, device=torch_device
        )
        output = hf_generator(prompt, max_length=len(prompt) + 128, do_sample=True)
        out = output[0]["generated_text"]
        if "### Response:" in out:
            out = out.split("### Response:")[1]
        if "### Instruction:" in out:
            out = out.split("### Instruction:")[0]
        return out.strip()


def get_rating(x):
    """
    Extract a rating from a string.

    Args:
    - x (str): The string to extract the rating from.

    Returns:
    - int: The rating extracted from the string, or None if no rating is found.
    """
    nums = [int(i) for i in re.findall(r"\d+", x)]
    if len(nums) > 0:
        return min(nums)
    else:
        return None


# Summarize simulation loop with OpenAI GPT-4
def summarize_simulation(log_output):
    """Summarize the simulation loop.

    Args:
        log_output (str): The log output to summarize.

    Returns:
        str: The summary of the simulation loop.
    """
    prompt = f"Summarize the simulation loop:\n\n{log_output}"
    response = generate(prompt)
    return response
