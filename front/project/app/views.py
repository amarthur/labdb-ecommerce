from django.shortcuts import render

from django.shortcuts import render
from django.views import View
from .models import Company, Carrier, Seller, Product, Order, PaymentMethod, User, Sells, Promotes, HasPaymentMethod, Pays, OrderHas
from .mongo_models import MongoUser, MongoRating
from .neo_models import NeoUser, NeoProduct

class CompanyListView(View):
    def get(self, request):
        companies = Company.objects.all()
        return render(request, 'company_list.html', {'companies': companies})

class CompanyDetailView(View):
    def get(self, request, cnpj):
        company = Company.objects.get(cnpj=cnpj)
        return render(request, 'company_detail.html', {'company': company})

class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'product_list.html', {'products': products})

class ProductDetailView(View):
    def get(self, request, product_id):
        product = Product.objects.get(product_id=product_id)
        return render(request, 'product_detail.html', {'product': product})

class OrderListView(View):
    def get(self, request):
        orders = Order.objects.all()
        return render(request, 'order_list.html', {'orders': orders})

class OrderDetailView(View):
    def get(self, request, order_id):
        order = Order.objects.get(order_id=order_id)
        return render(request, 'order_detail.html', {'order': order})

class UserDetailView(View):
    def get(self, request, cpf):
        user = User.objects.get(cpf=cpf)
        return render(request, 'user_detail.html', {'user': user})

class UserRatingView(View):
    def get(self, request, cpf):
        user = User.objects.get(cpf=cpf)
        ratings = user.ratings.all()
        return render(request, 'user_ratings.html', {'user': user, 'ratings': ratings})

class NeoUserDetailView(View):
    def get(self, request, cpf):
        user = NeoUser.nodes.get(cpf=cpf)
        return render(request, 'neo_user_detail.html', {'user': user})

class NeoProductDetailView(View):
    def get(self, request, product_id):
        product = NeoProduct.nodes.get(product_id=product_id)
        return render(request, 'neo_product_detail.html', {'product': product})

class MongoUserDetailView(View):
    def get(self, request, _id):
        user = MongoUser.objects.get(_id=_id)
        return render(request, 'mongo_user_detail.html', {'user': user})

class MongoRatingListView(View):
    def get(self, request, product_id):
        ratings = MongoRating.objects.filter(product__id=product_id)
        return render(request, 'mongo_rating_list.html', {'ratings': ratings})
