# Models go here
from peewee import *
import datetime

db = SqliteDatabase("betsy.db")


class User(Model):
    name = CharField()
    address = CharField()
    billing_info = CharField()

    class Meta:
        database = db


class Product(Model):
    name = CharField()
    description = CharField()
    price_in_cents = IntegerField()
    amount_in_stock = IntegerField()
    owner = ForeignKeyField(User, backref="product")

    class Meta:
        database = db


class Tag(Model):
    name = CharField()

    class Meta:
        database = db


class Product_Tag(Model):
    product = ForeignKeyField(Product, backref="product_tag")
    tag = ForeignKeyField(Tag, backref="tag_product")

    class Meta:
        database = db


class Purchase(Model):
    product = ForeignKeyField(Product, backref="product_purchase")
    user = ForeignKeyField(User, backref="user_purchase")
    quantity = IntegerField()
    total_price_in_cents = IntegerField()
    purchase_datetime = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def create_db_tables():
    db.create_tables([User, Product, Tag, Product_Tag, Purchase])
