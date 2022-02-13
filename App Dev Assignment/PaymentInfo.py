from datetime import date

class PaymentInfo:
    def __init__(self,shoppingCartObject,deliveryAddressObject,cardObject):
        self.__shoppingCartObject=shoppingCartObject
        self.__deliveryAddress=deliveryAddressObject
        self.__cardInfo=cardObject
        self.__dateOfPayment=date.today()
        self.__shippingOption="FS"
        self.__totalPrice=shoppingCartObject.get_totalDiscountedPrice()
        self.__subTotal=self.__totalPrice
        self.__savings=shoppingCartObject.get_savings()

    def set_deliveryAddress(self,deliveryAddress):
        self.__deliveryAddress=deliveryAddress

    def set_cardInfo(self,cardObject):
        self.__cardInfo=cardObject

    def set_shippingOption(self,shippingOption):
        self.__shippingOption=shippingOption
        if shippingOption=="ES":
            self.__subTotal=self.__totalPrice+3
        else:
            self.__subTotal=self.__totalPrice

    def get_deliveryAddress(self):
        return self.__deliveryAddress

    def get_shoppingCartObject(self):
        return self.__shoppingCartObject

    def get_cardInfo(self):
        return self.__cardInfo

    def get_shippingOption(self):
        return self.__shippingOption

    def get_dateOfPayment(self):
        return self.__dateOfPayment

    def get_subTotal(self):
        return self.__subTotal

    def get_totalPrice(self):
        return self.__totalPrice

    def get_savings(self):
        return self.__savings

class deliveryAddress:
    def __init__(self,address,zipcode,city):
        self.__address=address
        self.__zipcode=zipcode
        self.__city=city

    def get_address(self):
        return self.__address

    def get_zipcode(self):
        return self.__zipcode

    def get_city(self):
        return self.__city

    def set(self,address,zipcode,city):
        self.__address=address
        self.__zipcode=zipcode
        self.__city=city




