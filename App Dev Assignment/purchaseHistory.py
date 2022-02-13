class PurchaseHistory:
    def __init__(self,userShoppingCartObject,userEmail,paymentDetailsObject):
        self.__userEmail=userEmail
        self.__paymentDetails=paymentDetailsObject
        self.__merchants=[]
        merchants_dict=userShoppingCartObject.get_merchants()
        for merchantEmail in merchants_dict:
            self.__merchants.append(merchants_dict[merchantEmail])

    def get_userEmail(self):
        return self.__userEmail

    def get_paymentDetails(self):
        return self.__paymentDetails

    def get_merchants(self):
        return self.__merchants

class WholePurchaseHistory():
    def __init__(self):
        self.__purchaseHistory={}

    def add_purchaseHistory(self,purchaseHistoryObject):
        count=len(self.__purchaseHistory)
        count+=1
        self.__purchaseHistory[count]=purchaseHistoryObject

    def get_purchaseHistory(self):
        return self.__purchaseHistory


