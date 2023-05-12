import pymongo
import os
import argparse

parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-SUBALIGNER_loss', help='Description for bar argument', required=True)
parser.add_argument('-SUBALIGNER_time_load_dataset', help='Description for bar argument', required=True)
parser.add_argument('-SUBALIGNER_video_file_path', help='Description for bar argument', required=True)
parser.add_argument('-SUBALIGNER_subtitle_file_path', help='Description for bar argument', required=True)
parser.add_argument('-SUBALIGNER_time_load_dataset', help='Description for bar argument', required=True)
parser.add_argument('-SUBALIGNER_X_shape', help='Description for bar argument', required=True)
parser.add_argument('-SUBALIGNER_time_predictions', help='Description for bar argument', required=True)
parser.add_argument('-SUBALIGNER_seconds_to_shift', help='Description for bar argument', required=True)
parser.add_argument('-SUBALIGNER_original_start', help='Description for bar argument', required=True)
parser.add_argument('-SUBALIGNER_Extension', help='Description for bar argument', required=True)
parser.add_argument('-MONGO_HOST', help='Description for bar argument', required=True)
parser.add_argument('-DB', help='Description for bar argument', required=True)
parser.add_argument('-COLLECTION', help='Description for bar argument', required=True)

args = vars(parser.parse_args())
user = args.get('MONGO_USER', 'root')
password = args.get('MONGO_PASSWORD')
host = args.get('MONGO_HOST')
port = args.get('MONGO_PORT', '27017')

database = args.get('DB')
collec = args.get('COLLECTION')

if all([user, password, host, port]):
    client = pymongo.MongoClient(f'mongodb://{user}:{password}@{host}:{port}')
    if database and collec:
        db = getattr(client, database)
        collection = getattr(db, collec)
        record = {}
        for key, value in args.items():
            if key.startswith('SUBALIGNER_'):
                clean_key = key.replace('SUBALIGNER_', '')
                record[clean_key] = value
        collection.insert_one(record)
    else:
        raise Exception('Must specify mongo db and collection names!')
else:
    raise Exception('Must specify mongo auth parameters!')
