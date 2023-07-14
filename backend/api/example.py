import json
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dao import daos, repos


def update_and_get(dao, entity_id, new_data):
    dao.update(entity_id, new_data)
    x = dao.get(entity_id)
    print(x)


def ex_carriers(sql_repo):
    carriers_data = [{
        "cnpj": "1919191919191",
        "name": "Carrier X",
        "info": "Information about Carrier X",
        "contact": ["contact@example.com", "123-456-7890"],
        "location": "City X"
    }, {
        "cnpj": "282828282828",
        "name": "Carrier Y",
        "info": "Information about Carrier Y",
        "contact": ["contact@example.com", "987-654-3210"],
        "location": "City Y"
    }, {
        "cnpj": "373737373737",
        "name": "Carrier Z",
        "info": "Information about Carrier Z",
        "contact": ["contact@example.com", "555-555-5555"],
        "location": "City Z"
    }]
    carrier_dao = daos.CarrierDAO(sql_repo)
    carrier_dao.create(carriers_data)
    carrier_dao.delete('373737373737')


def ex_carriers_update(sql_repo):
    new_carrier_data = {"name": "Super Fast", "info": "Giga blaster fast carrier"}
    carrier_dao = daos.CarrierDAO(sql_repo)
    update_and_get(carrier_dao, '1919191919191', new_carrier_data)


def ex_sellers(sql_repo):
    sellers_data = [{
        "cnpj": "12345678901234",
        "name": "Seller A",
        "info": "Information about Seller A",
        "contact": ["contact@example.com", "123-456-7890"],
        "location": "City A"
    }, {
        "cnpj": "56789012345678",
        "name": "Seller B",
        "info": "Information about Seller B",
        "contact": ["contact@example.com", "987-654-3210"],
        "location": "City B"
    }, {
        "cnpj": "90123456789012",
        "name": "Seller C",
        "info": "Information about Seller C",
        "contact": ["contact@example.com", "555-555-5555"],
        "location": "City C"
    }, {
        "cnpj": "0112358132134",
        "name": "Seller D",
        "info": "Information about Seller D",
        "contact": ["contact@example.com", "666-666-666"],
        "location": "City D"
    }]
    seller_dao = daos.SellerDAO(sql_repo)
    seller_dao.create(sellers_data)
    seller_dao.delete('12345678901234')


def ex_sellers_update(sql_repo):
    new_seller_data = {"name": "Mercadao", "info": "Best seller of the west", "location": "The West"}
    seller_dao = daos.SellerDAO(sql_repo)
    update_and_get(seller_dao, '56789012345678', new_seller_data)


def ex_products(sql_repo, neo_repo):
    products_data = [{
        "product_id": 1,
        "name": "Product A",
        "brand": "Brand A",
        "description": "This is Product A",
        "manufacturer": "Manufacturer A",
        "technical_details": "Technical details of Product A",
        "image_urls": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"]
    }, {
        "product_id": 2,
        "name": "Product B",
        "brand": "Brand B",
        "description": "This is Product B",
        "manufacturer": "Manufacturer B",
        "technical_details": "Technical details of Product B",
        "image_urls": ["https://example.com/image3.jpg", "https://example.com/image4.jpg"]
    }, {
        "product_id": 3,
        "name": "Product C",
        "brand": "Brand C",
        "description": "This is Product C",
        "manufacturer": "Manufacturer C",
        "technical_details": "Technical details of Product C",
        "image_urls": ["https://example.com/image5.jpg", "https://example.com/image6.jpg"]
    }]
    product_dao = daos.ProductDAO(sql_repo, neo_repo)
    product_dao.create(products_data)
    product_dao.delete(3)


def ex_products_update(sql_repo, neo_repo):
    new_product_data = {"name": "Ultra Wide Tv", "description": "Kilometers of Tv", "brand": "Samzong"}
    product_dao = daos.ProductDAO(sql_repo, neo_repo)
    update_and_get(product_dao, 1, new_product_data)


def ex_users(sql_repo, neo_repo, mongo_repo):
    users_data = [{
        'cpf': '00011100011',
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'password': 'password1',
        'phone_number': ['1234567890', '9876543210'],
        'addresses': ['123 Main St', '456 Elm St'],
    }, {
        'cpf': '22244422244',
        'name': 'Jane Smith',
        'email': 'jane.smith@example.com',
        'password': 'password2',
        'phone_number': ['1112223333', '4445556666'],
        'addresses': ['789 Oak St', '987 Pine St'],
    }, {
        'cpf': '50040030022',
        'name': 'Mable Marble',
        'email': 'marble@example.com',
        'password': 'password3',
        'phone_number': ['989999999'],
        'addresses': ['789 Oak St'],
    }]
    user_dao = daos.UserDAO(sql_repo, neo_repo, mongo_repo)
    user_dao.create(users_data)


def ex_users_update(sql_repo, neo_repo, mongo_repo):
    new_user_data = {"name": "Mirabelle", "email": "mirabelle@mail.com", "password": "strong_password"}
    user_dao = daos.UserDAO(sql_repo, neo_repo, mongo_repo)
    update_and_get(user_dao, '22244422244', new_user_data)


def ex_category(neo_repo):
    categories_data = [
        {
            'category_id': 1,
            'name': 'Electronics'
        },
        {
            'category_id': 2,
            'name': 'TVs'
        },
        {
            'category_id': 3,
            'name': '4K TVs'
        },
        {
            'category_id': 4,
            'name': 'Plants'
        },
    ]
    category_dao = daos.CategoryDAO(neo_repo)
    category_dao.create(categories_data)
    category_dao.delete(4)


def ex_category_update(neo_repo):
    new_category_data = {"name": "Ultra Wide TV"}
    category_dao = daos.CategoryDAO(neo_repo)
    update_and_get(category_dao, 2, new_category_data)


def ex_sales(sql_repo, neo_repo):
    sales_data = [
        {
            'cnpj': '56789012345678',
            'product_id': 2,
            'price': 10,
            'stock': 100,
            'guarantee': '1 year'
        },
        {
            'cnpj': '90123456789012',
            'product_id': 1,
            'price': 100,
            'stock': 1,
            'guarantee': '10 years'
        },
        {
            'cnpj': '0112358132134',
            'product_id': 1,
            'price': 11,
            'stock': 0,
            'guarantee': '3 months'
        },
        {
            'cnpj': '0112358132134',
            'product_id': 2,
            'price': 115,
            'stock': 3,
            'guarantee': '10 years'
        },
    ]
    seller_dao = daos.SellerDAO(sql_repo)
    for sales_data in sales_data:
        seller_dao.add_sale(sales_data)

    seller_dao.remove_sale('90123456789012', 1)
    sales = seller_dao.get_sales('0112358132134')
    print(sales)

    product_dao = daos.ProductDAO(sql_repo, neo_repo)
    sellers = product_dao.get_sellers(1)
    print(sellers)


def ex_promotion(sql_repo):
    promotion_data = [
        {
            'cnpj': '0112358132134 ',
            'product_id': 2,
            'start_date': '2023-01-30 10:00:00',
            'finish_date': '2023-06-30 15:00:00',
            'promotion_type': '15% Off'
        },
        {
            'cnpj': '90123456789012',
            'product_id': 2,
            'start_date': '2023-01-30 10:00:00',
            'finish_date': '2023-06-30 15:00:00',
            'promotion_type': '15% Off'
        },
    ]
    seller_dao = daos.SellerDAO(sql_repo)
    for promotion in promotion_data:
        seller_dao.add_promotion(promotion)

    seller_dao.remove_promotion('90123456789012', 2)
    promotions = seller_dao.get_promotions('0112358132134')
    print(promotions)


def ex_subcategory(neo_repo):
    category_dao = daos.CategoryDAO(neo_repo)
    category_dao.add_subcategory(1, 2)
    category_dao.add_subcategory(2, 3)


def ex_product_category(sql_repo, neo_repo):
    product_dao = daos.ProductDAO(sql_repo, neo_repo)
    product_dao.add_category(1, 2)


def ex_order_has(sql_repo, neo_repo, mongo_repo):
    orders_data = [
        {
            'order_id': 1,
            'order_date': datetime(2023, 6, 29, 10, 0, 0),
            'order_status': 'Pending',
            'observations': 'Waiting for payment',
            'order_user_id': '00011100011'
        },
        {
            'order_id': 2,
            'order_date': datetime(2023, 1, 1, 10, 0, 0),
            'order_status': 'Completed',
            'observations': 'Delivered on time',
            'order_user_id': '00011100011'
        },
        {
            'order_id': 3,
            'order_date': datetime(2023, 4, 3, 2, 30, 0),
            'order_status': 'Cancelled',
            'observations': None,
            'order_user_id': '22244422244'
        },
    ]
    order_has_data = [
        {
            'order_id': 1,
            'carrier_id': '282828282828',
            'seller_id': '56789012345678',
            'product_id': 2,
            'tracking': 'yes',
            'quantity': 1,
            'shipping_fee': 10.0,
            'delivery_date': '2023-07-02 15:30:00'
        },
        {
            'order_id': 2,
            'carrier_id': '1919191919191',
            'seller_id': '0112358132134',
            'product_id': 1,
            'tracking': 'no',
            'quantity': 15,
            'shipping_fee': 2.0,
            'delivery_date': '2023-01-01 10:10:00'
        },
        {
            'order_id': 3,
            'carrier_id': '282828282828',
            'seller_id': '0112358132134',
            'product_id': 1,
            'tracking': 'no',
            'quantity': 15,
            'shipping_fee': 2.0,
            'delivery_date': '2023-01-01 10:10:00'
        },
    ]

    user_dao = daos.UserDAO(sql_repo, neo_repo, mongo_repo)
    for order, order_rel in zip(orders_data, order_has_data):
        user_dao.add_order(order, order_rel)


def ex_rating(sql_repo, neo_repo, mongo_repo):
    user_dao = daos.UserDAO(sql_repo, neo_repo, mongo_repo)
    rating_data = [
        {
            "_id": 1,
            "rating": 5,
            "date": datetime(2023, 6, 30, 10, 0, 0),
            "comment": "Fine",
        },
        {
            "_id": 2,
            "rating": 10,
            "date": datetime(2022, 3, 12, 4, 30, 0),
            "comment": "Very good",
        },
    ]
    user_dao.add_company_rating('22244422244', '1919191919191', rating_data[0])
    user_dao.add_company_rating('00011100011', '90123456789012', rating_data[1])
    user_dao.remove_rating(1)


def ex_creation_delete(sql_repo, neo_repo, mongo_repo):
    ex_carriers(sql_repo)
    ex_sellers(sql_repo)
    ex_products(sql_repo, neo_repo)
    ex_users(sql_repo, neo_repo, mongo_repo)
    ex_category(neo_repo)
    ex_rating(sql_repo, neo_repo, mongo_repo)


def ex_update_get(sql_repo, neo_repo, mongo_repo):
    ex_carriers_update(sql_repo)
    ex_sellers_update(sql_repo)
    ex_products_update(sql_repo, neo_repo)
    ex_users_update(sql_repo, neo_repo, mongo_repo)
    ex_category_update(neo_repo)


def ex_relationships(sql_repo, neo_repo, mongo_repo):
    ex_sales(sql_repo, neo_repo)
    ex_promotion(sql_repo)
    ex_subcategory(neo_repo)
    ex_product_category(sql_repo, neo_repo)
    ex_order_has(sql_repo, neo_repo, mongo_repo)


def main():
    file_path = os.path.join(os.path.dirname(__file__), 'urls.json')
    with open(file_path, 'r') as file:
        config = json.load(file)

    sql_repo = repos.SQLRepository(config['sql_url'])
    neo_repo = repos.NeoRepository(config['neo_url'])
    mongo_repo = repos.MongoRepository(config['mongo_url'])

    snm = (sql_repo, neo_repo, mongo_repo)
    ex_creation_delete(*snm)
    ex_update_get(*snm)
    ex_relationships(*snm)


if __name__ == "__main__":
    main()
