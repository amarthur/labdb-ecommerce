from flask import Flask, request, jsonify
from database_connections import sql_cursor, mongo_db, neo4j_driver
app = Flask(__name__)

@app.route('/query', methods=['GET'])
def run_query():
    db_type = request.args.get('db')  # get the db type from request arguments
    query = request.args.get('query')  # get the query from request arguments
    return allocate_request(db_type, query)

def allocate_request(db_type, query):
    if db_type == "sql":
        result =  data_from_sql(query)
    elif db_type == "mongo":
        result =  data_from_mongo(query)
    elif db_type == "neo4j":
        result =  data_from_neo4j(query)
    else:
        return jsonify({"error": "Invalid database type."})
    return jsonify({"result": result})

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

