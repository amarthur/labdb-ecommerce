from neomodel import (StructuredNode, StringProperty, IntegerProperty, 
                      DateTimeProperty, JSONProperty, RelationshipTo, RelationshipFrom)

class Company(StructuredNode):
    cnpj = StringProperty(unique_index=True)
    name = StringProperty()
    info = StringProperty()
    contact = JSONProperty()  # JSONProperty is used for list of strings
    location = StringProperty()
    company_type = StringProperty()

class Carrier(Company):
    pass

class Seller(Company):
    sells = RelationshipTo('Product', 'SELLS')
    promotes = RelationshipTo('Product', 'PROMOTES')

class Product(StructuredNode):
    product_id = IntegerProperty(unique_index=True)
    name = StringProperty()
    brand = StringProperty()
    description = StringProperty()
    manufacturer = StringProperty()
    technical_details = StringProperty()
    image_urls = JSONProperty()  # JSONProperty is used for list of strings

class Order(StructuredNode):
    order_id = IntegerProperty(unique_index=True)
    order_date = DateTimeProperty()
    order_status = StringProperty()
    observations = StringProperty()
    order_user = RelationshipTo('User', 'ORDERED_BY')

class PaymentMethod(StructuredNode):
    payment_id = IntegerProperty(unique_index=True)
    info = StringProperty()

class User(StructuredNode):
    cpf = StringProperty(unique_index=True)
    name = StringProperty()
    email = StringProperty()
    password = StringProperty()
    addresses = JSONProperty()  # JSONProperty is used for list of strings
    phone_number = JSONProperty()  # JSONProperty is used for list of strings
    has_payment_method = RelationshipTo('PaymentMethod', 'HAS_PAYMENT_METHOD')
    makes = RelationshipTo('Order', 'MAKES')

class Sells(StructuredNode):
    cnpj = RelationshipFrom('Seller', 'SELLS')
    product = RelationshipFrom('Product', 'SOLD_BY')
    price = IntegerProperty()
    stock = IntegerProperty()
    guarantee = StringProperty()
    finish_date = DateTimeProperty()

class Promotes(StructuredNode):
    cnpj = RelationshipFrom('Seller', 'PROMOTES')
    product = RelationshipFrom('Product', 'PROMOTED_BY')
    start_date = DateTimeProperty()
    finish_date = DateTimeProperty()
    promotion_type = StringProperty()

class HasPaymentMethod(StructuredNode):
    user = RelationshipFrom('User', 'HAS_PAYMENT_METHOD')
    payment_method = RelationshipFrom('PaymentMethod', 'PAYMENT_METHOD_OF')
    payment_type = StringProperty()

class Pays(StructuredNode):
    payment_method = RelationshipFrom('PaymentMethod', 'PAYMENT_METHOD_FOR')
    order = RelationshipFrom('Order', 'PAID_BY')
    installment = StringProperty()

class OrderHas(StructuredNode):
    order = RelationshipFrom('Order', 'HAS_ORDER')
    carrier = RelationshipFrom('Carrier', 'CARRIED_BY')
    seller_id = StringProperty()
    product_id = IntegerProperty()
    tracking = StringProperty()
    quantity = IntegerProperty()
    shipping_fee = IntegerProperty()
    delivery_date = DateTimeProperty()
