import shelve
from shopVoucherFixedAmt import *

class shopVoucherPercentage(shopVoucherFixedAmt):
    def __init__(self,name,startingDate,endingDate,minSpend,usageQuantity,percentageOff):
        super().__init__(name,startingDate,endingDate,minSpend,usageQuantity)
        self.__discountType="percentageOff"
        self.__voucherType="shop"
        self.__percentageOff=percentageOff
        self.__cappedAmt=0


    #mutator methods
    def set_percentageOff(self,percentageOff):
        self.__percentageOff=percentageOff
    def set_cappedAmtType(self,cappedAmtType):
        self.__cappedAmtType=cappedAmtType
    def set_cappedAmt(self,cappedAmt):
        self.__cappedAmt=cappedAmt

    #accessor methods
    def get_discountType(self):
        return self.__discountType
    def get_percentageOff(self):
        return self.__percentageOff
    def get_cappedAmtType(self):
        return self.__cappedAmtType
    def get_cappedAmt(self):
        return self.__cappedAmt
