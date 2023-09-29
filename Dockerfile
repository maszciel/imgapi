FROM python:3.9-alpine3.18

ENV PYTHONUNBUFFERED 1

# change user for production
RUN addgroup app && \
    adduser -S -G app app

WORKDIR /app

RUN mkdir /app/static

COPY requirements.txt .

RUN pip install --upgrade pip && \
    # dependencies required for postgres on alpine:
    # postgresql-client, build-base, postgresql-dev, musl-dev
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    pip install -r requirements.txt && \
    apk del .tmp-build-deps

COPY /imgapi .

EXPOSE 8000

ENV PATH="/py/bin:$PATH"