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

ENV APP_HOME=/app

RUN groupadd -g $GROUP_ID vv_user \
    && useradd -u $USER_ID -g vv_user -s /bin/bash -d ${APP_HOME} vv_user \
    && mkdir -p ${APP_HOME} \
    && mkdir -p ${APP_HOME}/static \
    && mkdir -p ${APP_HOME}/media \
    && chown -R vv_user:vv_user ${APP_HOME}

# Install the project requirements.
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install --no-root

COPY ./docker/containers/dev/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY . ${APP_HOME}

# Use user "vv_user" to run the build commands below and the server itself.
USER vv_user

# Use /app folder as a directory where the source code is stored.
WORKDIR ${APP_HOME}

ENTRYPOINT [ "/entrypoint.sh" ]
