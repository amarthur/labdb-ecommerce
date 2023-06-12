from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['ecommerce-documentos']

users = db["usuarios"]
carts = db["carrinhos"]
orders = db["pedidos"]

# Encontrar um usuário por ID:
id_usuario = "user1234"
usuario = users.find_one({"_id": id_usuario})
print(usuario)

# Encontrar todos os usuários:
todos_usuarios = users.find()
for usuario in todos_usuarios:
    print(usuario)

# Encontrar um carrinho por ID de usuário:
id_usuario = "user1234"
carrinho = carts.find_one({"id_usuario": id_usuario})
print(carrinho)

# Encontre o carrinho associado a um usuário específico
id_usuario = "user1234"
usuario = users.find_one({"_id": id_usuario})

id_carrinho = usuario["carrinho"]
carrinho = carts.find_one({"_id": id_carrinho})

# Encontre todos os pedidos para esse carrinho
for id_pedido in carrinho["pedidos"]:
    pedido = orders.find_one({"_id": id_pedido})
    print(pedido)

# Atualizar o nome de um usuário:
id_usuario = "user1234"
novo_nome = "John Doe"
users.update_one({"_id": id_usuario}, {"$set": {"nome": novo_nome}})

# Excluir um usuário:
id_usuario = "user1234"
users.delete_one({"_id": id_usuario})

