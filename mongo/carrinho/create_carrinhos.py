from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['my_database']

users = db["usuarios"]
carts = db["carrinhos"]
orders = db["pedidos"]

# User 1
user_data = {
    "nome": "John Doe",
    "email": "john.doe@example.com",
    "_id": "user1234",
}

user_id_1 = users.insert_one(user_data).inserted_id

# User 2
user_data = {
    "nome": "Jane Doe",
    "email": "jane.doe@example.com",
    "_id": "user1235",
}

user_id_2 = users.insert_one(user_data).inserted_id

# Cart 1 for User 1pedidos
cart_data = {
    "id_usuario": user_id_1,
    "pedidos": []
}

cart_id_1 = carts.insert_one(cart_data).inserted_id

# Cart 2 for User 2
cart_data = {
    "id_usuario": user_id_2,
    "pedidos": []
}

cart_id_2 = carts.insert_one(cart_data).inserted_id

# Order 1 for Cart 1
order_data = {
    "id_transportadora": "trns123456",
    "itens": [
        {
            "itemId": "item123456",
            "descricao": "Some description of the item"
        },
        {
            "itemId": "item123457",
            "descricao": "Some description of another item"
        }
    ]
}

order_id_1 = orders.insert_one(order_data).inserted_id

# Order 2 for Cart 1
order_data = {
    "id_transportadora": "trns123458",
    "itens": [
        {
            "itemId": "item123459",
            "descricao": "Some description of the item"
        },
        {
            "itemId": "item123460",
            "descricao": "Some description of another item"
        }
    ]
}

order_id_2 = orders.insert_one(order_data).inserted_id

# Order 3 for Cart 2
order_data = {
    "id_transportadora": "trns123461",
    "itens": [
        {
            "itemId": "item123462",
            "descricao": "Some description of the item"
        },
        {
            "itemId": "item123463",
            "descricao": "Some description of another item"
        }
    ]
}

order_id_3 = orders.insert_one(order_data).inserted_id

# Add orders to carts
carts.update_one(
    {"_id": cart_id_1},
    {"$push": {"pedidos": {"$each": [order_id_1, order_id_2]}}}
)

carts.update_one(
    {"_id": cart_id_2},
    {"$push": {"pedidos": order_id_3}}
)

# Add carts to users
users.update_one(
    {"_id": user_id_1},
    {"$set": {"carrinho": cart_id_1}}
)

users.update_one(
    {"_id": user_id_2},
    {"$set": {"carrinho": cart_id_2}}
)

# User 3
user_data = {
    "nome": "Alice Smith",
    "email": "alice.smith@example.com",
    "_id": "user1236",
}

user_id_3 = users.insert_one(user_data).inserted_id

# Cart 3 for User 3
cart_data = {
    "id_usuario": user_id_3,
    "pedidos": []
}

cart_id_3 = carts.insert_one(cart_data).inserted_id

# Order 4 for Cart 3
order_data = {
    "id_transportadora": "trns123464",
    "itens": [
        {
            "itemId": "item123465",
            "descricao": "Some description of the item"
        },
        {
            "itemId": "item123466",
            "descricao": "Some description of another item"
        }
    ]
}

order_id_4 = orders.insert_one(order_data).inserted_id

# Order 5 for Cart 3
order_data = {
    "id_transportadora": "trns123467",
    "itens": [
        {
            "itemId": "item123468",
            "descricao": "Some description of the item"
        },
        {
            "itemId": "item123469",
            "descricao": "Some description of another item"
        }
    ]
}

order_id_5 = orders.insert_one(order_data).inserted_id

# Add orders to cart
carts.update_one(
    {"_id": cart_id_3},
    {"$push": {"pedidos": {"$each": [order_id_4, order_id_5]}}}
)

# Add cart to user
users.update_one(
    {"_id": user_id_3},
    {"$set": {"carrinho": cart_id_3}}
)

# User 4
user_data = {
    "nome": "Bob Johnson",
    "email": "bob.johnson@example.com",
    "_id": "user1237",
}

user_id_4 = users.insert_one(user_data).inserted_id

# User 5
user_data = {
    "nome": "Carol Martinez",
    "email": "carol.martinez@example.com",
    "_id": "user1238",
}

user_id_5 = users.insert_one(user_data).inserted_id

# Cart 4 for User 4
cart_data = {
    "id_usuario": user_id_4,
    "pedidos": []
}

cart_id_4 = carts.insert_one(cart_data).inserted_id

# Cart 5 for User 5
cart_data = {
    "id_usuario": user_id_5,
    "pedidos": []
}

cart_id_5 = carts.insert_one(cart_data).inserted_id

# Order 6 for Cart 4
order_data = {
    "id_transportadora": "trns123470",
    "itens": [
        {
            "itemId": "item123471",
            "descricao": "Some description of the item"
        },
    ]
}

order_id_6 = orders.insert_one(order_data).inserted_id

# Order 7 for Cart 5
order_data = {
    "id_transportadora": "trns123472",
    "itens": [
        {
            "itemId": "item123473",
            "descricao": "Some description of the item"
        },
        {
            "itemId": "item123474",
            "descricao": "Some description of another item"
        }
    ]
}

order_id_7 = orders.insert_one(order_data).inserted_id

# Add orders to carts
carts.update_one(
    {"_id": cart_id_4},
    {"$push": {"pedidos": order_id_6}}
)

carts.update_one(
    {"_id": cart_id_5},
    {"$push": {"pedidos": order_id_7}}
)

# Add carts to users
users.update_one(
    {"_id": user_id_4},
    {"$set": {"carrinho": cart_id_4}}
)

users.update_one(
    {"_id": user_id_5},
    {"$set": {"carrinho": cart_id_5}}
)
