# generative-dungeon-master
Implementation of ideas from generative agents using the power of LLM, T2S, and S2T networks.

## Linux Installation

You can locally install the package with `poetry`. This allows fast iteration and experimentation.

1. [Setup SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) for access to the repository.

2. Install ``pyenv`` - a really nice way to manage/install specific Python versions on Linux systems.

    i) Make sure you install the [build dependencies](https://github.com/pyenv/pyenv/wiki/Common-build-problems#prerequisites) for your system.

    ii) Run
    ```
    curl https://pyenv.run | bash
    ```
    iii) Restart your shell so the path changes take effect.
    ```
    exec $SHELL
    ```
    iv) Install a specific Python version (e.g. 3.8.3) with
    ```
    pyenv install 3.8.3
    ```
3. Install [`poetry`](https://python-poetry.org/docs/#installing-with-the-official-installer) for your OS.

4. Install package
    ```
    git clone git@github.com:dzermas/generative-dungeon-master.git
    cd generative-dungeon-master
    pyenv install $(cat .python-version)
    poetry install
    ```
        
5. Set up ``pre-commit`` to ensure all commits to adhere to **black** and **PEP8** style conventions.
    ```
    poetry run pre-commit install
    ```

## Execute locally with poetry

To see all options, simply use the `CLI` from the poetry environment and run:
```
poetry run generativedm --help
```

The world generation with the default parameters can be executed as:
```
poetry run generativedm generate-world
```

## Docker

The default docker image is a lightweight `python:3.8-slim-buster`. If an NVidia GPU with CUDA is available, the `nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu20.04` is usualy a good image choice to start from. Notice that in that case, the `Dockerfile` will need to change and have `torch` be installed via poetry with `poetry install -E pytorch` instead of the current `pip3` way. Build with 
```
docker build -t gdm-image .
``` 
from within the repo root folder.

Use the docker image with
```
docker run --rm -ti gdm-image poetry run generativedm generate-world
```

Note that since the text-generation model needs to be downloaded, using docker will have to download the model each time the image is opened. Maybe you should avoid using the `--rm` and have a persistent container.

## LLM Models

The code can either use an OpenAI account for inference with ChatGPT4, or HuggingFace for local inference with an open network like Alpaca. The OpenAI account charges real money for inferences and it can start getting expensive especially when the code base is not efficient enough. By default, the `use_openai` parameter in the `main.py` script is set to `False`. The HuggingFace model is downloaded locally in the `~/.cache/hub/` folder the first time it is called by the `generate()` function and every subsequent use happens by loading that local model. We can experiment with other models based on the inference capabilities of the local machines. The model selection is exposed for easy experimentation.

## Resources

Look into the Alpaca models, an open source small model that is supposed to rival ChatGPT3:

https://medium.com/@martin-thissen/llama-alpaca-chatgpt-on-your-local-computer-tutorial-17adda704c23

https://github.com/cocktailpeanut/dalai

HuggingFace has a lot of models we can try before we need to train and finetune anything:

https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads