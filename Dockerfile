FROM python:3.8 as builder

ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=8000

WORKDIR /code
COPY . /code/

RUN pip install --upgrade pip \
 && pip install -r requirements.txt
CMD uvicorn app.application:app --host ${HOST} --port ${PORT} --reload