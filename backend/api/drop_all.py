import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dao import repos


def main():
    file_path = os.path.join(os.path.dirname(__file__), 'urls.json')
    with open(file_path, 'r') as file:
        config = json.load(file)

    sql_repo = repos.SQLRepository(config['sql_url'])
    neo_repo = repos.NeoRepository(config['neo_url'])
    mongo_repo = repos.MongoRepository(config['mongo_url'])

    snm = (sql_repo, neo_repo, mongo_repo)
    for repo in snm:
        repo.drop_all()


if __name__ == "__main__":
    main()
