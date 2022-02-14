import json,shelve
from datetime import date
import uuid

class discountPromo():
    def __init__(self,name,startingDate,endingDate,productCode,productObject):
        self.__name=name
        self.__code=str(uuid.uuid4())
        self.__startingDate=startingDate
        self.__endingDate=endingDate
        self.__productCode=productCode
        self.__productObject=productObject
        self.__status=""

    #mutator methods
    def set_name(self,name):
        self.__name = name
    def set_code(self,code):
        self.__code = code
    def set_startingDate(self,startingDate):
        self.__startingDate = startingDate
    def set_endingDate(self,endingDate):
        self.__endingDate = endingDate
    def set_product(self,productCode,productObject):
        self.__productCode = productCode
        self.__productObject = productObject
    def set_status(self):
        today = date.today()
        if today < self.__startingDate:
            self.__status="Upcoming"
        elif today>= self.__startingDate and today <= self.__endingDate:
            self.__status="Ongoing"
        elif today > self.__endingDate:
            self.__status="Expired"

    #accesor methods
    def get_name(self):
        return self.__name
    def get_code(self):
        return self.__code
    def get_startingDate(self):
        return self.__startingDate
    def get_endingDate(self):
        return self.__endingDate
    def get_productCode(self):
        return self.__productCode
    def get_productObject(self):
        return self.__productObject
    def get_status(self):
        return self.__status


class DiscountProduct():
    def __init__(self,name,code,stock,originalPrice,discount,purchaseLimit):
        self.__name=name
        self.__code=code
        self.__stock=stock
        self.__originalPrice=originalPrice
        self.__discount=discount
        self.__purchaseLimitType="noLimit"
        self.__purchaseLimit=purchaseLimit

    def set_discount(self,discount):
        self.__discount=discount
    def set_purchaseLimitType(self,purchaseLimitType):
        self.__purchaseLimitType=purchaseLimitType
    def set_purchaseLimit(self,purchaseLimit):
        self.__purchaseLimit=purchaseLimit

    def get_discount(self):
        return self.__discount
    def get_purchaseLimitType(self):
        return self.__purchaseLimitType
    def get_purchaseLimit(self):
        return self.__purchaseLimit
    def get_name(self):
        return self.__name
    def get_code(self):
        return self.__code
    def get_originalPrice(self):
        return self.__originalPrice
    def get_stock(self):
        return self.__stock

    @classmethod
    def from_json(cls,json_string):
        json_dict=json.loads(json_string) #changes the json string to a python dictionary
        return cls(json_dict["name"],json_dict["code"],json_dict["originalPrice"],json_dict["discount"],json_dict["discountedPrice"],json_dict["purchaseLimit"])

#testing code
json_string="""{"name":"Cotton Candy","code":10,"stock":1000,"originalPrice":10,"discount":5,"discountedPrice":9.50,"purchaseLimitType":"No Limit","purchaseLimit":100}"""

product=DiscountProduct.from_json(json_string)
print(product.get_purchaseLimit())


