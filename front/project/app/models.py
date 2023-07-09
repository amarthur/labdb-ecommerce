from django.db import models
from django.contrib.postgres.fields import ArrayField

class Company(models.Model):
    cnpj = models.CharField(max_length=14, primary_key=True)
    name = models.CharField(max_length=100)
    info = models.TextField()
    contact = ArrayField(models.CharField(max_length=100, blank=True), blank=True)
    location = models.CharField(max_length=100)
    company_type = models.CharField(max_length=20)

class Carrier(Company):
    pass

class Seller(Company):
    pass

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    manufacturer = models.CharField(max_length=100)
    technical_details = models.TextField()
    image_urls = ArrayField(models.TextField(), blank=True)

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_date = models.DateTimeField()
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
    addresses = ArrayField(models.CharField(max_length=100, blank=True), blank=True)
    phone_number = ArrayField(models.CharField(max_length=15, blank=True), blank=True)

class Sells(models.Model):
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    price = models.IntegerField()
    stock = models.IntegerField()
    guarantee = models.CharField(max_length=100)
    finish_date = models.DateTimeField(null=True, blank=True)

class Promotes(models.Model):
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField(null=True, blank=True)
    promotion_type = models.CharField(max_length=100)

class HasPaymentMethod(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=100)

class Pays(models.Model):
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    installment = models.CharField(max_length=100, null=True, blank=True)

class OrderHas(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    carrier = models.ForeignKey('Carrier', on_delete=models.CASCADE)
    seller = models.CharField(max_length=14)
    product = models.IntegerField()
    tracking = models.CharField(max_length=100)
    quantity = models.IntegerField()
    shipping_fee = models.FloatField()
    delivery_date = models.DateTimeField()


