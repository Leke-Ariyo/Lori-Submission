FROM python:3.8.0-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
RUN mkdir /app
WORKDIR /app
# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev

# copy and install python dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt


# copy the source code
COPY . /app/