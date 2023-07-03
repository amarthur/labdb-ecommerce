from neomodel import (DateTimeProperty, IntegerProperty, RelationshipFrom,
                      RelationshipTo, StringProperty, StructuredNode,
                      StructuredRel, UniqueIdProperty, config, db)


class User(StructuredNode):
    cpf = StringProperty(unique_index=True, required=True)
    name = StringProperty(required=True)

    history = RelationshipTo('Product', 'Searches')
    wishlist = RelationshipTo('Product', 'Wishes')
    makes = RelationshipTo('Order', 'Makes')


class Product(StructuredNode):
    product_id = IntegerProperty(unique_index=True, required=True)
    name = StringProperty(required=True)

    belongs_to = RelationshipTo('Category', 'BelongsTo')


class Order(StructuredNode):
    order_id = IntegerProperty(unique_index=True, required=True)

    has_product = RelationshipTo('Product', 'HasProduct')


class Category(StructuredNode):
    category_id = IntegerProperty(unique_index=True, required=True)
    name = StringProperty(required=True)

    subcategory = RelationshipTo('Category', 'Subcategory')

    def add_subcategory(self, category):
        self.subcategory.connect(category)


def main():
    pass


if __name__ == "__main__":
    main()
