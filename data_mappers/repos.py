from abc import ABC, abstractmethod
from contextlib import contextmanager

from map_sql import Base
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
        self.session = None

    def create_connection(self):
        engine = create_engine(self.URL, future=True)
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(engine, future=True)
        self.session = Session()

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

    def create_connection(self):
        config.DATABASE_URL = self.URL

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

    def read(self, entity, entity_id):
        return entity.nodes.get_or_none(**entity_id)

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

    @staticmethod
    def entity_to_dict(entity):
        entity_dict = {key: value for key, value in entity.__properties__.items()}
        return entity_dict


class MongoRepository(Repository):

    # Connection
    def __init__(self, URL):
        self.URL = URL

    def create_connection(self):
        connect(host=self.URL)

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
