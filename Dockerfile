FROM python:3.10.0-slim-bullseye

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive \
 apt-get install -y \
 python3-pip \
 python3-venv \
 ssh \
 git \ 
 ffmpeg \
 libsm6 \
 libxext6 \
 libpq-dev
 
RUN pip3 install poetry

# Activate a virtual environment to keep dependencies isolated
# Add venv to path to make it the default python
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# Set up SSH:
ARG SSH_PRIVATE_KEY
RUN mkdir /root/.ssh/
RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

WORKDIR /app

# Install dependencies:
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --no-root

# Install package:
COPY generativedm generativedm
RUN poetry install

# Copy files for pre-commit:
COPY .pre-commit-config.yaml .flake8 ./
COPY .git .git

ARG VERSION
ENV VERSION=$VERSION

# Don't buffer Python stdout (logs)
ENV PYTHONUNBUFFERED 1
ENV ECS_AVAILABLE_LOGGING_DRIVERS="awslogs"

# Set entrypoint:
ENTRYPOINT [ "generativedm" ]
CMD [ "--help" ]