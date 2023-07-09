from django.db import models
from djongo import models as djongo_models

class Company(models.Model):
    cnpj = models.CharField(max_length=14, primary_key=True)
    name = models.CharField(max_length=100)
    info = models.TextField()
    contact = models.JSONField()  # Storing list of strings
    location = models.CharField(max_length=100)
    company_type = models.CharField(max_length=20)

    class Meta:
        abstract = True

class Carrier(Company):
    pass

class Seller(Company):
    pass
    # Relationships to Sells and Promotes will be defined in those models

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    manufacturer = models.CharField(max_length=100)
    technical_details = models.TextField()
    image_urls = models.JSONField()  # Storing list of strings

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=100)
    observations = models.TextField(blank=True, null=True)
    order_user = models.ForeignKey('User', on_delete=models.CASCADE)

class PaymentMethod(models.Model):
    payment_id = models.AutoField(primary_key=True)
    info = models.CharField(max_length=100)

class User(models.Model):
    cpf = models.CharField(max_length=11, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    addresses = models.JSONField()  # Storing list of strings
    phone_number = models.JSONField()  # Storing list of strings

class Sells(models.Model):
    cnpj = models.ForeignKey('Seller', on_delete=models.CASCADE, db_column='cnpj')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, db_column='product_id')
    price = models.IntegerField()
    stock = models.IntegerField()
    guarantee = models.CharField(max_length=100)
    finish_date = models.DateTimeField(blank=True, null=True)

class Promotes(models.Model):
    cnpj = models.ForeignKey('Seller', on_delete=models.CASCADE, db_column='cnpj')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, db_column='product_id')
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField(blank=True, null=True)
    promotion_type = models.CharField(max_length=100)

class HasPaymentMethod(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='user_id')
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE, db_column='payment_method_id')
    payment_type = models.CharField(max_length=100)

class Pays(models.Model):
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE, db_column='payment_method_id')
    order = models.ForeignKey('Order', on_delete=models.CASCADE, db_column='order_id')
    installment = models.CharField(max_length=100, blank=True, null=True)

class OrderHas(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, db_column='order_id')
    carrier = models.ForeignKey('Carrier', on_delete=models.CASCADE, db_column='carrier_id')
    seller_id = models.CharField(max_length=14)
    product_id = models.IntegerField()
    tracking = models.CharField(max_length=100)
    quantity = models.IntegerField()
    shipping_fee = models.FloatField()
    delivery_date = models.DateTimeField()

    class Meta:
        unique_together = ['order', 'carrier', 'seller_id', 'product_id']
        constraints = [
            models.ForeignKeyConstraint(['seller_id', 'product_id'], ['Sells.cnpj', 'Sells.product_id']),
        ]
