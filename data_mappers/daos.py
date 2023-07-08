from typing import Dict, List

import map_mongo
import map_neo
import map_sql
from repos import MongoRepository, NeoRepository, SQLRepository, Transactor
from sqlalchemy import update


class SqlDAO:

    def __init__(
        self,
        sql_repo,
        entity_class,
    ):
        self.sql_repo = sql_repo
        self.entity_class = entity_class

    @staticmethod
    def ensure_list(entity_data: Dict | List[Dict]):
        return entity_data if isinstance(entity_data, list) else [entity_data]

    def create(self, entity_data: Dict | List[Dict]):
        entity_data = self.ensure_list(entity_data)
        sql_entities = [self.entity_class(**entity) for entity in entity_data]
        self.sql_repo.create(sql_entities)

    def delete(self, entity_id):
        entity = self.sql_repo.read(self.entity_class, entity_id)
        self.sql_repo.delete(entity)


class NeoDAO:

    def __init__(
        self,
        neo_repo,
        entity_class,
        entity_id_key,
    ):
        self.neo_repo = neo_repo
        self.entity_class = entity_class
        self.entity_id_key = entity_id_key

    @staticmethod
    def ensure_list(entity_data: Dict | List[Dict]):
        return entity_data if isinstance(entity_data, list) else [entity_data]

    def create(self, entity_data: Dict | List[Dict]):
        entity_data = self.ensure_list(entity_data)
        neo_entities = [self.entity_class(**entity) for entity in entity_data]
        self.neo_repo.create(neo_entities)

    def delete(self, entity_id):
        entity_id_dict = {self.entity_id_key: entity_id}
        category_node = self.neo_repo.read(self.entity_class, entity_id_dict)
        self.neo_repo.delete(category_node)


class MongoDAO:

    def __init__(
        self,
        mongo_repo,
        entity_class,
    ):
        self.mongo_repo = mongo_repo
        self.entity_class = entity_class

    @staticmethod
    def ensure_list(entity_data: Dict | List[Dict]):
        return entity_data if isinstance(entity_data, list) else [entity_data]

    def create(self, entity_data: Dict | List[Dict]):
        entity_data = self.ensure_list(entity_data)
        mongo_entities = [self.entity_class(**entity) for entity in entity_data]
        self.mongo_repo.create(mongo_entities)

    def delete(self, entity_id):
        entity = self.mongo_repo.read(self.entity_class, entity_id)
        self.mongo_repo.delete(entity)


class NeoRelator:

    def __init__(
        self,
        neo_repo,
        entity_class,
        entity_id_key,
        target_class,
        target_id_key,
        relationship_name,
    ):
        self.neo_repo = neo_repo
        self.entity_class = entity_class
        self.entity_id_key = entity_id_key
        self.target_class = target_class
        self.target_id_key = target_id_key
        self.relationship_name = relationship_name

    def relate_entities(self, entity_id_value, target_id_value, connect):
        entity_id_dict = {self.entity_id_key: entity_id_value}
        target_id_dict = {self.target_id_key: target_id_value}

        entity = self.neo_repo.read(self.entity_class, entity_id_dict)
        target = self.neo_repo.read(self.target_class, target_id_dict)
        relationship = getattr(entity, self.relationship_name)

        if connect:
            relationship.connect(target)
        else:
            relationship.disconnect(target)

    def connect_entities(self, entity_id, target_id):
        self.relate_entities(entity_id, target_id, connect=True)

    def disconnect_entities(self, entity_id, target_id):
        self.relate_entities(entity_id, target_id, connect=False)


class CarrierDAO():

    def __init__(self, sql_repo):
        self.sql_repo = sql_repo
        self.sql_dao = SqlDAO(sql_repo, map_sql.Carrier)

    def create(self, carrier_data):
        with self.sql_repo.transaction():
            self.sql_dao.create(carrier_data)

    def delete(self, carrier_id):
        with self.sql_repo.transaction():
            self.sql_dao.delete(carrier_id)


class SellerDAO():

    def __init__(self, sql_repo):
        self.sql_repo = sql_repo
        self.sql_dao = SqlDAO(sql_repo, map_sql.Seller)

    def create(self, seller_data):
        with self.sql_repo.transaction():
            self.sql_dao.create(seller_data)

    def delete(self, seller_id):
        with self.sql_repo.transaction():
            self.sql_dao.delete(seller_id)

    def get_sales(self, seller_id):
        with self.sql_repo.transaction():
            seller = self.sql_repo.read(map_sql.Seller, seller_id)
            products = []
            if seller:
                for product in seller.selling_products:
                    products.append(product)
                    self.sql_repo.expunge(product)
            return products

    def add_sale(self, sale_data: Dict):
        with self.sql_repo.transaction():
            sells = map_sql.Sells(**sale_data)
            seller = self.sql_repo.read(map_sql.Seller, sells.cnpj)
            product = self.sql_repo.read(map_sql.Product, sells.product_id)

            sells.is_sold = product
            seller.selling_prods.append(sells)

    def remove_sale(self, seller_id, product_id):
        with self.sql_repo.transaction():
            sells_tuple = self.sql_repo.read(map_sql.Sells, (seller_id, product_id))
            self.sql_repo.delete(sells_tuple)

    def get_promotions(self, seller_id):
        with self.sql_repo.transaction():
            seller = self.sql_repo.read(map_sql.Seller, seller_id)
            promotions = []
            if seller:
                for product in seller.promoting_products:
                    promotions.append(product)
                    self.sql_repo.expunge(product)
            return promotions

    def add_promotion(self, promotion_data: Dict):
        with self.sql_repo.transaction():
            promotes = map_sql.Promotes(**promotion_data)
            seller = self.sql_repo.read(map_sql.Seller, promotes.cnpj)
            product = self.sql_repo.read(map_sql.Product, promotes.product_id)

            promotes.is_promoted = product
            seller.promoting_prods.append(promotes)

    def remove_promotion(self, seller_id, product_id):
        with self.sql_repo.transaction():
            sells_tuple = self.sql_repo.read(map_sql.Promotes, (seller_id, product_id))
            self.sql_repo.delete(sells_tuple)


class ProductDAO():

    def __init__(self, sql_repo, neo_repo):
        self.sql_repo = sql_repo
        self.neo_repo = neo_repo
        self.transactor = Transactor([sql_repo, neo_repo])

        self.sql_dao = SqlDAO(sql_repo, map_sql.Product)
        self.neo_dao = NeoDAO(neo_repo, map_neo.Product, 'product_id')

        self.product_category_relator = \
            NeoRelator(neo_repo, map_neo.Product, 'product_id', map_neo.Category, 'category_id', 'belongs_to')

    def create(self, product_data: Dict | List[Dict]):
        product_data = self.sql_dao.ensure_list(product_data)

        with self.transactor.transaction():
            self.sql_dao.create(product_data)
            self.neo_dao.create(product_data)

    def delete(self, product_id: str):
        with self.transactor.transaction():
            self.sql_dao.delete(product_id)
            self.neo_dao.delete(product_id)

    def get_sellers(self, product_id):
        with self.sql_repo.transaction():
            product = self.sql_repo.read(map_sql.Product, product_id)
            sellers = []
            if product:
                for seller in product.sold_by:
                    sellers.append(seller.selling)
                    self.sql_repo.expunge(seller.selling)
            return sellers

    def get_categories(self, product_id):
        query = (f"MATCH (p:Product)-[:BelongsTo]->(c:Category)<-[:Subcategory*0..]-(s:Category)"
                 f"WHERE p.product_id = {product_id} RETURN s")
        with self.neo_repo.transaction():
            results, _ = self.neo_repo.cypher_query(query)
            nodes = [node for row in results for node in row]
            return nodes

    def add_category(self, product_id, category_id):
        with self.neo_repo.transaction():
            self.product_category_relator.connect_entities(product_id, category_id)

    def remove_category(self, product_id, category_id):
        with self.neo_repo.transaction():
            self.product_category_relator.disconnect_entities(product_id, category_id)


class PaymentDAO():

    def __init__(self, sql_repo):
        self.sql_repo = sql_repo
        self.sql_dao = SqlDAO(sql_repo, map_sql.PaymentMethod)

    def create(self, payment_data):
        with self.sql_repo.transaction():
            self.sql_dao.create(payment_data)

    def delete(self, payment_id):
        with self.sql_repo.transaction():
            self.sql_dao.delete(payment_id)


class UserDAO():

    def __init__(self, sql_repo, neo_repo, mongo_repo):
        self.sql_repo = sql_repo
        self.neo_repo = neo_repo
        self.mongo_repo = mongo_repo
        self.transactor = Transactor([sql_repo, neo_repo])

        self.sql_dao = SqlDAO(sql_repo, map_sql.User)
        self.neo_dao = NeoDAO(neo_repo, map_neo.User, 'cpf')
        self.mongo_dao = MongoDAO(mongo_repo, map_mongo.User)
        self.order_dao = OrderDAO(sql_repo, neo_repo)

        self.user_history_relator = \
            NeoRelator(self.neo_repo, map_neo.User, 'cpf', map_neo.Product, 'product_id', 'history')
        self.user_wishlist_relator = \
            NeoRelator(self.neo_repo, map_neo.User, 'cpf', map_neo.Product, 'product_id', 'wishlist')
        self.user_order_relator = \
            NeoRelator(self.neo_repo, map_neo.User, 'cpf', map_neo.Order, 'order_id', 'makes')

    def create(self, user_data: Dict | List[Dict]):
        user_data = self.sql_dao.ensure_list(user_data)

        with self.transactor.transaction():
            self.sql_dao.create(user_data)
            self.neo_dao.create(user_data)

    def update(self, new_user):
        table_id = getattr(map_sql.User, self.pk_name)
        user_id = getattr(new_user, self.pk_name)

        if not self.read(user_id):
            return

        new_data = {column: getattr(new_user, column) for column in map_sql.User.__table__.columns.keys()}
        stmt = (update(map_sql.User).where(table_id == user_id).values(**new_data))

        with self.unit_of_work.transaction():
            self.sql_repo.session.execute(stmt)

    def delete(self, user_id):
        with self.transactor.transaction():
            self.sql_dao.delete(user_id)
            self.neo_dao.delete(user_id)

    def add_order(self, order_data: Dict, order_rel_data: Dict):
        user_id = order_data.get('order_user_id')
        order_id = order_rel_data.get('order_id')
        product_id = order_rel_data.get('product_id')
        order_has = [map_sql.OrderHas(**order_rel_data)]

        with self.transactor.transaction():
            self.order_dao.create(order_data)
            self.sql_repo.create(order_has)

            self.order_dao.add_product(order_id, product_id)
            self.user_order_relator.connect_entities(user_id, order_id)

    def remove_order(self, order_id):
        self.order_dao.delete(order_id)

    def add_search(self, user_id, product_id):
        with self.neo_repo.transaction():
            self.user_history_relator.connect_entities(user_id, product_id)

    def remove_search(self, user_id, product_id):
        with self.neo_repo.transaction():
            self.user_history_relator.disconnect_entities(user_id, product_id)

    def add_wish(self, user_id, product_id):
        with self.neo_repo.transaction():
            self.user_wishlist_relator.connect_entities(user_id, product_id)

    def remove_wish(self, user_id, product_id):
        with self.neo_repo.transaction():
            self.user_wishlist_relator.disconnect_entities(user_id, product_id)

    def add_product_rating(self, user_id, product_id, rating_data):
        self.add_rating(user_id, product_id, map_mongo.Product, rating_data)

    def add_company_rating(self, user_id, company_id, rating_data):
        self.add_rating(user_id, company_id, map_mongo.Company, rating_data)

    def add_rating(self, user_id, entity_id, entity_class, rating_data):
        user = self.mongo_repo.read(map_mongo.User, user_id)
        rating = self.mongo_repo.read(map_mongo.Rating, rating_data['_id'])
        entity = self.mongo_repo.read(entity_class, entity_id)

        mongo_rating = MongoDAO(self.mongo_repo, map_mongo.Rating)
        mongo_entity = MongoDAO(self.mongo_repo, entity_class)

        if not user:
            self.mongo_dao.create({"_id": user_id})
            user = self.mongo_repo.read(map_mongo.User, user_id)

        if not rating:
            rating_data['user'] = user
            mongo_rating.create(rating_data)
            rating = self.mongo_repo.read(map_mongo.Rating, rating_data['_id'])

        if not entity:
            mongo_entity.create({"_id": entity_id, "ratings": [rating]})
        else:
            entity.ratings.append(rating)
            self.mongo_repo.save(entity)

    def remove_rating(self, rating_id):
        mongo_rating = MongoDAO(self.mongo_repo, map_mongo.Rating)
        mongo_rating.delete(rating_id)


class OrderDAO():

    def __init__(self, sql_repo, neo_repo):
        self.sql_repo = sql_repo
        self.neo_repo = neo_repo
        self.transactor = Transactor([sql_repo, neo_repo])

        self.sql_dao = SqlDAO(sql_repo, map_sql.Order)
        self.neo_dao = NeoDAO(neo_repo, map_neo.Order, 'order_id')

        self.order_product_relator = \
            NeoRelator(self.neo_repo, map_neo.Order, 'order_id', map_neo.Product, 'product_id', 'has_product')

    def create(self, order_data: Dict | List[Dict]):
        """
        Creation is handled by the UserDAO,
        so it's not encapsulated in a transaction.
        """
        order_data = self.sql_dao.ensure_list(order_data)
        self.sql_dao.create(order_data)
        self.neo_dao.create(order_data)

    def delete(self, order_id):
        with self.transactor.transaction():
            self.sql_dao.delete(order_id)
            self.neo_dao.delete(order_id)

    def add_product(self, order_id, product_id):
        self.order_product_relator.connect_entities(order_id, product_id)

    def remove_product(self, order_id, product_id):
        with self.neo_repo.transaction():
            self.order_product_relator.disconnect_entities(order_id, product_id)


class CategoryDAO():

    def __init__(self, neo_repo):
        self.pk = 'category_id'
        self.neo_repo = neo_repo

        self.neo_dao = NeoDAO(self.neo_repo, map_neo.Category, 'category_id')
        self.category_subcategory_relator = \
            NeoRelator(self.neo_repo, map_neo.Category, 'category_id', map_neo.Category, 'category_id', 'subcategory')

    def create(self, entity_data):
        self.neo_dao.create(entity_data)

    def delete(self, category_id):
        self.neo_dao.delete(category_id)

    def add_subcategory(self, category_id, subcategory_id):
        with self.neo_repo.transaction():
            self.category_subcategory_relator.connect_entities(category_id, subcategory_id)

    def remove_subcategory(self, category_id, subcategory_id):
        with self.neo_repo.transaction():
            self.category_subcategory_relator.disconnect_entities(category_id, subcategory_id)


def main():
    pass


if __name__ == "__main__":
    main()
