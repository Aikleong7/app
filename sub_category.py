from products import *


class Sub_Category(Product):
    def __init__(self, product_cat, product_name, product_price, product_desc, sub_cat, quantity, inventory_name):
        super().__init__(product_cat, product_name, product_price, product_desc, quantity, inventory_name)
        self.__sub_cat = sub_cat

    def get_sub_cat(self):
        return self.__sub_cat

    def set_sub_cat(self, sub_cat):
        self.__sub_cat = sub_cat
