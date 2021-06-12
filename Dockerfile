FROM python:3
ENV PYTHONBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN set -eux \
    && apt update \
    && apt install -y libgdal-dev \
    && pip install -r requirements.txt
COPY . /app/
