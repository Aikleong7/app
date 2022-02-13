import shelve

class Favourite():
    def __init__(self):
        self.__favouritedItems=[]
        self.__numItem=0

    def add_favourite(self,favouriteItemObject):
        add=True
        for item in self.__favouritedItems:
            if item.get_productID() == favouriteItemObject.get_productID():
                add=False
        if add:
            self.__favouritedItems.append(favouriteItemObject)
            self.__numItem+=1

    def delete_favourite(self,favouriteItemObject):
        if favouriteItemObject in self.__favouritedItems:
            self.__favouritedItems.remove(favouriteItemObject)
            self.__numItem-=1

    def get_favouritedItems(self):
        return self.__favouritedItems

    def get_numItems(self):
        return self.__numItem

class FavouriteItem():
    def __init__(self,productID):
        self.__productID=productID
        #getting merchant email with product ID
        db = shelve.open('customer.db', "c")
        muser_dict = {}
        try:
            muser_dict = db["Merchant"]
        except:
            print("Error in retrieving products from customer.db.")
        db.close()
        for merchantEmail in muser_dict:
            merchantproducts=muser_dict[merchantEmail].get_products()
            for id in merchantproducts:
                if id ==productID:
                    self.__merchantEmail=merchantEmail
                    print(self.__merchantEmail)
                    break

        #getting productObject
        db = shelve.open("customer.db", "r")
        musers_dict = db["Merchant"]
        db.close()
        all_singtopias_product_object = []
        for merchant in musers_dict:
            all_merchant_products = musers_dict.get(merchant).get_products()
            for product_id in all_merchant_products:
                all_singtopias_product_object.append(all_merchant_products.get(product_id))

        for item in all_singtopias_product_object:
            if item.get_product_id() == productID:
                self.__productObject=item

        #getting original price
        self.__originalPrice=self.__productObject.get_product_price()

        #getting discountPromo
        discountPromo_dict = {}
        DiscountPromodb = shelve.open('discountPromo.db', 'c')
        try:
            if 'discountPromo' in DiscountPromodb:  # is key exist?
                discountPromo_dict = DiscountPromodb['discountPromo']  # retrieve data
            else:
                DiscountPromodb['discountPromo'] = discountPromo_dict  # start with empty
        except:
            print("Error in retrieving discountPromo from discountPromo.db.")
        merchantDiscounts_dict = {}
        try:
            if self.__merchantEmail in discountPromo_dict:
                merchantDiscounts_dict = discountPromo_dict[self.__merchantEmail]
            else:
                discountPromo_dict[self.__merchantEmail] = merchantDiscounts_dict
        except:
            print("Error occured in shop discounts dictionary.")

        DiscountPromodb.close()
        self.__discountPromo=0
        for count in merchantDiscounts_dict:
            productcode=merchantDiscounts_dict[count].get_productCode()
            if productcode==productID:
                self.__discountPromo=merchantDiscounts_dict[count].get_productObject().get_discount()
                break
        if self.__discountPromo!=0:
            self.__discountedPrice=((100-self.__discountPromo)/100)*self.__originalPrice
        else:
            self.__discountedPrice=0

        #getting Available Vouchers
        self.__availableVoucher=[]
        shopVoucher_dict = {}
        fixeddb = shelve.open('shopVoucherFixedAmt.db', 'r')
        # shopVoucher_dict={merchant email:{shop voucher code: shop voucher object}}
        try:
            if 'shopVouchers' in fixeddb:  # is key exist?
                shopVoucher_dict = fixeddb['shopVouchers']  # retrieve data
            else:
                fixeddb['shopVouchers'] = shopVoucher_dict  # start with empty
        except:
            print("Error in retrieving shopVouchers from vouchers.db.")
        merchantShopVoucher_dict = {}
        try:
            if self.__merchantEmail in shopVoucher_dict:
                merchantShopVoucher_dict = shopVoucher_dict[self.__merchantEmail]
            else:
                shopVoucher_dict[self.__merchantEmail] = merchantShopVoucher_dict
        except:
            print("Error occured in shop voucher dictionary.")
        fixeddb.close()

        for key in merchantShopVoucher_dict:
            voucher=merchantShopVoucher_dict.get(key)
            if voucher.get_status() == "Ongoing" and voucher.get_usageQuantity()>0:
                self.__availableVoucher.append(voucher)

        db = shelve.open('shopVouchersPercentage.db', 'r')
        shopVoucher_dict={}
        # shopVoucher_dict={merchant email:{shop voucher code: shop voucher object}}
        try:
            if 'shopVouchersPercentage' in db:  # is key exist?
                shopVoucher_dict = db['shopVouchersPercentage']  # retrieve data
            else:
                db['shopVouchersPercentage'] = shopVoucher_dict  # start with empty
        except:
            print("Error in retrieving shopVouchers from vouchers.db.")
        merchantShopVoucher_dict = {}
        try:
            if self.__merchantEmail in shopVoucher_dict:
                merchantShopVoucher_dict = shopVoucher_dict[self.__merchantEmail]
            else:
                shopVoucher_dict[self.__merchantEmail] = merchantShopVoucher_dict
        except:
            print("Error occured in shop voucher dictionary.")

        for key in merchantShopVoucher_dict:
            voucher=merchantShopVoucher_dict.get(key)
            if voucher.get_status() == "Ongoing" and voucher.get_usageQuantity()>0:
                self.__availableVoucher.append(voucher)
        db.close()

        self.__voucherShow=[]
        if len(self.__availableVoucher) > 3:
            for x in range(3):
                self.__voucherShow.append(self.__availableVoucher[x])
        else:
            for x in range(len(self.__availableVoucher)):
                self.__voucherShow.append(self.__availableVoucher[x])


    def get_voucherShow(self):
        return self.__voucherShow

    def get_productID(self):
        return self.__productID

    def get_merchantEmail(self):
        return self.__merchantEmail

    def get_originalPrice(self):
        return self.__originalPrice

    def get_discountedPrice(self):
        return self.__discountedPrice

    def get_discountPromo(self):
        return self.__discountPromo

    def get_availableVouchers(self):
        return self.__availableVoucher

    def get_productObject(self):
        return self.__productObject


