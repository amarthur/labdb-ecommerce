import psycopg2
from neo4j import GraphDatabase
from pymongo import MongoClient

NEO_4J_PORT = 7687
MONGO_DB_PORT = 27017
SQL_PORT = 5432

neo4j_driver = GraphDatabase.driver(f"bolt://localhost:{NEO_4J_PORT}", auth=("neo4j", "password"))

mongo_client = MongoClient(f'mongodb://localhost:{MONGO_DB_PORT}/')
mongo_db = mongo_client['ecommerce-documentos']

sql_conn = psycopg2.connect(
    host="localhost",
    port=SQL_PORT,
    database="testdb",
    user="postgres",
    password="secretpassword"
)

sql_cursor = sql_conn.cursor()
