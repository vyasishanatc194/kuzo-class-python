# pull official base image
FROM python:3


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /app

ADD . /app
 
COPY ./requirements /app/requirements
#COPY ./requirements/local.txt /usr/src/app/requirements/local.txt

RUN pip install -r requirements/local.txt

# copy project
COPY . /app