from mongoengine import (DateTimeField, Document, IntField, ListField,
                         ReferenceField, StringField)


class User(Document):
    _id = StringField(primary_key=True)


class Rating(Document):
    _id = IntField(primary_key=True)
    user = ReferenceField(User, required=True, reverse_delete_rule=2)
    rating = IntField(required=True)
    date = DateTimeField(required=True)
    comment = StringField()


class Product(Document):
    _id = IntField(primary_key=True)
    ratings = ListField(ReferenceField(Rating, required=True, reverse_delete_rule=4))


class Company(Document):
    _id = StringField(primary_key=True)
    ratings = ListField(ReferenceField(Rating, required=True, reverse_delete_rule=4))


def main():
    pass


if __name__ == "__main__":
    main()
