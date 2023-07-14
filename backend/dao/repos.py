from abc import ABC, abstractmethod
from contextlib import contextmanager

from data_mappers.map_sql import Base
from pymongo import MongoClient
from mongoengine import connect
from neomodel import config, db
from sqlalchemy import and_, create_engine, update
from sqlalchemy.orm import class_mapper, sessionmaker


class Repository(ABC):

    @contextmanager
    def transaction(self):
        try:
            self.begin()
            yield
        except Exception:
            self.rollback()
            raise
        else:
            self.commit()
        finally:
            self.close()

    # Transaction
    @abstractmethod
    def begin(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def close(self):
        pass

    # Data Access
    @abstractmethod
    def create(self, entities):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class SQLRepository(Repository):
    # Connection
    def __init__(self, URL):
        self.URL = URL
        self.engine = None
        self.session = None
        self.create_connection()

    def create_connection(self):
        self.engine = create_engine(self.URL, future=True)
        Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(self.engine, future=True)
        self.session = Session()

    def drop_all(self):
        Base.metadata.drop_all(bind=self.engine)

    # Transaction
    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def close(self):
        self.session.close()

    # CRUD Data Access
    def create(self, entities):
        self.session.add_all(entities)

    def read(self, entity_class, entity_id):
        return self.session.get(entity_class, entity_id)

    def update(self, pks, pk_ids, entity_class, entity_data):
        conditions = [getattr(entity_class, pk) == pk_id for pk, pk_id in zip(pks, pk_ids)]
        condition = and_(*conditions)
        stmt = (update(entity_class).where(condition).values(**entity_data))
        self.session.execute(stmt)

    def delete(self, entity):
        self.session.delete(entity)

    # Other operations
    def get(self, entity_class, entity_id):
        entity = self.read(entity_class, entity_id)
        return self.entity_to_dict(entity)

    def get_all(self, entity_class):
        return [self.entity_to_dict(entity) for entity in self.session.query(entity_class).all()]

    def execute(self, stmt):
        self.session.execute(stmt)

    def expunge(self, obj):
        self.session.expunge(obj)

    @staticmethod
    def entity_to_dict(entity):
        entity_class = type(entity)
        mapper = class_mapper(entity_class)
        columns = [column.key for column in mapper.columns]
        entity_dict = {column: getattr(entity, column) for column in columns}
        return entity_dict


class NeoRepository(Repository):
    # Connection
    def __init__(self, URL):
        self.URL = URL
        self.create_connection()

    def create_connection(self):
        config.DATABASE_URL = self.URL

    def drop_all(self):
        self.cypher_query("MATCH(n) DETACH DELETE(n)")

    # Transaction
    def begin(self):
        db.begin()

    def commit(self):
        db.commit()

    def rollback(self):
        db.rollback()

    def close(self):
        pass

    # CRUD Data Access
    def create(self, entities):
        for entity in entities:
            node_class = type(entity)
            node_class.save(entity)

    def read(self, entity_class, entity_id):
        return entity_class.nodes.get_or_none(**entity_id)

    def update(self, entity):
        entity.save()

    def delete(self, entity):
        node_class = type(entity)
        node_class.delete(entity)

    # Other operations
    def cypher_query(self, query_params):
        return db.cypher_query(query_params)

    def get(self, entity):
        return self.entity_to_dict(entity)

    def get_all(self, entity_class):
        return [self.entity_to_dict(entity) for entity in entity_class.nodes.all()]

    @staticmethod
    def entity_to_dict(entity):
        entity_dict = {key: value for key, value in entity.__properties__.items()}
        return entity_dict


class MongoRepository(Repository):

    # Connection
    def __init__(self, URL):
        self.URL = URL
        self.db = self.create_connection()

    def create_connection(self):
        return connect(host=self.URL)

    def drop_all(self):
        db_name = MongoClient(self.URL).get_default_database().name
        self.db.drop_database(db_name)

    # Transaction
    def begin(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        pass

    # Data Access
    def create(self, entities):
        for entity in entities:
            entity.save()

    def read(self, entity, entity_id):
        return entity.objects(_id=entity_id).first()

    def update(self):
        pass

    def delete(self, entity):
        entity.delete()

    def save(self, entity):
        entity.save()


class Transactor(Repository):

    def __init__(self, repositories):
        self.repositories = repositories

    def begin(self):
        for repository in self.repositories:
            repository.begin()

    def commit(self):
        for repository in self.repositories:
            repository.commit()

    def rollback(self):
        for repository in self.repositories:
            repository.rollback()

    def close(self):
        for repository in self.repositories:
            repository.close()

    def create(self):
        pass

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass


def main():
    pass


if __name__ == "__main__":
    main()
