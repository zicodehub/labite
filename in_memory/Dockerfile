FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app/

RUN apt-get update -y 

RUN pip3 install "fastapi[all]"


COPY ./ /app
COPY ./start.sh /app

ENV PYTHONPATH=/app