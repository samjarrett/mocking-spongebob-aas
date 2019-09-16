FROM python:3.7

WORKDIR /app
COPY requirements.txt /tmp/
RUN set -xe && \
    pip install -r /tmp/requirements.txt -t . && \
    true

COPY src /app
