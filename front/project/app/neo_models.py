# Neo4J

from django_neomodel import DjangoNode
from neomodel import StringProperty, IntegerProperty, RelationshipTo

class NeoUser(DjangoNode):
    cpf = StringProperty(unique_index=True, required=True)
    name = StringProperty(required=True)

    history = RelationshipTo('NeoProduct', 'Searches')
    wishlist = RelationshipTo('NeoProduct', 'Wishes')
    makes = RelationshipTo('Order', 'Makes')


class NeoProduct(DjangoNode):
    product_id = IntegerProperty(unique_index=True, required=True)
    name = StringProperty(required=True)

    belongs_to = RelationshipTo('Category', 'BelongsTo')


class Order(DjangoNode):
    order_id = IntegerProperty(unique_index=True, required=True)

    has_product = RelationshipTo('NeoProduct', 'HasProduct')


class Category(DjangoNode):
    category_id = IntegerProperty(unique_index=True, required=True)
    name = StringProperty(required=True)

    subcategory = RelationshipTo('Category', 'Subcategory')

    def add_subcategory(self, category):
        self.subcategory.connect(category)
