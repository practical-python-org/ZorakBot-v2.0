FROM python:3.11.6-slim-bullseye AS builder-image
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY src /code/src

RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt /code/
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "src/__main__.py"]