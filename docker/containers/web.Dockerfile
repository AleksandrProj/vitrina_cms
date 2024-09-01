# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.11-slim-buster

ARG USER_ID
ENV USER_ID ${USER_ID}

ARG GROUP_ID
ENV GROUP_ID ${GROUP_ID}

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    vim \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip \
    && pip install poetry==1.8.3 \
    && poetry config virtualenvs.create false


RUN groupadd -g $GROUP_ID wagtail \
    && useradd -u $USER_ID -g wagtail -s /bin/bash -d /app wagtail \
    && mkdir -p /app \
    && chown wagtail:wagtail /app

# Install the project requirements.
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install --no-root

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Collect static files.
# RUN python manage.py collectstatic --noinput --clear

CMD set -xe; python manage.py migrate --noinput; python manage.py runserver 0.0.0.0:8000
