FROM python:3.7

WORKDIR /deps
COPY requirements.txt /tmp/
RUN set -xe && \
    pip install -r /tmp/requirements.txt -t . && \
    true

COPY mocking_spongebob /app/mocking_spongebob
COPY tests /app/tests
