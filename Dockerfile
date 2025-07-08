# pull official base image
FROM python:3.13-slim

# set working directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat-openbsd gcc postgresql \
  && apt-get clean

# install python dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .

# Expone el puerto en el que la aplicación escuche
EXPOSE 8000
