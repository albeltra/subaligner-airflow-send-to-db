import pymongo
import os
import json
import ast

user = os.environ.get('MONGO_USER', 'root')
password = os.environ.get('MONGO_PASSWORD')
host = os.environ.get('MONGO_HOST')
port = os.environ.get('MONGO_PORT', '27017')

database = os.environ.get('DB')
collec = os.environ.get('COLLECTION')

mediaFile = ast.literal_eval(os.environ.get("mediaFile")) if os.environ.get("mediaFile") else None
mediaInfo = ast.literal_eval(os.environ.get("mediaInfo")) if os.environ.get("mediaInfo") else None

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
        if mediaFile:
            record["mediaFile"] = mediaFile
        if mediaInfo:
            record["mediaInfo"] = mediaInfo

        collection.insert_one(record)

        collection = getattr(db, collec + '_short')
        record_short = {}
        for key, value in record.items():
            if 'path' not in key and 'ANALYTICS_MONGODB' not in key:
                record_short[key] = value
        if mediaFile:
            record_short["releaseGroup"] = mediaFile.get("releaseGroup", "")
            if "movieId" in mediaFile:
                record_short["kind"] = "movie"
            else:
                record_short["kind"] = "tv"
        if mediaInfo:
            record_short["audioBitrate"] = mediaInfo.get("audioBitrate", "")
            record_short["audioChannels"] = mediaInfo.get("audioChannels", "")
            record_short["audioCodec"] = mediaInfo.get("audioCodec", "")
            record_short["audioLanguages"] = mediaInfo.get("audioLanguages", "")
            record_short["audioStreamCount"] = mediaInfo.get("audioStreamCount", "")
            record_short["videoBitDepth"] = mediaInfo.get("videoBitDepth", "")
            record_short["videoBitrate"] = mediaInfo.get("videoBitrate", "")
            record_short["videoCodec"] = mediaInfo.get("videoCodec", "")
            record_short["videoDynamicRangeType"] = mediaInfo.get("videoDynamicRangeType", "")
            record_short["videoFps"] = mediaInfo.get("videoFps", "")
            record_short["resolution"] = mediaInfo.get("resolution", "")
            record_short["runTime"] = mediaInfo.get("runTime", "")
            record_short["scanType"] = mediaInfo.get("scanType", "")
            record_short["subtitles"] = mediaInfo.get("subtitles", "")
        collection.insert_one(record_short)

    else:
        raise Exception('Must specify mongo db and collection names!')
else:
    raise Exception('Must specify mongo auth parameters!')
