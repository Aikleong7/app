from uuid import uuid4


class CampVouchers:
    def __init__(self, minimum_spendage, campaign_origin):
        self.__minimum_spendage = minimum_spendage
        self.__campaign_origin = campaign_origin

    def set_minimum_spendage(self, minimum_spendage):
        self.__minimum_spendage = minimum_spendage

    def get_minimum_spendage(self):
        return self.__minimum_spendage


    def set_campaign_origin(self, campaign_origin):
        self.__campaign_origin = campaign_origin

    def get_campaign_origin(self):
        return self.__campaign_origin


class campaign_vouchers_percentage(CampVouchers):
    def __init__(self, discount_amt, minimum_spendage, campaign_origin):
        self.__voucher_id = str(uuid4())[:8]
        super().__init__(minimum_spendage, campaign_origin)
        self.__discount_amt = discount_amt

    def get_voucher_id(self):
        return self.__voucher_id

    def set_discount_amt(self, discount_amt):
        self.__discount_amt = discount_amt

    def get_discount_amt(self):
        return self.__discount_amt


class campaign_vouchers_price(CampVouchers):
    def __init__(self, discount_amt, minimum_spendage,campaign_origin):
        self.__voucher_id = str(uuid4())[:8]
        super().__init__(minimum_spendage,campaign_origin)
        self.__discount_amt = discount_amt

    def get_voucher_id(self):
        return self.__voucher_id

    def set_discount_amt(self, discount_amt):
        self.__discount_amt = discount_amt

    def get_discount_amt(self):
        return self.__discount_amt
