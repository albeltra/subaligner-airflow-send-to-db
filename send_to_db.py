import pymongo
import os

user = os.environ.get('MONGO_USER', 'root')
password = os.environ.get('MONGO_PASSWORD')
host = os.environ.get('MONGO_HOST')
port = os.environ.get('MONGO_PORT', '27017')

database = os.environ.get('DB')
collec = os.environ.get('COLLECTION')

if all([user, password, host, port]):
    client = 
pymongo.MongoClient(f'mongodb://{user}:{password}@{host}:{port}')
    if database and collec:
        db = getattr(client)
        collection = getattr(db, collec)
        record = {}
        for key, value in os.environ.items():
            if key.startswith('SUBALIGNER_'):
                clean_key = key.copy().replace('SUBALIGNER_', '')
                record[clean_key] = value
        collection.insert_one(record)
    else:
        raise Exception('Must specify mongo db and collection names!')
else:
    raise Exception('Must specify mongo auth parameters!')
