import json

import daos
import repos
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/api/start', methods=['POST'])
def start():
    with open('./urls.json', 'r') as file:
        config = json.load(file)

    SQL_URL = config['sql_url']
    NEO_URL = config['neo_url']
    MONGO_URL = config['mongo_url']

    sql_repo = repos.SQLRepository(SQL_URL)
    neo_repo = repos.NeoRepository(NEO_URL)
    mongo_repo = repos.MongoRepository(MONGO_URL)

    sql_repo.create_connection()
    neo_repo.create_connection()
    mongo_repo.create_connection()


@app.route('/api/create', methods=['POST'])
def create():
    data = request.get_json()
    entity = data.get('entity')
    entity_data = data.get('data')

    if entity == "Carrier":
        carrier_dao = daos.CarrierDAO(repos.sql_repo)
        carrier_dao.create(entity_data)
    elif entity == "Seller":
        seller_dao = daos.SellerDAO(repos.sql_repo)
        seller_dao.create(entity_data)
    elif entity == "Product":
        product_dao = daos.ProductDAO(repos.sql_repo, repos.neo_repo)
        product_dao.create(entity_data)
    elif entity == "User":
        entity_dao = daos.UserDAO(repos.sql_repo, repos.neo_repo, repos.mongo_repo)
        entity_dao.create(entity_data)


if __name__ == "__main__":
    app.run()
