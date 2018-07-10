FROM alpine:3.7

COPY /server /code
WORKDIR /code

EXPOSE 8000

RUN apk update && \
    apk upgrade && \
    apk add python3 && \
    python3 -m pip install --upgrade --no-cache-dir pip && \
    python3 -m pip install --upgrade --no-cache-dir -r requirements.txt && \
    python3 manage.py migrate && \
    python3 manage.py loaddata fixtures/initial.json
