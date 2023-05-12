FROM python:3.10-alpine

RUN mkdir /scripts

COPY ./send_to_db.py /scripts/

RUN pip install pymongo
