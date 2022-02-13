class Wallet:
    def __init__(self, merchant_balance):
        self.__balance = merchant_balance

    def withdraw_amt(self, withdraw):
        self.__balance -= withdraw

    def get_balance(self):
        return self.__balance

    def set_balance(self, balance):
        self.__balance = balance

    def top_up_amt(self, top_up):
        self.__balance += top_up


class Transactions:
    def __init__(self, transaction_type, amount, transaction_date, balance):
        self.__transaction_type = transaction_type
        self.__amount = amount
        self.__transaction_date = transaction_date
        self.__balance_after_transaction = balance

    def get_transaction_type(self):
        return self.__transaction_type

    def get_amount(self):
        return self.__amount

    def get_transaction_date(self):
        return self.__transaction_date

    def get_balance_after_transaction(self):
        return self.__balance_after_transaction


class SalesIncome:
    def __init__(self, category):
        self.__category = category
        self.__quantity = []
        self.__sales = []

    def get_quantity(self):
        return sum(self.__quantity)

    def get_sales(self):
        return sum(self.__sales)

    def get_category(self):
        return self.__category

    def add_sales(self, sales):
        self.__sales.append(sales)

    def add_quantity(self, qty):
        self.__quantity.append(qty)

