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