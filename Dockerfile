FROM python:3.10-alpine

RUN mkdir /scripts

COPY ./sent_to_db.py /scripts/

RUN pip install pymongo

ENTRYPOINT ["python", "/scripts/send_to_db.py"]
