import json

import daos
import repos
from flask import Flask, current_app, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def get_repo(repo_name, repo_url, RepoClass):
    if repo_name not in current_app.config:
        with open('./urls.json', 'r') as file:
            config = json.load(file)

        repo_url = config[repo_url]
        current_app.config[repo_name] = RepoClass(repo_url)
        current_app.config[repo_name].create_connection()

    return current_app.config[repo_name]


def get_sql_repo():
    return get_repo('sql_repo', 'sql_url', repos.SQLRepository)


def get_neo_repo():
    return get_repo('neo_repo', 'neo_url', repos.NeoRepository)


def get_mongo_repo():
    return get_repo('mongo_repo', 'mongo_url', repos.MongoRepository)


@app.route('/api/start', methods=['POST'])
def start():
    get_sql_repo()
    get_neo_repo()
    get_mongo_repo()


@app.route('/api/create', methods=['POST'])
def create():
    sql_repo = get_sql_repo()
    neo_repo = get_neo_repo()
    mongo_repo = get_mongo_repo()

    data = request.get_json()
    entity = data.get('entity')
    entity_data = data.get('data')

    if entity == "Carrier":
        carrier_dao = daos.CarrierDAO(sql_repo)
        carrier_dao.create(entity_data)
    elif entity == "Seller":
        seller_dao = daos.SellerDAO(sql_repo)
        seller_dao.create(entity_data)
    elif entity == "Product":
        product_dao = daos.ProductDAO(sql_repo, neo_repo)
        product_dao.create(entity_data)
    elif entity == "User":
        entity_dao = daos.UserDAO(sql_repo, neo_repo, mongo_repo)
        entity_dao.create(entity_data)


if __name__ == "__main__":
    app.run()
