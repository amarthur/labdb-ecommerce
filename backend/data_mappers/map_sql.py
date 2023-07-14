from datetime import datetime
from typing import List, Optional

from sqlalchemy import (ARRAY, CHAR, ForeignKey, ForeignKeyConstraint,
                        Identity, Integer, PrimaryKeyConstraint, String, Text)
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Company(Base):
    __tablename__ = 'company'

    cnpj: Mapped[str] = mapped_column(CHAR(14), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    info: Mapped[str] = mapped_column(Text)
    contact: Mapped[List[str]] = mapped_column(ARRAY(String(100)))
    location: Mapped[str] = mapped_column(String(100))
    company_type: Mapped[str] = mapped_column(String(20))

    __mapper_args__ = {
        'polymorphic_identity': 'company',
        'polymorphic_on': company_type,
    }


class Carrier(Company):
    __tablename__ = 'carrier'

    cnpj = mapped_column(ForeignKey('company.cnpj'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'carrier',
    }


class Seller(Company):
    __tablename__ = 'seller'

    cnpj = mapped_column(ForeignKey('company.cnpj'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'seller',
    }

    selling_prods: Mapped[List['Sells']] = relationship(back_populates='selling', cascade='all')
    promoting_prods: Mapped[List['Promotes']] = relationship(back_populates='promoting', cascade='all')

    selling_products: AssociationProxy[List['Product']] = association_proxy(
        "selling_prods",
        "is_sold",
        creator=lambda product_obj: Sells(is_sold=product_obj),
    )

    promoting_products: AssociationProxy[List['Product']] = association_proxy(
        "promoting_prods",
        "is_promoted",
        creator=lambda product_obj: Sells(is_promoted=product_obj),
    )


class Product(Base):
    __tablename__ = 'product'

    product_id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    brand: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    manufacturer: Mapped[str] = mapped_column(String(100))
    technical_details: Mapped[str] = mapped_column(Text)
    image_urls: Mapped[List[str]] = mapped_column(ARRAY(Text))

    sold_by: Mapped[List['Sells']] = relationship(back_populates='is_sold', cascade='all')
    promoted_by: Mapped[List['Promotes']] = relationship(back_populates='is_promoted', cascade='all')

    selling_products: AssociationProxy[List['Seller']] = association_proxy(
        "sold_by",
        "selling",
        creator=lambda seller_obj: Sells(selling=seller_obj),
    )


class Order(Base):
    __tablename__ = 'e_order'

    order_id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    order_date: Mapped[datetime]
    order_status: Mapped[str] = mapped_column(String(100))
    observations: Mapped[Optional[str]] = mapped_column(Text)

    order_user_id: Mapped[str] = mapped_column(ForeignKey("e_user.cpf"))
    paid_by: Mapped[List['Pays']] = relationship(back_populates='is_paid', cascade='all')
    cascade_order = relationship('OrderHas', cascade='all')


class PaymentMethod(Base):
    __tablename__ = 'payment_method'

    payment_id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    info: Mapped[str] = mapped_column(String(100))

    had_by: Mapped[List['HasPaymentMethod']] = relationship(back_populates='had', cascade='all')
    pays_order: Mapped[List['Pays']] = relationship(back_populates='pays', cascade='all')


class User(Base):
    __tablename__ = 'e_user'

    cpf: Mapped[str] = mapped_column(CHAR(11), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(100))
    addresses: Mapped[List[str]] = mapped_column(ARRAY(String(100)))
    phone_number: Mapped[List[str]] = mapped_column(ARRAY(String(15)))

    makes_order: Mapped[List['Order']] = relationship()
    has_payment: Mapped[List['HasPaymentMethod']] = relationship(back_populates='has', cascade='all')


class Sells(Base):
    __tablename__ = 'sells'

    cnpj: Mapped[str] = mapped_column(ForeignKey('seller.cnpj'), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.product_id'), primary_key=True)
    price: Mapped[int]
    stock: Mapped[int]
    guarantee: Mapped[str] = mapped_column(String(100))
    finish_date: Mapped[Optional[datetime]]

    selling: Mapped['Seller'] = relationship(back_populates='selling_prods')
    is_sold: Mapped['Product'] = relationship(back_populates='sold_by')


class Promotes(Base):
    __tablename__ = 'promotes'

    cnpj: Mapped[str] = mapped_column(ForeignKey('seller.cnpj'), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.product_id'), primary_key=True)
    start_date: Mapped[datetime]
    finish_date: Mapped[Optional[datetime]]
    promotion_type: Mapped[str] = mapped_column(String(100))

    promoting: Mapped['Seller'] = relationship(back_populates='promoting_prods')
    is_promoted: Mapped['Product'] = relationship(back_populates='promoted_by')


class HasPaymentMethod(Base):
    __tablename__ = 'has_pay_method'

    user_id: Mapped[str] = mapped_column(ForeignKey('e_user.cpf'), primary_key=True)
    payment_method_id: Mapped[int] = mapped_column(ForeignKey('payment_method.payment_id'), primary_key=True)
    payment_type: Mapped[str] = mapped_column(String(100))

    has: Mapped['User'] = relationship(back_populates='has_payment')
    had: Mapped['PaymentMethod'] = relationship(back_populates='had_by')


class Pays(Base):
    __tablename__ = 'pays'

    payment_method_id: Mapped[int] = mapped_column(ForeignKey('payment_method.payment_id'), primary_key=True)
    order_id: Mapped[str] = mapped_column(ForeignKey('e_order.order_id'), primary_key=True)
    installment: Mapped[Optional[str]] = mapped_column(String(100))

    pays: Mapped['PaymentMethod'] = relationship(back_populates='pays_order')
    is_paid: Mapped['Order'] = relationship(back_populates='paid_by')


class OrderHas(Base):
    __tablename__ = 'order_has'

    order_id: Mapped[str] = mapped_column(ForeignKey('e_order.order_id'))
    carrier_id: Mapped[str] = mapped_column(ForeignKey('carrier.cnpj'))
    seller_id: Mapped[str] = mapped_column(CHAR(14))
    product_id: Mapped[int]

    tracking: Mapped[str] = mapped_column(String(100))
    quantity: Mapped[int]
    shipping_fee: Mapped[float]
    delivery_date: Mapped[datetime]

    __table_args__ = (
        PrimaryKeyConstraint('order_id', 'carrier_id', 'seller_id', 'product_id'),
        ForeignKeyConstraint(['seller_id', 'product_id'], ['sells.cnpj', 'sells.product_id']),
    )


def main():
    pass


if __name__ == '__main__':
    main()
