class User:
    def __init__(self, first_name, last_name, email, phone, password):
        self.__profile_picture = "data:image/png;base64, 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"
        self.__first_name = first_name
        self.__last_name = last_name
        self.__cid = None
        self.__email = email
        self.__phone = phone
        self.__password = password
        self.__security_qn1 = ""
        self.__security_qn2 = ""
        self.__security_qn3 = ""
        self.__password_change = ""

    def set_profile_picture(self, profile_picture):
        self.__profile_picture = profile_picture

    def get_profile_picture(self):
        return self.__profile_picture

    def set_cid(self, cid):
        self.__cid = cid

    def get_cid(self):
        return self.__cid

    def set_security_qn1(self, security_qn1):
        self.__security_qn1 = security_qn1

    def get_security_qn1(self):
        return self.__security_qn1

    def set_security_qn2(self, security_qn2):
        self.__security_qn2 = security_qn2

    def get_security_qn2(self):
        return self.__security_qn2

    def set_security_qn3(self, security_qn3):
        self.__security_qn3 = security_qn3

    def get_security_qn3(self):
        return self.__security_qn3

    def set_email(self, email):
        self.__email = email

    def get_email(self):
        return self.__email

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_phone(self, phone):
        self.__phone = phone

    def get_phone(self):
        return self.__phone

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def set_password(self, password):
        self.__password = password

    def get_password(self):
        return self.__password

    def set_password_change(self, password_change):
        self.__password_change = password_change

    def get_password_change(self):
        return self.__password_change


class Customer(User):
    def __init__(self, first_name, last_name, email, phone, password, gender):
        super().__init__(first_name, last_name, email, phone, password)
        self.__date_joined = None
        self.__birthday = ""
        self.__rewards_indiv= []
        self.__points = 0
        self.__points_usable = 0
        self.__gender = gender
        self.__city = ""
        self.__zipcode = 0
        self.__credit_card = []
        self.__address = ""

    def update_rewards_indiv(self, rewards_indiv):
        self.__rewards_indiv.append(rewards_indiv)

    def set_rewards_indiv(self, rewards_indiv):
        self.__rewards_indiv = rewards_indiv

    def get_rewards_indiv(self):
        return self.__rewards_indiv

    def set_points(self, points):
        self.__points = points

    def get_points(self):
        return self.__points

    def set_points_usable(self, points_usable):
        self.__points_usable = points_usable

    def get_points_usable(self):
        return self.__points_usable

    def set_birthday(self, birthday):
        self.__birthday = birthday

    def get_birthday(self):
        return self.__birthday

    def set_zipcode(self, zipcode):
        self.__zipcode = zipcode

    def get_zipcode(self):
        return self.__zipcode

    def update_credit_card(self, credit_card):
        self.__credit_card.append(credit_card)

    def set_credit_card(self, credit_card):
        self.__credit_card = credit_card

    def get_credit_card(self):
        return self.__credit_card

    def set_city(self, city):
        self.__city = city

    def get_city(self):
        return self.__city

    def set_gender(self, gender):
        self.__gender = gender

    def get_gender(self):
        return self.__gender

    def set_address(self, address):
        self.__address = address

    def get_address(self):
        return self.__address

    def set_date_joined(self, date_joined):
        self.__date_joined = date_joined

    def get_date_joined(self):
        return self.__date_joined


class Feedbackuser:
    def __init__(self, name, email, message, read):
        self.__name = name
        self.__email = email
        self.__message = message
        self.__reply = False

    def get_email(self):
        return self.__email

    def get_name(self):
        return self.__name

    def get_messge(self):
        return self.__message

    def set_reply(self, reply):
        self.__reply = reply

    def get_reply(self):
        return self.__reply

class CreditCard:
    def __init__(self, credit_card, csv, default):
        self.__credit_card = credit_card
        self.__csv = csv
        self.__default = default

    def set_credit_card(self, credit_card):
        self.__credit_card = credit_card

    def set_csv(self, csv):
        self.__csv = csv

    def get_credit_card(self):
        return self.__credit_card

    def get_csv(self):
        return self.__csv

    def set_default(self, default):
        self.__default = default

    def get_default(self):
        return self.__default


class Supplier:
    def __init__(self, name, email, phone, product):
        self.__name = name
        self.__email = email
        self.__phone = phone
        self.__product = product

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_email(self, email):
        self.__email = email

    def get_email(self):
        return self.__email

    def set_phone(self, phone):
        self.__phone = phone

    def get_phone(self):
        return self.__phone

    def set_product(self, product):
        self.__product = product

    def get_product(self):
        return self.__product


class Admin(User):
    def __init__(self, first_name, last_name, email, phone, password, balance):
        super().__init__(first_name, last_name, email, phone, password)
        self.__balance = balance
        self.__transactions = []

    def get_transactions(self):
        return self.__transactions

    def add_transaction(self, amount):
        self.__transactions.append(amount)

    def set_balance(self, balance):
        self.__balance = balance

    def get_balance(self):
        return self.__balance


class Merchant(User):
    def __init__(self, first_name, last_name, email, phone, password):
        super().__init__(first_name, last_name, email, phone, password)
        self.__products = {}
        self.__supplier = []
        self.__main_address = ""
        self.__main_address_postal = ""
        self.__main_address_unit = ""
        self.__storage_address = ""
        self.__storage_address_postal = ""
        self.__storage_address_unit = ""
        self.__date_joined = ""
        self.__wallet_balance = 0
        self.__shop_description = ""
        self.__transactions = []


    def set_shop_description(self, shop_description):
        self.__shop_description = shop_description

    def get_shop_description(self):
        return self.__shop_description

    def get_products(self):
        return self.__products

    def set_products(self, product_dict):
        self.__products = product_dict

    def set_balance(self, wallet_balance):
        self.__wallet_balance = wallet_balance

    def get_balance(self):
        return self.__wallet_balance

    def set_date_joined(self, date_joined):
        self.__date_joined = date_joined

    def get_date_joined(self):
        return self.__date_joined

    def set_supplier(self, supplier):
        self.__supplier = supplier

    def add_supplier(self, supplier):
        self.__supplier.append(supplier)

    def get_supplier(self):
        return self.__supplier

    def set_main_address(self, main_address):
        self.__main_address = main_address

    def get_main_address(self):
        return self.__main_address

    def set_main_address_postal(self, main_address_postal):
        self.__main_address_postal = main_address_postal

    def get_main_address_postal(self):
        return self.__main_address_postal

    def set_main_address_unit(self, main_address_unit):
        self.__main_address_unit = main_address_unit

    def get_main_address_unit(self):
        return self.__main_address_unit

    def set_storage_address(self, storage_address):
        self.__storage_address = storage_address

    def get_storage_address(self):
        return self.__storage_address

    def set_storage_address_postal(self, storage_address_postal):
        self.__storage_address_postal = storage_address_postal

    def get_storage_address_postal(self):
        return self.__storage_address_postal

    def set_storage_address_unit(self, storage_address_unit):
        self.__storage_address_unit = storage_address_unit

    def get_storage_address_unit(self):
        return self.__storage_address_unit

    def get_transactions(self):
        return self.__transactions

    def set_transactions(self, transactions):
        self.__transactions = transactions
