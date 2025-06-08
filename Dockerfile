FROM python:3-alpine

WORKDIR /usr/src/app

COPY . .

RUN python3 -m pip install -r requirements.txt --no-cache-dir