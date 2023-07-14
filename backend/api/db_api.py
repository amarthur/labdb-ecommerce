import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dao import daos, repos
from flask import Flask, current_app, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/api/create', methods=['POST'])
def create():
    data = request.get_json()
    entity_class = data.get('entity')
    entity_data = data.get('data')

    entity_dao = get_entity_dao(entity_class)
    entity_dao.create(entity_data)


@app.route('/api/update', methods=['POST'])
def update():
    data = request.get_json()
    entity_class = data.get('entity')
    entity_id = data.get('entity_id')
    entity_data = data.get('data')

    entity_dao = get_entity_dao(entity_class)
    entity_dao.update(entity_id, entity_data)


@app.route('/api/delete', methods=['POST'])
def delete():
    data = request.get_json()
    entity_class = data.get('entity')
    entity_id = data.get('entity_id')

    entity_dao = get_entity_dao(entity_class)
    entity_dao.delete(entity_id)


@app.route('/api/get', methods=['POST'])
def get():
    data = request.get_json()
    entity_class = data.get('entity')
    entity_id = data.get('entity_id')

    entity_dao = get_entity_dao(entity_class)
    return jsonify(entity_dao.get(entity_id))


def get_repo(repo_name, repo_url, RepoClass):
    if repo_name not in current_app.config:

        file_path = os.path.join(os.path.dirname(__file__), 'urls.json')
        with open(file_path, 'r') as file:
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


def get_entity_dao(entity_class):
    sql_repo = get_sql_repo()
    neo_repo = get_neo_repo()
    mongo_repo = get_mongo_repo()

    if entity_class == "Carrier":
        return daos.CarrierDAO(sql_repo)
    elif entity_class == "Seller":
        return daos.SellerDAO(sql_repo)
    elif entity_class == "Product":
        return daos.ProductDAO(sql_repo, neo_repo)
    elif entity_class == "User":
        return daos.UserDAO(sql_repo, neo_repo, mongo_repo)


if __name__ == "__main__":
    app.run()
