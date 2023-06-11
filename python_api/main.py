from flask import Flask
from database_connections import sql_cursor, mongo_db, neo4j_driver
app = Flask(__name__)

@app.route('/api', methods=['GET'])
def get_data():
    # Pull data from SQL database
    # Pull data from Neo4j graph database
    # Pull data from MongoDB document database
    # Pull data from Redis key-value database
    # Combine and return data3
    raise NotImplementedError

def data_from_sql(query):
    sql_cursor.execute(query)
    res = sql_cursor.fetchall()
    return res 

def data_from_mongo(collection, query):
    res = mongo_db[collection].find(query)
    return res

def data_from_neo4j(query):
    with neo4j_driver.session() as session:
        data_from_neo4j = session.run(query)
    return data_from_neo4j


if __name__ == "__main__":
    app.run(debug=True)

