import json

from pymongo import MongoClient


def insert_data_into_collection(db, collection_name, drop_then_insert=True):
    json_data_file = f"./data/{collection_name}.json"
    collection = db[collection_name]
    if drop_then_insert:
        collection.drop()

    with open(json_data_file, 'r') as f:
        json_data = json.load(f)

    collection.insert_many(json_data)


def main():
    DB = "ecommerce"
    collections = ["avaliacoesEmpresas", "avaliacoesProdutos"]

    client = MongoClient()
    db = client[DB]

    for collection in collections:
        insert_data_into_collection(db, collection)


if __name__ == "__main__":
    main()
