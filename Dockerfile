FROM python:3.10.7-slim-buster

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
    libxml2-dev \
    libxmlsec1-dev \
    gcc \
    python-dev \
    libpq-dev \
    mime-support \
    telnet \
    iputils-ping \
    curl \
    htop \
    vim \
    procps \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/statics /app/log/{uwsgi,gunicorn,uvicorn}

WORKDIR /app

COPY services/noti_service/pyproject.toml /app/

RUN --mount=type=cache,target=/root/.cache/pip,id=scc/sop/backend-service/services/noti_service pip3 install --upgrade pip \
    && pip3 install poetry \
    && poetry config virtualenvs.in-project true \
    && poetry install

# copy neccessary files
COPY core /app/core
COPY services/noti_service/. /app/
RUN chmod +x /app/scripts/*.sh

EXPOSE 5002

CMD ["sh", "/app/scripts/run_service.sh"]
