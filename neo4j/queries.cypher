MATCH (u:Usuario)-[r:Faz]->(p:Pedido)-[:Contem]->(pr:Produto)
RETURN u, p, pr

MATCH (u:Usuario)-[r:Deseja]->(p:Produto)
RETURN u, p

MATCH (c:Categoria {nome:"Moda"})-[r:TemSubcategoria]->(s:Categoria)
RETURN c, s

MATCH (c:Categoria)-[r:TemSubcategoria]->(s:Categoria)<-[:PertenceA]-(p:Produto)
RETURN c, s, p

MATCH (p:Produto)-[:PertenceA]->(c:Categoria)<-[r:TemSubcategoria*]-(s:Categoria)
RETURN p, c, s

