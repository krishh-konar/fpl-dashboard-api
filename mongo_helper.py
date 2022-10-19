from dotenv import dotenv_values

ENV_VARS = dotenv_values(".env")

def insertIntoCollection(client, collection_name, doc):
    collection = client[ENV_VARS["MONGO_FPL_DB_NAME"]][collection_name]
    _id = collection.insert_one(doc)
    return _id

def delete_from_mongo():
    pass

def isDocInCollection(client, key, value, collection_name):
    collection = client[ENV_VARS["MONGO_FPL_DB_NAME"]][collection_name]
    details = collection.find_one({key : value})

    if details:
        return (True, details)
    else:
        return (False, [])

