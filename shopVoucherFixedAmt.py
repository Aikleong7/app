import shelve
from datetime import date
import uuid

class shopVoucherFixedAmt():
    def __init__(self,name,startingDate,endingDate,minSpend,usageQuantity):
        self.__name=name
        self.__startingDate=startingDate
        self.__endingDate=endingDate
        self.__minSpend=minSpend
        self.__usageQuantity=usageQuantity
        self.__discountType="fixedAmt"
        self.__voucherType="shop"
        self.__code=str(uuid.uuid4())
        self.status=""


     #mutator methods
    def set_name(self,name):
        self.__name=name
    def set_code(self,code):
        self.__code=code
    def set_startingDate(self,startingDate):
        self.__startingDate=startingDate
    def set_endingDate(self,endingDate):
        self.__endingDate=endingDate
    def set_minSpend(self,minSpend):
        self.__minSpend=minSpend
    def set_usageQuantity(self,usageQuantity):
        self.__usageQuantity=usageQuantity
    def set_fixedAmt(self,fixedAmt):
        self.__fixedAmt=fixedAmt
    def set_status(self):
        today = date.today()
        if today < self.__startingDate:
            self.__status="Upcoming"
        elif today>= self.__startingDate and today <= self.__endingDate:
            self.__status="Ongoing"
        elif today > self.__endingDate:
            self.__status="Expired"
        if self.__usageQuantity==0:
            self.__status="Expired"

    #accessor methods
    def get_name(self):
        return self.__name
    def get_code(self):
        return self.__code
    def get_startingDate(self):
        return self.__startingDate
    def get_endingDate(self):
        return self.__endingDate
    def get_minSpend(self):
        return self.__minSpend
    def get_usageQuantity(self):
        return self.__usageQuantity
    def get_discountType(self):
        return self.__discountType
    def get_fixedAmt(self):
        return self.__fixedAmt
    def get_voucherType(self):
        return self.__voucherType
    def get_status(self):
        return self.__status

