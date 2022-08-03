__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"
from peewee import *
from models import User, Product, Tag, Product_Tag, Purchase, db, create_db_tables


def populate_test_database():

    db.connect()
    create_db_tables()

    edgar = User.create(name="Edgar", address="1 Churchstreet, 1584AP, The Netherlands",
                        billing_info="Visa 4568 6548 1598 3548")
    dave = User.create(name="Dave", address="2 Mainstreet, 4865RE, The Netherlands",
                       billing_info="Mastercard 8497 5846 5241 5487")
    jane = User.create(name="Jane", address="3 Downstreet, 4715GT, The Netherlands",
                       billing_info="PayPal jane@doe.com")
    maria = User.create(name="Maria", address="4 Upperstreet, 5826AE, The Netherlands",
                        billing_info="Bank NL47RABO04854796")

    candle = Product.create(name="Candle", description="Vanilla scented candle",
                            price_in_cents=699, amount_in_stock=48,  owner=jane)
    cheese = Product.create(name="Cheese", description="Fresh cream cheese",
                            price_in_cents=1299, amount_in_stock=8,  owner=edgar)
    plate = Product.create(name="Plate", description="Decorated table plate",
                           price_in_cents=899, amount_in_stock=4,  owner=dave)
    painting = Product.create(name="Painting", description="Custom order painting",
                              price_in_cents=9000, amount_in_stock=1,  owner=maria)
    juice = Product.create(name="Juice", description="Homemade apple juice",
                           price_in_cents=499, amount_in_stock=48,  owner=dave)
    card = Product.create(name="Card", description="Golden birthday card",
                          price_in_cents=299, amount_in_stock=12,  owner=edgar)
    knife = Product.create(name="Knife", description="Large kitchen knife",
                           price_in_cents=899, amount_in_stock=4,  owner=jane)
    pie = Product.create(name="Pie", description="Fresh apple pie",
                         price_in_cents=499, amount_in_stock=2,  owner=edgar)
    shampoo = Product.create(name="Shampoo", description="Soap free shampoo",
                             price_in_cents=399, amount_in_stock=8,  owner=dave)
    origami = Product.create(name="Origami", description="Origami bird",
                             price_in_cents=199, amount_in_stock=10,  owner=maria)

    fresh = Tag.create(name="Fresh")
    food = Tag.create(name="Food")
    non_food = Tag.create(name="Non Food")
    made_to_order = Tag.create(name="Made to order")

    Product_Tag.create(product=candle, tag=non_food)
    Product_Tag.create(product=cheese, tag=food)
    Product_Tag.create(product=cheese, tag=fresh)
    Product_Tag.create(product=plate, tag=non_food)
    Product_Tag.create(product=painting, tag=non_food)
    Product_Tag.create(product=painting, tag=made_to_order)
    Product_Tag.create(product=juice, tag=food)
    Product_Tag.create(product=card, tag=non_food)
    Product_Tag.create(product=knife, tag=non_food)
    Product_Tag.create(product=pie, tag=food)
    Product_Tag.create(product=pie, tag=fresh)
    Product_Tag.create(product=shampoo, tag=non_food)
    Product_Tag.create(product=origami, tag=non_food)

    Purchase.create(product=candle, user=edgar,
                    quantity=2, total_price_in_cents=1398)
    Purchase.create(product=knife, user=dave,
                    quantity=1, total_price_in_cents=899)
    Purchase.create(product=pie, user=jane, quantity=1,
                    total_price_in_cents=499)
    Purchase.create(product=origami, user=jane,
                    quantity=3, total_price_in_cents=597)

    db.close()


def search(term):
    db.connect()
    query = (
        Product.select()
        .join(User, on=(Product.owner == User.id))
        .where(fn.LOWER(Product.name).contains(term.lower()) | fn.LOWER(Product.description).contains(term.lower()))
    )
    for result in query:
        print(f"Product name: {result.name}")
        print(f"Product description: {result.description}")
        print(f"Product price: {result.price_in_cents}")
        print(f"Amount in stock: {result.amount_in_stock}")
        print(f"Sold by: {result.owner.name}")
        print("")
    db.close()


def list_user_products(user_id):
    db.connect()
    query = (
        Product.select()
        .join(User, on=(Product.owner == User.id))
        .where(User.id == user_id)
    )
    for product in query:
        print(f"Products sold by {product.owner.name}")
        print("")
        break
    for product in query:
        print(f"Product name: {product.name}")
        print(f"Product description: {product.description}")
        print(f"Price: {product.price_in_cents}")
        print(f"Amount in stock: {product.amount_in_stock}")
        print("")
    db.close()


def list_products_per_tag(tag_id):
    db.connect()
    query = (
        Product.select(Product, Product_Tag, Tag)
        .join(Product_Tag, on=(Product_Tag.product == Product.id))
        .join(Tag, on=(Product_Tag.tag == Tag.id))
        .where(Tag.id == tag_id)
    )
    for product in query:
        print(f"Products tagged with: {product.product_tag.tag.name}")
        print("")
        break
    for product in query:
        print(f"Product name: {product.name}")
        print(f"Product description: {product.description}")
        print(f"Price: {product.price_in_cents}")
        print(f"Amount in stock: {product.amount_in_stock}")
        print("")
    db.close()


def add_product_to_catalog(user_id, product):
    db.connect()
    Product.create(name=product["name"], description=product["description"],
                   price_in_cents=product["price_in_cents"], amount_in_stock=product["amount_in_stock"], owner=user_id)
    print(f"""Product '{product["name"]}' added to the catalog!""")
    db.close()


def update_stock(product_id, new_quantity):
    db.connect()
    querry = (
        Product.select()
        .where(Product.id == product_id)
        .get()
    )
    querry.amount_in_stock = new_quantity
    querry.save()
    print(
        f"""Product '{querry.name}' new quantity is {querry.amount_in_stock}.""")
    db.close()


def purchase_product(product_id, buyer_id, quantity):
    db.connect()
    product = (
        Product.select()
        .where(Product.id == product_id)
        .get()
    )
    user = (
        User.select()
        .where(User.id == buyer_id)
        .get()
    )
    Purchase.create(product=product, user=user, quantity=quantity,
                    total_price_in_cents=product.price_in_cents*quantity)
    print(f"{quantity} {product.name}(s) where purchased by {user.name}.")
    db.close()


def remove_product(product_id):
    db.connect()
    product = (
        Product.select()
        .where(Product.id == product_id)
        .get()
    )
    product.delete_instance()
    product.save()
    print(
        f"""Product '{product.name}' with product id {product.id} has been deleted.""")
    db.close()


'''
Function calls to test functionalities
'''
# populate_test_database()

# search("ee")

# list_user_products(2)

# list_products_per_tag(2)

# test_product_dict = {
#     "name": "Test product",
#     "description": "A test product",
#     "price_in_cents": 699,
#     "amount_in_stock": 1
# }
# add_product_to_catalog(1, test_product_dict)

# update_stock(4, 66)

# purchase_product(3, 2, 1)

# remove_product(1)
