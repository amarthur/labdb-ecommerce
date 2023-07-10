from neomodel import (IntegerProperty, RelationshipTo, StringProperty,
                      StructuredNode)


class PrimaryKey:

    @classmethod
    def get_pk(cls):
        for name, prop in cls.defined_properties().items():
            if prop.unique_index and prop.required:
                return name
        return None


class User(StructuredNode, PrimaryKey):
    cpf = StringProperty(unique_index=True, required=True)
    name = StringProperty(required=True)

    history = RelationshipTo('Product', 'Searches')
    wishlist = RelationshipTo('Product', 'Wishes')
    makes = RelationshipTo('Order', 'Makes')


class Product(StructuredNode, PrimaryKey):
    product_id = IntegerProperty(unique_index=True, required=True)
    name = StringProperty(required=True)

    belongs_to = RelationshipTo('Category', 'BelongsTo')


class Order(StructuredNode, PrimaryKey):
    order_id = IntegerProperty(unique_index=True, required=True)

    has_product = RelationshipTo('Product', 'HasProduct')


class Category(StructuredNode, PrimaryKey):
    category_id = IntegerProperty(unique_index=True, required=True)
    name = StringProperty(required=True)

    subcategory = RelationshipTo('Category', 'Subcategory')

    def add_subcategory(self, category):
        self.subcategory.connect(category)


def main():
    pass


if __name__ == "__main__":
    main()
