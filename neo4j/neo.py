from neo4j import GraphDatabase


def CreateQueries(relation_name, creation_query):
    csv_path = f"file:///data/{relation_name}.csv"
    csv_query = f"LOAD CSV WITH HEADERS FROM '{csv_path}' AS row"
    rel_query = f"CREATE (x)-[:{relation_name}]->(y)"

    full_query = f"{csv_query}{creation_query}{rel_query}"
    return full_query


def TemSubcategoria():
    query = """
    MERGE (x:Categoria {id: toInteger(row.id_categoria), nome: row.categoria})
    MERGE (y:Categoria {id: toInteger(row.id_subcategoria), nome: row.subcategoria})
    """
    return query


def PertenceA():
    query = """
    MERGE (x:Produto {id: toInteger(row.id_produto), nome: row.produto})
    MERGE (y:Categoria {id: toInteger(row.id_categoria)})
    """
    return query


def Busca():
    query = """
    MERGE (x:Usuario {id: toInteger(row.id_usuario)})
    MERGE (y:Produto {id: toInteger(row.id_produto)})
    """
    return query


def Deseja():
    query = """
    MERGE (x:Usuario {id: toInteger(row.id_usuario)})
    MERGE (y:Produto {id: toInteger(row.id_produto)})
    """
    return query


def RecomendadoPara():
    query = """
    MERGE (x:Produto {id: toInteger(row.id_produto)})
    MERGE (y:Usuario {id: toInteger(row.id_usuario)})
    """
    return query


def Faz():
    query = """
    MERGE (x:Usuario {id: toInteger(row.id_usuario)})
    MERGE (y:Pedido {id: toInteger(row.id_pedido)})
    """
    return query


def Contem():
    query = """
    MERGE (x:Pedido {id: toInteger(row.id_pedido)})
    MERGE (y:Produto {id: toInteger(row.id_produto)})
    """
    return query


def DeleteAll():
    query = "MATCH (n) DETACH DELETE n"
    return query


def main():
    # Queries
    delete_all = True
    rel_queries = [TemSubcategoria, PertenceA, Busca, Deseja, RecomendadoPara, Faz, Contem]
    queries = [CreateQueries(rel_query.__name__, rel_query()) for rel_query in rel_queries]

    # Driver
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "password"
    driver = GraphDatabase.driver(uri, auth=(username, password))

    with driver.session() as session:
        if delete_all:
            session.run(DeleteAll())
        for query in queries:
            session.run(query)

    driver.close()


if __name__ == "__main__":
    main()
