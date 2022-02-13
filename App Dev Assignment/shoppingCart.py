import shelve

class ShoppingCart():
    def __init__(self,userEmail):
        self.__userEmail=userEmail
        self.__chosenWebsiteVoucher=None #website voucher object
        self.__chosenWebsiteReward=None # website reward object
        self.__totalPrice=0
        self.__totalDiscountedPrice=0 #after the website vouchers are set
        self.__savings=0
        self.__availableWebsiteVouchers={} #{"reward":{websiteVoucherID:websiteVoucherObject}}
        self.__merchants={} #merchants ={merchantEmail:merchantObject}

    #can use when updating too
    def add_merchant(self,merchantEmail,SortByMerchantObject):
        self.__merchants[merchantEmail]=SortByMerchantObject

    #do some validation like SortByMerchant Object.get_products() , and productslist must be [] to delete
    def delete_merchant(self,merchantEmail):
        self.__merchants.pop(merchantEmail)

    #setting the whole merchant dict again
    def set_merchants(self,merchants_dict):
        self.__merchants=merchants_dict


    def calculate_totalPrice(self):
        self.__totalPrice=0
        for merchantObject in self.__merchants:
            if self.__merchants[merchantObject].get_discountedTotalPrice() != 0:
                self.__totalPrice+=float(self.__merchants[merchantObject].get_discountedTotalPrice())
            else:
                if self.__merchants[merchantObject].get_usedVoucher() == None:
                    self.__totalPrice+=float(self.__merchants[merchantObject].get_totalPrice())
                else:
                    self.__totalPrice+=0
        if self.__totalPrice<0:
            self.__totalPrice=0
        self.__totalDiscountedPrice=self.__totalPrice

    #do a method that calculates all the savings and run it when retrievin checkout
    def calculate_savings(self):
        self.__Merchantsavings=0
        for merchantObject in self.__merchants:
            if self.__merchants[merchantObject].get_savings() > 0:
                self.__Merchantsavings+=float(self.__merchants[merchantObject].get_savings())
                self.__savings=self.__Merchantsavings


    #do neccessary methods to include website vouchers - need to open db here and change things with the points
    #need to run the set web rewards and voucher whenever the user loads the checkout page
    def set_website_voucher(self,voucherObject):
        self.__chosenWebsiteVoucher=voucherObject
        self.__webVoucherSavings=0
        if voucherObject.get_discount_amt() >= 1: #fixed amt
            self.__webVoucherSavings=voucherObject.get_discount_amt()
            self.__totalDiscountedPrice=self.__totalDiscountedPrice-self.__webVoucherSavings
        else: #percentage
            self.__webVoucherSavings=self.__totalPrice*float(voucherObject.get_discount_amt())
            self.__totalDiscountedPrice-=self.__webVoucherSavings
        if self.__savings > 0:
            self.__savings+=self.__webVoucherSavings
        else:
            self.__savings=self.__webVoucherSavings

    # this method needs to be run before changing the website voucher and check if the chosenWebsiteVoucher is not equal to None
    def delete_website_voucher(self,voucherObject):
        self.__chosenWebsiteVoucher=None
        if voucherObject.get_discount_amt() >= 1: #fixed amt
            self.__totalDiscountedPrice+=voucherObject.get_discount_amt()
            self.__savings-=voucherObject.get_discount_amt()
        else:
            self.__totalDiscountedPrice+=self.__totalPrice*float(voucherObject.get_discount_amt())
            self.__savings-=self.__totalPrice*float(voucherObject.get_discount_amt())

    #doing the web rewards
    def set_web_reward(self,webRewardObject):
        self.__webRewardSavings=0
        self.__chosenWebsiteReward=webRewardObject
        self.__webRewardSavings=webRewardObject.get_amt_rewarded()
        if self.__webRewardSavings > self.__totalDiscountedPrice:
            self.__webRewardSavings=self.__totalDiscountedPrice
            self.__totalDiscountedPrice=0
        else:
            self.__totalDiscountedPrice-=self.__webRewardSavings
        print("total discounted price:",self.__totalDiscountedPrice)


        if self.__savings > 0:
            self.__savings+=self.__webRewardSavings
        else:
            self.__savings=self.__webRewardSavings

    #delete web rewards - use when changing the web rewards
    def delete_web_reward(self,webRewardObject):
        self.__chosenWebsiteReward=None
        self.__totalDiscountedPrice+=self.__webRewardSavings
        self.__savings-=self.__webRewardSavings

    def get_merchants(self):
        return self.__merchants

    def get_totalPrice(self):
        return self.__totalPrice

    def get_userEmail(self):
        return self.__userEmail

    def get_totalDiscountedPrice(self):
        return self.__totalDiscountedPrice

    def get_savings(self):
        return self.__savings

    def get_chosenWebsiteVoucher(self):
        return self.__chosenWebsiteVoucher

    def get_chosenWebsiteReward(self):
        return self.__chosenWebsiteReward

    def get_availableWebsiteVouchers(self):
        return self.__availableWebsiteVouchers


class SortByProduct():
    def __init__(self,productID,quantity,originalPrice,discountedPrice):
        self.__productID=productID
        self.__quantity=quantity #get it from the form
        self.__originalPrice=originalPrice # set original, discounted price by using the product object
        self.__discountedPrice=discountedPrice
        self.__totalPriceOfProduct=0
        db = shelve.open("customer.db", "r")
        musers_dict = db["Merchant"]
        db.close()
        all_singtopias_product_object = []
        for merchant in musers_dict:
            all_merchant_products = musers_dict.get(merchant).get_products()
            for product_id in all_merchant_products:
                all_singtopias_product_object.append(all_merchant_products.get(product_id))

        chosenProduct=None
        for x in range(len(all_singtopias_product_object)):
            if all_singtopias_product_object[x].get_product_id() == productID:
                chosenProduct=all_singtopias_product_object[x]

        self.__productObject=chosenProduct


    def set_quantity(self,quantity):
        self.__quantity=quantity
    def set_originalPrice(self,originalPrice):
        self.__originalPrice=originalPrice
    def set_discountedPrice(self,discountPrice):
        self.__discountedPrice=discountPrice
    def set_totalPrice(self):
        if self.__discountedPrice==0:
            total=int(self.__quantity)*float(self.__originalPrice)
        else:
            total=int(self.__quantity)*float(self.__discountedPrice)
        self.__totalPriceOfProduct=total

    def get_quantity(self):
        return self.__quantity
    def get_originalPrice(self):
        return self.__originalPrice
    def get_discountedPrice(self):
        return self.__discountedPrice
    def get_totalPrice(self):
        return self.__totalPriceOfProduct
    def get_productID(self):
        return self.__productID
    def get_productObject(self):
        return self.__productObject

class SortByMerchant():
    def __init__(self,merchantEmail,availableVouchers,merchantName):
        self.__products=[] # [sort by productObject]
        self.__merchantName=merchantName
        self.__totalPrice=0
        self.__discountedTotalPrice=0
        self.__savings=0
        self.__merchantEmail=merchantEmail
        self.__totalProducts=0
        self.__availableVouchers=availableVouchers #{count: voucherObject}
        self.__usedVoucher=None #voucher object

    def add_product(self,SortByProductObject):
        self.__products.append(SortByProductObject)
        self.__totalProducts+=1

    def delete_product(self,productID):
        for productObject in self.__products:
            if productID == productObject.get_productID():
                self.__products.remove(productObject)
                self.__totalProducts-=1

    #setting the whole product list again
    def set_productList(self,productList):
        self.__products=productList

    def calculate_totalPrice(self):
        total=0
        if self.__products!=[]:
            for productObject in self.__products:
                total+=float(productObject.get_totalPrice())
            self.__totalPrice=total
        else:
            self.__totalPrice=0


    def set_availableVouchers(self,vouchers_dict):
        self.__availableVouchers=vouchers_dict

    def set_savings_for_products(self):
        self.__Productsavings=0
        for sortbyproductObject in self.__products:
            if sortbyproductObject.get_discountedPrice() !=0:
                saving=sortbyproductObject.get_originalPrice()-sortbyproductObject.get_discountedPrice()
                self.__Productsavings+=saving*sortbyproductObject.get_quantity()
                self.__savings=self.__Productsavings

    def set_usedVoucher(self,count):
        self.__savings=0
        self.__usedVoucher=self.__availableVouchers[count]
        if self.__usedVoucher.get_discountType() == "fixedAmt":
            if float(self.__usedVoucher.get_fixedAmt()) >= self.__totalPrice:
                self.__savings=float(self.__totalPrice)
                self.__discountedTotalPrice=0
            else:
                self.__savings=float(self.__usedVoucher.get_fixedAmt())
                self.__discountedTotalPrice=float(self.__totalPrice)-self.__savings
        else:
            self.__savings=float(self.__totalPrice)*(self.__usedVoucher.get_percentageOff()/100)
            if self.__usedVoucher.get_cappedAmt() != 0: #if there is a limit
                if self.__savings > self.__usedVoucher.get_cappedAmt():
                    self.__savings=self.__usedVoucher.get_cappedAmt()
            if self.__savings>self.__totalPrice:
                self.__discountedTotalPrice=0
                self.__savings=float(self.__totalPrice)
            else:
                self.__discountedTotalPrice=self.__totalPrice-self.__savings
        if self.__Productsavings !=0:
            self.__savings+=self.__Productsavings

    def delete_voucher(self):
        self.__savings=0
        self.__discountedTotalPrice=0
        self.__usedVoucher=None

    def get_products(self):
        return self.__products

    def get_totalPrice(self):
        return self.__totalPrice

    def get_discountedTotalPrice(self):
        return self.__discountedTotalPrice

    def get_totalProducts(self):
        return self.__totalProducts

    def get_availableVouchers(self):
        return self.__availableVouchers

    def get_merchantEmail(self):
        return self.__merchantEmail

    def get_savings(self):
        return self.__savings

    def get_usedVoucher(self):
        return self.__usedVoucher

    def get_merchantName(self):
        return self.__merchantName






