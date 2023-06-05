ARG BASE
FROM ${BASE}

ENV DEBIAN_FRONTEND=noninteractive


# Package management
RUN apt update && apt install -y  \
    apt-utils \
    software-properties-common

# Essentials
RUN apt update && apt install -y \
    git \
    ssh \
    tmux \
    sudo \
    nano \
    unzip \
    xterm \
    git-lfs \
    bash-completion

# Introspection
RUN apt update && apt install -y \
    gdb \
    htop \
    netdata \
    dmidecode

# Network utils
RUN apt update && apt install -y \
    jq \
    wget \
    curl \
    gnupg \
    rsync



RUN apt-get update && apt-get install -y \
  python3-pip \
  ffmpeg \
  libsm6 \
  libxext6 \
  libpq-dev

RUN pip3 install \
  poetry \
  argparse \
  argcomplete

RUN activate-global-python-argcomplete

RUN pip3 install --index-url https://download.pytorch.org/whl/cpu \
  torch \
  torchvision \
  torchaudio

RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL ' | tee -a /etc/sudoers

# # Activate a virtual environment to keep dependencies isolated
# # Add venv to path to make it the default python
# ENV VIRTUAL_ENV=/opt/venv
# RUN python3 -m venv $VIRTUAL_ENV
# ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"


# # Install dependencies:
# COPY pyproject.toml .
# COPY poetry.lock .

# # Install package:
# RUN poetry install

ARG VERSION
ENV VERSION=$VERSION

# Don't buffer Python stdout (logs)
ENV PYTHONUNBUFFERED 1

COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]

# Set entrypoint:
CMD ["bash"]