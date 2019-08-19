FROM python:3.7.4

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN pip install --upgrade pip
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

COPY . /code/
