import os
import sys
from typing import Any, Dict, List, Tuple

# Get relative imports to work when the package is not installed on the PYTHONPATH.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_mappers import map_mongo, map_neo, map_sql
from sqlalchemy.inspection import inspect

from .repos import MongoRepository, NeoRepository, SQLRepository, Transactor


class SqlDAO:

    def __init__(
        self,
        sql_repo: SQLRepository,
        entity_class: Any,
    ):
        self.sql_repo = sql_repo
        self.entity_class = entity_class
        self.pks = [key.name for key in inspect(entity_class).primary_key]

    def create(self, entity_data: Dict | List[Dict]):
        sql_entities = [self.entity_class(**entity) for entity in entity_data]
        self.sql_repo.create(sql_entities)

    def update(self, entity_id: Any, entity_data: Dict):
        pk_ids = entity_id if isinstance(entity_id, list) else [entity_id]
        self.sql_repo.update(self.pks, pk_ids, self.entity_class, entity_data)

    def delete(self, entity_id: Any):
        entity = self.sql_repo.read(self.entity_class, entity_id)
        self.sql_repo.delete(entity)

    def get(self, entity_id: Any):
        return self.sql_repo.get(self.entity_class, entity_id)

    def get_all(self):
        return self.sql_repo.get_all(self.entity_class)


class NeoDAO:

    def __init__(self, neo_repo: NeoRepository, entity_class: Any):
        self.neo_repo = neo_repo
        self.entity_class = entity_class

    def get_neo_node(self, entity_id: Any):
        neo_id_dict = {self.entity_class.get_pk(): entity_id}
        return self.neo_repo.read(self.entity_class, neo_id_dict)

    def create(self, entity_data: Dict | List[Dict]):
        neo_nodes = [self.entity_class(**entity) for entity in entity_data]
        self.neo_repo.create(neo_nodes)

    def update(self, entity_id: Any, entity_data: Dict):
        neo_node = self.get_neo_node(entity_id)
        for key, value in entity_data.items():
            setattr(neo_node, key, value)
        self.neo_repo.update(neo_node)

    def delete(self, entity_id: Any):
        neo_node = self.get_neo_node(entity_id)
        self.neo_repo.delete(neo_node)

    def get(self, entity_id: Any):
        return self.neo_repo.get(self.get_neo_node(entity_id))

    def get_all(self):
        return self.neo_repo.get_all(self.entity_class)


class MongoDAO:

    def __init__(
        self,
        mongo_repo: MongoRepository,
        entity_class: Any,
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
        return mongo_entities[0] if len(mongo_entities) == 1 else mongo_entities

    def delete(self, entity_id: Any):
        entity = self.mongo_repo.read(self.entity_class, entity_id)
        self.mongo_repo.delete(entity)


class NeoRelator:

    def __init__(
        self,
        neo_repo,
        entity_class,
        target_class,
        relationship_name,
    ):
        self.neo_repo = neo_repo
        self.entity_class = entity_class
        self.target_class = target_class
        self.relationship_name = relationship_name

    def relate_entities(self, entity_id_value: Any, target_id_value: Any, connect: bool):
        entity_id_dict = {self.entity_class.get_pk(): entity_id_value}
        target_id_dict = {self.target_class.get_pk(): target_id_value}

        entity = self.neo_repo.read(self.entity_class, entity_id_dict)
        target = self.neo_repo.read(self.target_class, target_id_dict)
        relationship = getattr(entity, self.relationship_name)

        if connect:
            relationship.connect(target)
        else:
            relationship.disconnect(target)

    def connect_entities(self, entity_id: Any, target_id: Any):
        self.relate_entities(entity_id, target_id, connect=True)

    def disconnect_entities(self, entity_id: Any, target_id: Any):
        self.relate_entities(entity_id, target_id, connect=False)


class DAO:

    def __init__(self, repo_class_tuples: Tuple[Any, Any] | List[Tuple[Any, Any]]):
        repo_class_tuples = self.ensure_list(repo_class_tuples)
        self.repos = [repo_class_tuple[0] for repo_class_tuple in repo_class_tuples]

        self.daos = [self.create_dao(repo_class_tuple) for repo_class_tuple in repo_class_tuples]
        self.transactor = Transactor(self.repos)

    @staticmethod
    def create_dao(repo_class_tuple: Tuple[Any, Any]):
        repo, entity_class = repo_class_tuple
        if isinstance(repo, SQLRepository):
            return SqlDAO(repo, entity_class)
        elif isinstance(repo, NeoRepository):
            return NeoDAO(repo, entity_class)
        elif isinstance(repo, MongoRepository):
            return MongoDAO(repo, entity_class)
        else:
            raise ValueError("Unsupported repository type")

    @staticmethod
    def ensure_list(entity_data: Dict | List[Dict]):
        return entity_data if isinstance(entity_data, list) else [entity_data]

    def create(self, entity_data: Dict | List[Dict]):
        entity_data = self.ensure_list(entity_data)
        with self.transactor.transaction():
            for dao in self.daos:
                dao.create(entity_data)

    def update(self, entity_id: Any, new_entity_data: Dict):
        with self.transactor.transaction():
            for dao in self.daos:
                dao.update(entity_id, new_entity_data)

    def delete(self, entity_id: Any):
        with self.transactor.transaction():
            for dao in self.daos:
                dao.delete(entity_id)

    def get(self, entity_id: Any, repo_index: int = 0):
        if (0 <= repo_index < len(self.repos)):
            with self.transactor.transaction():
                return self.daos[repo_index].get(entity_id)

    def get_all(self, repo_index: int = 0):
        if (0 <= repo_index < len(self.repos)):
            with self.transactor.transaction():
                return self.daos[repo_index].get_all()


class CompanyDAO(DAO):

    def __init__(self, sql_repo: SQLRepository):
        super().__init__((sql_repo, map_sql.Company))


class CarrierDAO(DAO):

    def __init__(self, sql_repo: SQLRepository):
        super().__init__((sql_repo, map_sql.Carrier))
        self.company_dao = CompanyDAO(sql_repo)

    def update(self, carrier_id: str, new_carrier_data: Dict):
        self.company_dao.update(carrier_id, new_carrier_data)


class SellerDAO(DAO):

    def __init__(self, sql_repo: SQLRepository):
        super().__init__((sql_repo, map_sql.Seller))

        self.sql_repo = sql_repo
        self.sql_dao = SqlDAO(sql_repo, map_sql.Seller)
        self.company_dao = CompanyDAO(sql_repo)

    def update(self, seller_id: str, new_seller_data: Dict):
        self.company_dao.update(seller_id, new_seller_data)

    # Sales
    def add_sale(self, sale_data: Dict):
        with self.sql_repo.transaction():
            sells = map_sql.Sells(**sale_data)
            seller = self.sql_repo.read(map_sql.Seller, sells.cnpj)
            product = self.sql_repo.read(map_sql.Product, sells.product_id)

            sells.is_sold = product
            seller.selling_prods.append(sells)

    def remove_sale(self, seller_id: str, product_id: int):
        with self.sql_repo.transaction():
            sells_tuple = self.sql_repo.read(map_sql.Sells, (seller_id, product_id))
            self.sql_repo.delete(sells_tuple)

    def get_sales(self, seller_id: str):
        with self.sql_repo.transaction():
            seller = self.sql_repo.read(map_sql.Seller, seller_id)
            products = []
            if seller:
                products = [self.sql_repo.entity_to_dict(product) for product in seller.selling_products]
            return products

    # Promotions
    def add_promotion(self, promotion_data: Dict):
        with self.sql_repo.transaction():
            promotes = map_sql.Promotes(**promotion_data)
            seller = self.sql_repo.read(map_sql.Seller, promotes.cnpj)
            product = self.sql_repo.read(map_sql.Product, promotes.product_id)

            promotes.is_promoted = product
            seller.promoting_prods.append(promotes)

    def remove_promotion(self, seller_id: str, product_id: int):
        with self.sql_repo.transaction():
            sells_tuple = self.sql_repo.read(map_sql.Promotes, (seller_id, product_id))
            self.sql_repo.delete(sells_tuple)

    def get_promotions(self, seller_id: str):
        with self.sql_repo.transaction():
            seller = self.sql_repo.read(map_sql.Seller, seller_id)
            promotions = []
            if seller:
                promotions = [self.sql_repo.entity_to_dict(product) for product in seller.promoting_products]
            return promotions


class ProductDAO(DAO):

    def __init__(self, sql_repo: SQLRepository, neo_repo: NeoRepository):
        super().__init__([(sql_repo, map_sql.Product), (neo_repo, map_neo.Product)])
        self.sql_repo = sql_repo
        self.neo_repo = neo_repo

        self.product_category_relator = \
            NeoRelator(neo_repo, map_neo.Product, map_neo.Category, 'belongs_to')

    # Sellers
    def get_sellers(self, product_id: int):
        with self.sql_repo.transaction():
            product = self.sql_repo.read(map_sql.Product, product_id)
            sellers = []
            if product:
                sellers = [self.sql_repo.entity_to_dict(seller) for seller in product.sold_by]
            return sellers

    # Categories
    def add_category(self, product_id: int, category_id: int):
        with self.neo_repo.transaction():
            self.product_category_relator.connect_entities(product_id, category_id)

    def remove_category(self, product_id: int, category_id: int):
        with self.neo_repo.transaction():
            self.product_category_relator.disconnect_entities(product_id, category_id)

    def get_categories(self, product_id: int):
        query = (f"MATCH (p:Product)-[:BelongsTo]->(c:Category)<-[:Subcategory*0..]-(s:Category)"
                 f"WHERE p.product_id = {product_id} RETURN s")
        with self.neo_repo.transaction():
            results, _ = self.neo_repo.cypher_query(query)
            nodes = [dict(node) for row in results for node in row]
            return nodes


class PaymentDAO(DAO):

    def __init__(self, sql_repo):
        super().__init__((sql_repo, map_sql.PaymentMethod))


class UserDAO(DAO):

    def __init__(self, sql_repo: SQLRepository, neo_repo: NeoRepository, mongo_repo: MongoRepository):
        super().__init__([(sql_repo, map_sql.User), (neo_repo, map_neo.User)])

        self.sql_repo = sql_repo
        self.neo_repo = neo_repo
        self.mongo_repo = mongo_repo

        self.mongo_dao = MongoDAO(mongo_repo, map_mongo.User)
        self.order_dao = OrderDAO(sql_repo, neo_repo)

        self.user_history_relator = \
            NeoRelator(self.neo_repo, map_neo.User, map_neo.Product, 'history')
        self.user_wishlist_relator = \
            NeoRelator(self.neo_repo, map_neo.User, map_neo.Product, 'wishlist')
        self.user_order_relator = \
            NeoRelator(self.neo_repo, map_neo.User, map_neo.Order, 'makes')

    # Order
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

    def remove_order(self, order_id: int):
        self.order_dao.delete(order_id)

    # Search
    def add_search(self, user_id: str, product_id):
        with self.neo_repo.transaction():
            self.user_history_relator.connect_entities(user_id, product_id)

    def remove_search(self, user_id: str, product_id):
        with self.neo_repo.transaction():
            self.user_history_relator.disconnect_entities(user_id, product_id)

    # Wishlist
    def add_wish(self, user_id: str, product_id):
        with self.neo_repo.transaction():
            self.user_wishlist_relator.connect_entities(user_id, product_id)

    def remove_wish(self, user_id: str, product_id):
        with self.neo_repo.transaction():
            self.user_wishlist_relator.disconnect_entities(user_id, product_id)

    # Rating
    def add_product_rating(self, user_id: str, product_id: int, rating_data: Dict):
        self.add_rating(user_id, product_id, map_mongo.Product, rating_data)

    def add_company_rating(self, user_id: str, company_id: str, rating_data: Dict):
        self.add_rating(user_id, company_id, map_mongo.Company, rating_data)

    def add_rating(self, user_id: str, entity_id: Any, entity_class: Any, rating_data: Dict):
        user = self.mongo_repo.read(map_mongo.User, user_id)
        rating = self.mongo_repo.read(map_mongo.Rating, rating_data['_id'])
        entity = self.mongo_repo.read(entity_class, entity_id)

        mongo_rating = MongoDAO(self.mongo_repo, map_mongo.Rating)
        mongo_entity = MongoDAO(self.mongo_repo, entity_class)

        if not user:
            user = self.mongo_dao.create({"_id": user_id})

        if not rating:
            rating_data['user'] = user
            rating = mongo_rating.create(rating_data)
        else:
            return

        if not entity:
            mongo_entity.create({"_id": entity_id, "ratings": [rating]})
        else:
            entity.ratings.append(rating)
            self.mongo_repo.save(entity)

    def remove_rating(self, rating_id: int):
        mongo_rating = MongoDAO(self.mongo_repo, map_mongo.Rating)
        mongo_rating.delete(rating_id)


class OrderDAO(DAO):

    def __init__(self, sql_repo: SQLRepository, neo_repo: NeoRepository):
        super().__init__([(sql_repo, map_sql.Order), (neo_repo, map_neo.Order)])
        self.sql_repo = sql_repo
        self.neo_repo = neo_repo

        self.sql_dao = SqlDAO(sql_repo, map_sql.Order)
        self.neo_dao = NeoDAO(neo_repo, map_neo.Order)

        self.order_product_relator = \
            NeoRelator(self.neo_repo, map_neo.Order, map_neo.Product, 'has_product')

    # Order
    def create(self, order_data: Dict | List[Dict]):
        """
        Order creation is handled by the UserDAO
        """
        order_data = self.ensure_list(order_data)
        self.sql_dao.create(order_data)
        self.neo_dao.create(order_data)

    def get(self, order_id: str):
        with self.sql_repo.transaction():
            return self.sql_dao.get(order_id)

    # Order Product
    def add_product(self, order_id: int, product_id: int):
        self.order_product_relator.connect_entities(order_id, product_id)

    def remove_product(self, order_id: int, product_id: int):
        with self.neo_repo.transaction():
            self.order_product_relator.disconnect_entities(order_id, product_id)


class CategoryDAO(DAO):

    def __init__(self, neo_repo: NeoRepository):
        super().__init__((neo_repo, map_neo.Category))
        self.neo_repo = neo_repo

        self.neo_dao = NeoDAO(self.neo_repo, map_neo.Category)
        self.category_subcategory_relator = \
            NeoRelator(self.neo_repo, map_neo.Category, map_neo.Category, 'subcategory')

    # Subcategory
    def add_subcategory(self, category_id: int, subcategory_id: int):
        with self.transactor.transaction():
            self.category_subcategory_relator.connect_entities(category_id, subcategory_id)

    def remove_subcategory(self, category_id: int, subcategory_id: int):
        with self.transactor.transaction():
            self.category_subcategory_relator.disconnect_entities(category_id, subcategory_id)


def main():
    pass


if __name__ == "__main__":
    main()
