FROM public.ecr.aws/sam/build-python3.9

WORKDIR /deps

COPY dev-requirements.txt /tmp
RUN set -xe && \
    pip install -r /tmp/dev-requirements.txt && \
    true

COPY requirements.txt /tmp/
RUN set -xe && \
    pip install -r /tmp/requirements.txt -t . && \
    find . -name __pycache__ -type d | xargs rm -rf && \
    true

COPY mocking_spongebob /app/mocking_spongebob
COPY tests /app/tests
