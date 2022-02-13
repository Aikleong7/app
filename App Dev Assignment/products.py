from datetime import date
import uuid


class Product:
    def __init__(self, product_cat, product_name, product_price, product_desc, quantity, inventory_name, image):
        self.__product_cat = product_cat
        self.__product_name = product_name
        self.__product_price = product_price
        self.__product_desc = product_desc
        self.__date = date.today()
        self.__id = str(uuid.uuid4())
        self.__quantity = int(quantity)
        self.__inventory_name = inventory_name
        self.__image = image
        self.__review = []

    def set_review(self, review):
        self.__review = review

    def add_review(self, review):
        self.__review.append(review)

    def get_review(self):
        return self.__review

    def get_image(self):
        return self.__image

    def set_image(self, image):
        self.__image = image

    def get_quantity(self):
        return self.__quantity

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def get_product_cat(self):
        return self.__product_cat

    def get_product_name(self):
        return self.__product_name

    def get_product_price(self):
        return self.__product_price

    def get_product_desc(self):
        return self.__product_desc

    def get_date(self):
        return self.__date

    def get_product_id(self):
        return self.__id

    def set_product_cat(self, product_cat):
        self.__product_cat = product_cat

    def set_product_name(self, product_name):
        self.__product_name = product_name

    def set_product_price(self, price):
        self.__product_price = price

    def set_product_desc(self, desc):
        self.__product_desc = desc

    def get_inventory_name(self):
        return self.__inventory_name

    def set_inventory_name(self, inventory_name):
        self.__inventory_name = inventory_name


class Inventory:
    def __init__(self, quantity, category, name, unit_price):
        self.__quantity = quantity
        self.__category = category
        self.__name = name
        self.__product_assigned = None
        self.__unitPrice = unit_price
        if self.__category == "Clothing" or self.__category == "Shoes":
            self.__dict_of_sizes = {}
        else:
            self.__dict_of_sizes = {}

    def get_name(self):
        return self.__name

    def get_category(self):
        return self.__category

    def get_quantity(self):
        return self.__quantity

    def set_product_assigned(self, product):
        self.__product_assigned = product

    def get_product_assigned(self):
        return self.__product_assigned

    def add_quantity(self, quantity):
        self.__quantity += quantity

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def get_dict_of_sizes(self):
        return self.__dict_of_sizes

    def add_to_dict_of_sizes(self, size_object):
        self.__dict_of_sizes[size_object.get_size_name()] = size_object

    def set_unit_price(self, unit_price):
        self.__unitPrice = unit_price

    def get_unit_price(self):
        return self.__unitPrice

class SubCategory(Product):
    def __init__(self, product_cat, product_name, product_price, product_desc, sub_cat, quantity, inventory_name,
                 image):
        super().__init__(product_cat, product_name, product_price, product_desc, quantity, inventory_name, image)
        self.__sub_cat = sub_cat

    def get_sub_cat(self):
        return self.__sub_cat

    def set_sub_cat(self, sub_cat):
        self.__sub_cat = sub_cat




class SizeAndQuantity:
    def __init__(self, size_name, qty):
        self.__size_name = size_name
        self.__qty = qty

    def set_qty(self, qty):
        self.__qty = qty

    def get_qty(self):
        return self.__qty

    def get_size_name(self):
        return self.__size_name

    def add_qty(self, add_qty):
        self.__qty += add_qty


class Review:
    def __init__(self, customer, review, rating):
        self.__customer = customer
        self.__review = review
        self.__rating = rating

    def set_rating(self, rating):
        self.__rating = rating

    def get_rating(self):
        return self.__rating

    def set_customer(self, customer):
        self.__customer = customer

    def set_review(self, review):
        self.__review = review

    def get_customer(self):
        return self.__customer

    def get_review(self):
        return self.__review
