import pymongo
import os
import json
import ast
from datetime import datetime

user = os.environ.get('MONGO_USER', 'root')
password = os.environ.get('MONGO_PASSWORD')
host = os.environ.get('MONGO_HOST')
port = os.environ.get('MONGO_PORT', '27017')

database = os.environ.get('DB')
collec = os.environ.get('COLLECTION')
kind = os.environ.get('KIND')

dataPath = ast.literal_eval(os.environ.get("dataPath"))['path'] if os.environ.get("mediaFile") else None

if all([user, password, host, port]):
    if database and collec:
        client = pymongo.MongoClient(f'mongodb://{user}:{password}@{host}:{port}')
        db = getattr(client, database)
        collection = getattr(db, collec)
        record = {}
        for key, value in os.environ.items():
            if key.startswith('SUBALIGNER_'):
                clean_key = key.replace('SUBALIGNER_', '')
                try:
                    value = float(value)
                except ValueError:
                    pass
                record[clean_key] = value

        now = datetime.now()
        record['date'] = now

        record_short = {}
        for key, value in record.items():
            if 'path' not in key and 'ANALYTICS_MONGODB' not in key:
                record_short[key] = value

        record_short['kind'] = kind

        collection.insert_one(record_short)

    else:
        raise Exception('Must specify mongo db and collection names!')
else:
    raise Exception('Must specify mongo auth parameters!')
