FROM python:3.8.4

WORKDIR /deps

COPY dev-requirements.txt /tmp
RUN set -xe && \
    pip install -r /tmp/dev-requirements.txt && \
    true

COPY requirements.txt /tmp/
RUN set -xe && \
    pip install -r /tmp/requirements.txt -t . && \
    true

COPY mocking_spongebob /app/mocking_spongebob
COPY tests /app/tests
