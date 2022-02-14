from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
import shelve
from User import *
from Forms import *
import hashlib
from uuid import uuid4
from datetime import datetime
from datetime import timedelta
import json
from merchant_wallet import *
from td import *
from sub_category import *
from products import *
from shopVoucherFixedAmt import *
from shopVoucherPercentage import *
from shoppingCart import *
from discountPromo import *
from PaymentInfo import *
from favourites import *
from purchaseHistory import *
import website_rewards as wr
import website_campaign as wc
import campaign_vouchers as cv

app = Flask(__name__)
app.secret_key = "hello"

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "SingtopiaSG@gmail.com",
    "MAIL_PASSWORD": "Singtopia2022"
}
app.config.update(mail_settings)
mail = Mail(app)


@app.route("/")
def home():
    log = request.args.get('id')
    ses = None

    try:
        if session["user"] is not None:
            ses = session['user']
    except:
        pass
    # print(session['user'])

    db = shelve.open('customer.db', "c")
    musers_dict = {}
    try:
        musers_dict = db["Merchant"]
    except:
        print("error")
    all_product = []
    all_merchant_objects = []
    for key in musers_dict:
        merchant_obj = musers_dict.get(key)
        all_merchant_objects.append(merchant_obj)
    for i in all_merchant_objects:
        # print(i.get_products())
        merchants_product_dict = i.get_products()
        for x in merchants_product_dict:
            all_product.append(merchants_product_dict.get(x))

    # Aaralyn Part
    shoppingCarts = {}
    shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
    try:
        if "shoppingCart" in shoppingCartDB:  # is key exist?
            shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
        else:
            print("Shopping carts has an error.")  # start with empty
    except:
        print("Error in retrieving shopVouchers from vouchers.db.")

    userShoppingCart = None  # retrieves the shopping cart object
    try:
        if session['user'] in shoppingCarts:
            userShoppingCart = shoppingCarts[session['user']]
        else:
            print("Can't retrieve the user's shopping cart.")
    except:
        print("Error occured in dictionary.")
    shoppingCartDB.close()

    noOfItems = 0
    productList = []
    totalPrice = 0
    if userShoppingCart != None:
        merchant_dict = userShoppingCart.get_merchants()
        for merchantEmail in merchant_dict:
            merchantObject = merchant_dict[merchantEmail]
            product_list = merchantObject.get_products()
            for product in product_list:
                productList.append(product)
                noOfItems += 1
                totalPrice += round(product.get_totalPrice(), 2)

    datetoday = date.today()
    date_limit = timedelta(days=30)

    return render_template("index.html", log=log, session=ses, userShoppingCart=userShoppingCart, noOfItems=noOfItems,
                           productList=productList, totalPrice=totalPrice, all_product=all_product, date_limit=date_limit, datetoday=datetoday)


@app.route("/explore")
def home_explore():
    log = request.args.get('id')


    try:
        if session["user"] is not None:
            ses = session['user']
    except:
        ses = None
    # print(session['user'])

    db = shelve.open('customer.db', "r")
    musers_dict = {}
    try:
        musers_dict = db["Merchant"]
    except:
        print("error")
    all_product = []
    all_merchant_objects = []
    for key in musers_dict:
        merchant_obj = musers_dict.get(key)
        all_merchant_objects.append(merchant_obj)
    for i in all_merchant_objects:
        # print(i.get_products())
        merchants_product_dict = i.get_products()
        for x in merchants_product_dict:
            all_product.append(merchants_product_dict.get(x))

    # Aaralyn Part
    shoppingCarts = {}
    shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
    try:
        if "shoppingCart" in shoppingCartDB:  # is key exist?
            shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
        else:
            print("Shopping carts has an error.")  # start with empty
    except:
        print("Error in retrieving shopVouchers from vouchers.db.")

    userShoppingCart = None  # retrieves the shopping cart object
    try:
        if session['user'] in shoppingCarts:
            userShoppingCart = shoppingCarts[session['user']]
        else:
            print("Can't retrieve the user's shopping cart.")
    except:
        print("Error occured in dictionary.")
    shoppingCartDB.close()

    noOfItems = 0
    productList = []
    totalPrice = 0
    if userShoppingCart != None:
        merchant_dict = userShoppingCart.get_merchants()
        for merchantEmail in merchant_dict:
            merchantObject = merchant_dict[merchantEmail]
            product_list = merchantObject.get_products()
            for product in product_list:
                productList.append(product)
                noOfItems += 1
                totalPrice += round(product.get_totalPrice(), 2)

    return render_template("Explore_page.html", log=log, session=ses, userShoppingCart=userShoppingCart, noOfItems=noOfItems,
                       productList=productList, totalPrice=totalPrice, all_product=all_product)


@app.route("/about_us")
def bout_us():

    return render_template("common/about_us.html")


@app.route("/categories/<cat>")
def home_cat(cat):
    db = shelve.open('customer.db', "r")
    musers_dict = {}
    try:
        musers_dict = db["Merchant"]
    except:
        print("error")
    all_product = []
    products_list = []
    all_merchant_objects = []
    for key in musers_dict:
        merchant_obj = musers_dict.get(key)
        all_merchant_objects.append(merchant_obj)
    for i in all_merchant_objects:
        # print(i.get_products())
        merchants_product_dict = i.get_products()
        for x in merchants_product_dict:
            all_product.append(merchants_product_dict.get(x))
    for product in all_product:

        if product.get_product_cat() == cat:
            products_list.append(product)
    db.close()

    # Aaralyn Part
    shoppingCarts = {}
    shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
    try:
        if "shoppingCart" in shoppingCartDB:  # is key exist?
            shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
        else:
            print("Shopping carts has an error.")  # start with empty
    except:
        print("Error in retrieving shopVouchers from vouchers.db.")

    userShoppingCart = None  # retrieves the shopping cart object
    try:
        if session['user'] in shoppingCarts:
            userShoppingCart = shoppingCarts[session['user']]
        else:
            print("Can't retrieve the user's shopping cart.")
    except:
        print("Error occured in dictionary.")
    shoppingCartDB.close()

    noOfItems = 0
    productList = []
    totalPrice = 0
    if userShoppingCart != None:
        merchant_dict = userShoppingCart.get_merchants()
        for merchantEmail in merchant_dict:
            merchantObject = merchant_dict[merchantEmail]
            product_list = merchantObject.get_products()
            for product in product_list:
                productList.append(product)
                noOfItems += 1
                totalPrice += round(product.get_totalPrice(), 2)

    return render_template("index_cat.html", products_list=products_list,
                           userShoppingCart=userShoppingCart, noOfItems=noOfItems,
                           productList=productList, totalPrice=totalPrice)

    # print(merchants_product_dict)
    # for x in merchants_product_dict:
    #     print(merchants_product_dict.get(x).get_product_cat())
    # print(i.get_products())
    # for product_id in merchants_product_dict:
    #     product_obj = merchants_product_dict.get(product_id)
    #     if str(product_obj.get_product_cat()) == str(cat):
    #         products_list.append(product_obj)
    #         # print(products_list)
    #         return render_template("index_cat.html", products_list=products_list)
    #     else:
    #         print("error")


@app.route("/logout")
def logout():
    session['user'] = None
    return redirect(url_for("home", id=2))


@app.route("/login", methods=["POST", "GET"])
def login():
    customer = {}
    profile = request.args.get('id')
    form = LoginForm(request.form)
    # print(session['user'])
    if request.method == "POST":
        # print(form.email.data)
        try:
            db = shelve.open("customer.db", "r")
            customer = db['Customer']
        except:
            db = shelve.open("customer.db", "c")
            db['Customer'] = customer
        if form.email.data in customer:
            acc = db['Customer'].get(form.email.data)
            hashed = hashlib.sha3_256(form.password.data.encode())
            db.close()
            if acc.get_password() == hashed.hexdigest():
                session["user"] = acc.get_email()
                # print(acc.get_email())
                if profile == "1":
                    return redirect(url_for('profile'))
                elif profile == "2":
                    return redirect(url_for('favourites'))
                else:
                    return redirect(url_for("home", id=1))
            else:
                return render_template("Customer/login.html", form=form, warning=1)
        else:
            return render_template("Customer/login.html", form=form, warning=1)
    # print(session['user'])
    return render_template("Customer/login.html", form=form)


@app.route("/createaccount", methods=["POST", "GET"])
def create_account():
    form = CreateAccountForm(request.form)
    if request.method == 'POST':
        password = str(form.password.data)

        customers_dict = {}
        db = shelve.open("customer.db", 'c')

        try:
            if 'Customer' in db:
                customers_dict = db['Customer']
            else:
                db["Customer"] = customers_dict
        except:
            print("File cannot be found ")
        if form.email.data in db["Customer"] and form.password.data != form.password_confirm.data:
            return render_template("Customer/createaccount.html", form=form, warning=3)
        else:
            if form.password.data != form.password_confirm.data:
                return render_template("Customer/createaccount.html", form=form, warning=2)
            elif form.email.data in db["Customer"]:
                return render_template("Customer/createaccount.html", form=form, warning=1)
            elif len(form.password.data) < 8:
                return render_template("Customer/createaccount.html", form=form, warning=4)
            elif len(form.password.data) > 20:
                return render_template("Customer/createaccount.html", form=form, warning=4)
            elif len(form.password.data) < 20:
                for i in range(0, len(form.password.data)):
                    if (password[i].isalpha() == False) and (password[i].isdigit() == False):
                        return render_template("Customer/createaccount.html", form=form, warning=4)
                    else:
                        hashed = hashlib.sha3_256(form.password.data.encode())
                        customer = Customer(form.first_name.data, form.last_name.data, form.email.data, form.phone.data,
                                            hashed.hexdigest(), form.gender.data)
                        date = datetime.now()
                        customer.set_cid(str(uuid4()))
                        customer.set_date_joined([date.strftime("%Y"), date.strftime("%m"), date.strftime("%d")])
                        customer.set_points(0)
                        customer.set_points_usable(0)
                        customer.set_password_change([date.strftime("%Y"), date.strftime("%b"), date.strftime("%d")])
                        customers_dict[customer.get_email()] = customer
                        db["Customer"] = customers_dict
                        db.close()
                        return redirect(url_for('createaccount2', id=customer.get_email()))
            else:
                pass

    return render_template("Customer/createaccount.html", form=form)


@app.route("/createaccount2", methods=["GET", "POST"])
def createaccount2():
    form1 = CreateAccountForm1(request.form)
    email = request.args.get('id')
    db = shelve.open("customer.db", 'c')
    customers_dict = db["Customer"]
    customer = customers_dict.get(email)
    if request.method == "POST":
        # print(form1.credit_card.data)
        if form1.credit_card.data != "" and form1.csv.data != "":
            # print("hello")
            creditcard = CreditCard(form1.credit_card.data, form1.csv.data, 1)
            customer.update_credit_card(creditcard)
        if form1.credit_card.data != "" and form1.csv.data == "":
            return render_template("Customer/createaccount2.html", form=form1, warning=1)
        if form1.credit_card.data == "" and form1.csv.data != "":
            return render_template("Customer/createaccount2.html", form=form1, warning=2)
        if form1.address.data != "" and form1.city.data != "" and form1.zipcode.data is not None:
            customer.set_address(form1.address.data)
            customer.set_city(form1.city.data)
            customer.set_zipcode(form1.zipcode.data)
        if form1.address.data != "" and (form1.city.data == "" or form1.zipcode.data is None):
            return render_template("Customer/createaccount2.html", form=form1, warning=3)
        # if form1.address.data
        if form1.address.data == "" and (form1.city.data != "" or form1.zipcode.data is not None):
            return render_template("Customer/createaccount2.html", form=form1, warning=4)
        # print(form1.address.data)
        # print(customer.get_address())
        # print(customer.get_last_name())
        db["Customer"] = customers_dict
        # print(customer.get_credit_card())
        db.close()
        return redirect(url_for('createaccount3', id=customer.get_email()))
    return render_template("Customer/createaccount2.html", form=form1)


@app.route("/createaccount3", methods=["GET", "POST"])
def createaccount3():
    form2 = CreateAccountForm2(request.form)
    email = request.args.get('id')
    db = shelve.open("customer.db", 'c')
    customers_dict = db["Customer"]
    customer = customers_dict.get(email)
    if request.method == "POST":
        # print(customer.get_address())
        customer.set_security_qn1(form2.security_qn1.data)
        customer.set_security_qn2(form2.security_qn2.data)
        customer.set_security_qn3(form2.security_qn3.data)
        db["Customer"] = customers_dict
        db.close()
        return redirect(url_for("home"))

    return render_template("Customer/createaccount3.html", form=form2)


@app.route("/profile")
def profile():
    try:
        print(session['user'])
    except:
        return redirect(url_for("login", id=1))
    if session['user'] is None:
        return redirect(url_for("login", id=1))
    elif session['user'] == "":
        return redirect(url_for("login", id=1))
    else:
        # print(session['user'])
        db = shelve.open("customer.db", 'r')
        customers_dict = db["Customer"]
        email = session["user"]
        customer = customers_dict.get(email)

        # print(email)
        detail = "{} {}".format(customer.get_first_name(), customer.get_last_name())
        profile_pic = customer.get_profile_picture()
        # print(detail)
        # print(customer.get_first_name())
        return render_template("Customer/profile.html", details=detail, profile_pic=profile_pic)


@app.route("/personal")
def personal_info():
    if session["user"] is None:
        return redirect(url_for("login"))
    else:
        db = shelve.open("customer.db", 'r')
        customers_dict = db["Customer"]
        email = session["user"]
        customer = customers_dict.get(email)
        # print(customers_dict)
        profile_pic = customer.get_profile_picture()
        form = NewCreditCard(request.form)
        name = "{} {}".format(customer.get_first_name(), customer.get_last_name())
        birthday = customer.get_birthday()
        # print(customer.get_cid())
        phone = customer.get_phone()
        address = customer.get_address()
        zipcode = customer.get_zipcode()
        city = str(customer.get_city().capitalize())
        # password = customer.get_password()
        password_change = customer.get_password_change()
        payment = customer.get_credit_card()
        # print(payment)
        # print(password_change)
        last_change = "Last changed {} {}, {} ".format(password_change[1], password_change[2], password_change[0])
        gender = customer.get_gender()

        return render_template("Customer/personal_info.html", profile_pic=profile_pic, zipcode=zipcode, city=city,
                               birthday=birthday, form=form, details=name, name=name, gender=gender, email=email,
                               phone=phone, address=address, password_change=last_change, payment=payment,
                               customer=customer.get_email())


@app.route('/deleteCreditCard/<name>', methods=["POST"])
def delete_credit_card(name):
    db = shelve.open("customer.db", 'c')
    customers_dict = db["Customer"]
    email = session['user']
    customer = customers_dict.get(email)
    for i in range(0, len(customer.get_credit_card())):
        if str(customer.get_credit_card()[i].get_credit_card()) == str(name):
            # print("hi")
            customer.get_credit_card().pop(i)
            customer.set_credit_card(customer.get_credit_card())
            break

    db["Customer"] = customers_dict
    db.close()
    return redirect(url_for('personal_info'))


@app.route('/CreateCreditCard', methods=["POST", "GET"])
def new_credit_card():
    form = NewCreditCard(request.form)
    if request.method == "POST":
        db = shelve.open("customer.db", 'c')
        customers_dict = db["Customer"]
        customer = customers_dict.get(session['user'])

        if form.set_default.data is True:
            card = CreditCard(form.newcredit_card.data, form.newcsv.data, 1)
            for i in customer.get_credit_card():
                i.set_default(0)
        else:
            card = CreditCard(form.newcredit_card.data, form.newcsv.data, 0)
        customer.update_credit_card(card)
        db["Customer"] = customers_dict
        db.close()
        return redirect(url_for('personal_info'))
    return render_template("Customer/edit_credit_card.html", form=form)


@app.route('/setDefaultCreditCard/<name>', methods=["POST"])
def set_default_credit_card(name):
    db = shelve.open("customer.db", 'c')
    customers_dict = db["Customer"]
    customer = customers_dict.get(session['user'])
    # print(name)
    for i in customer.get_credit_card():
        if str(i.get_credit_card()) == str(name):
            i.set_default(1)
        else:
            i.set_default(0)
        # print(i.get_credit_card(), i.get_default())
    db["Customer"] = customers_dict
    db.close()
    return redirect(url_for('personal_info'))


@app.route("/contactus", methods=["GET", "POST"])
def contact_us():
    db = shelve.open("customer.db", 'c')
    customer = db['Customer'].get(session['user'])
    detail = customer.get_first_name() + " " + customer.get_last_name()
    profile_pic = customer.get_profile_picture()
    form = Feedback(request.form)
    feedback_dict = {}
    if request.method == "POST":
        try:
            if 'Feedback' in db:
                feedback_dict = db['Feedback']
            else:
                db["Feedback"] = feedback_dict
        except:
            print("File cannot be found ")
        feedback_dict[form.Email.data] = Feedbackuser(form.Name.data, form.Email.data, form.Message.data, 0)
        db["Feedback"] = feedback_dict
        db.close()
        return redirect(url_for("home"))
    return render_template("Customer/contactus.html", details=detail, form=form, profile_pic=profile_pic)


@app.route("/editphoto", methods=["POST", "GET"])
def edit_photo():
    form = Profile(request.form)
    if request.method == "POST":
        db = shelve.open("customer.db", 'c')
        customers_dict = db["Customer"]
        customer = customers_dict.get(session['user'])
        customer.set_profile_picture(form.base.data)
        db["Customer"] = customers_dict
        db.close()
        return redirect(url_for("personal_info"))

    return render_template("Customer/edit_photo.html", form=form)


@app.route("/editname", methods=["POST", "GET"])
def editname():
    form = Editname(request.form)
    if request.method == "POST":
        db = shelve.open("customer.db", 'c')
        customers_dict = db["Customer"]
        customer = customers_dict.get(session['user'])
        customer.set_first_name(form.first_name.data)
        customer.set_last_name(form.last_name.data)
        db["Customer"] = customers_dict
        db.close()
        return redirect(url_for("personal_info"))
    return render_template("Customer/edit_name.html", form=form)


@app.route("/editbirthday", methods=["POST", "GET"])
def editbirthday():
    form = Editbirthday(request.form)
    if request.method == "POST":
        db = shelve.open("customer.db", 'c')
        customers_dict = db["Customer"]
        customer = customers_dict.get(session['user'])
        # print(form.birthday.data)
        year = str(form.birthday.data)[0:4]
        month = str(form.birthday.data)[5:7]
        day = str(form.birthday.data)[8::]
        if month[0] == "0":
            month = int(month[1])
        monthinword = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        customer.set_birthday("{} {}, {}".format(monthinword[int(month) - 1], day, year))
        db["Customer"] = customers_dict
        db.close()
        return redirect(url_for("personal_info"))
    return render_template("Customer/edit_birthday.html", form=form)


@app.route("/editgender", methods=["POST", "GET"])
def editgender():
    form = Editgender(request.form)
    if request.method == "POST":
        db = shelve.open("customer.db", 'c')
        customers_dict = db["Customer"]
        customer = customers_dict.get(session['user'])
        customer.set_gender(form.gender.data)
        db["Customer"] = customers_dict
        db.close()
        return redirect(url_for("personal_info"))
    return render_template("Customer/edit_gender.html", form=form)


@app.route("/editemail", methods=["POST", "GET"])
def editemail():
    form = Editemail(request.form)
    warning = 0
    if request.method == "POST":
        db = shelve.open("customer.db", 'c')
        customers_dict = db["Customer"]
        customer = customers_dict.get(session['user'])
        if customers_dict.get(form.email.data) is None:
            customers_dict[form.email.data] = customers_dict[session['user']]
            customers_dict.pop(session['user'])
            # print(customers_dict)
            session['user'] = form.email.data
            customer = customers_dict.get(session['user'])
            customer.set_email(session['user'])
            # print(session['user'])
            db["Customer"] = customers_dict
            db.close()
        else:
            warning = 1
            return render_template("Customer/edit_email.html", warning=warning, form=form)
        return redirect(url_for("personal_info"))
    return render_template("Customer/edit_email.html", form=form, warning=warning)


@app.route("/editphone", methods=["GET", "POST"])
def editphone():
    form = Editphone(request.form)
    warning = 0
    if request.method == "POST":
        phone = form.phone.data
        if len(phone) != 8:
            warning = 1
            return render_template("Customer/edit_phone.html", warning=warning, form=form)
        for x in phone:
            if x.isalpha():
                warning = 1
                return render_template("Customer/edit_phone.html", warning=warning, form=form)

        db = shelve.open("customer.db", 'c')
        customers_dict = db["Customer"]
        customer = customers_dict.get(session['user'])
        customer.set_phone(form.phone.data)
        db["Customer"] = customers_dict
        db.close()
        return redirect(url_for("personal_info"))
    return render_template("Customer/edit_phone.html", form=form, warning=warning)


@app.route("/editaddress", methods=["GET", "POST"])
def editaddress():
    form = Editaddress(request.form)
    if request.method == "POST":
        db = shelve.open("customer.db", 'c')
        customers_dict = db["Customer"]
        customer = customers_dict.get(session['user'])
        customer.set_address(form.address.data)
        customer.set_zipcode(form.zipcode.data)
        customer.set_city(form.city.data)
        db["Customer"] = customers_dict
        db.close()
        return redirect(url_for("personal_info"))
    return render_template("Customer/edit_address.html", form=form)


@app.route("/editpassword", methods=["GET", "POST"])
def editpassword():
    form = Editpassword(request.form)
    if request.method == "POST":
        db = shelve.open("customer.db", 'c')
        customers_dict = db["Customer"]
        customer = customers_dict.get(session['user'])
        hashed = hashlib.sha3_256(form.current_password.data.encode())
        hashs = hashed.hexdigest()
        if hashs == customer.get_password() and form.new_password.data == form.confirm_new_password.data:
            hashing = hashlib.sha3_256(form.new_password.data.encode())
            customer.set_password(hashing.hexdigest())
            date = datetime.now()
            customer.set_password_change([date.strftime("%Y"), date.strftime("%b"), date.strftime("%d")])
            db["Customer"] = customers_dict
            db.close()
            return redirect(url_for("personal_info"))
    return render_template("Customer/edit_password.html", form=form)


@app.route("/customer_delete")
def customer_delete():
    email = session['user']
    db = shelve.open("customer.db", 'c')
    customer_dict = db["Customer"]
    customer_dict.pop(email)
    db["Customer"] = customer_dict
    db.close()
    session["user"] = None
    return redirect(url_for("home"))


@app.route("/customer_forget_password", methods=["GET", "POST"])
def customer_forget():
    form = Forget(request.form)
    notice = "A forget password email have been sent to your email"
    if request.method == "POST":
        db = shelve.open("customer.db", 'c')
        customer_dict = db["Customer"]
        customer = customer_dict.get(form.email.data)
        email = customer.get_email()
        token = customer.get_cid()
        message = "We received an inquire to reset your password, if is not you, ignore this email. key in your token:{} and new password with the following link to reset your password: http://127.0.0.1:5000/customer_forget_token".format(
            token)
        with app.app_context():
            msg = Message(subject="Reset Password", sender="SingtopiaSG@gmail.com", recipients=[email], body=message)
            mail.send(msg)
            return render_template("Customer/customer_forget.html", form=form, notice=notice)
    return render_template("Customer/customer_forget.html", form=form)


@app.route("/customer_forget_token", methods=["GET", "POST"])
def customer_token():
    form = ForgetAcc(request.form)
    db = shelve.open("customer.db", "r")
    customer_dict = db["Customer"]
    for i in customer_dict:
        print(customer_dict[i].get_cid())
        if customer_dict[i].get_cid() == form.token.data:
            email = customer_dict[i].get_email()
            return redirect(url_for("customer_forget_2", id=email))
    return render_template("Customer/customer_token.html", form=form)


@app.route("/customer_forget_password2", methods=["POST", "GET"])
def customer_forget_2():
    form = CreateAccountForm2(request.form)
    email = request.args.get('id')
    db = shelve.open("customer.db", 'r')
    customer_dict = db["Customer"]
    customer = customer_dict.get(email)
    if request.method == "POST":
        if str(customer.get_security_qn1()) == str(form.security_qn1.data) and str(customer.get_security_qn2()) == str(
                form.security_qn2.data) and str(customer.get_security_qn3()) == str(form.security_qn3.data):
            return redirect(url_for("customer_new_password", id=email))
    return render_template("Customer/customer_forget_password2.html", form=form)


@app.route("/customer_new_password", methods=["GET", "POST"])
def customer_new_password():
    form = New_password(request.form)
    email = request.args.get("id")
    if request.method == "POST":
        db = shelve.open("customer.db", 'c')
        customer_dict = db["Customer"]
        customer = customer_dict.get(email)
        hashed = hashlib.sha3_256(form.password.data.encode())
        customer.set_password(hashed.hexdigest())
        date = datetime.now()
        customer.set_password_change([date.strftime("%Y"), date.strftime("%b"), date.strftime("%d")])
        customer.set_cid(str(uuid4()))
        db["Customer"] = customer_dict
        db.close()
        return redirect(url_for("login"))
    return render_template("Customer/customer_new_password.html", form=form)


# @app.route("/purchase")
# def purchase_info():
#     email = session['user']
#     db = shelve.open("customer.db", 'r')
#     customer_dict = db["Customer"]
#     customer = customer_dict.get(email)
#     merchant_dict = db["Merchant"]
#     merchant = merchant_dict.get("aikleong0713@gmail.com")
#     products_dict = merchant.get_products()
#     detail = "{} {}".format(customer.get_first_name(), customer.get_last_name())
#     profile_pic = customer.get_profile_picture()
#     return render_template("Customer/customer_purchase.html",
#                            profile_pic=profile_pic, details=detail, products_dict=products_dict)


@app.route("/review/<email>/<id>", methods=["POST", "GET"])
def review(email, id):
    form = Review_form(request.form)
    db = shelve.open("customer.db", 'c')
    merchant_dict = db["Merchant"]
    merchant = merchant_dict.get(email)

    product_dict = merchant.get_products()
    customer_dict = db["Customer"]
    email = session['user']
    customer = customer_dict.get(email)
    product = product_dict.get(id)

    if request.method == "POST":
        reviews = Review(customer, form.review.data, form.rating.data)
        product_dict.get(id).add_review(reviews)
        db["Merchant"] = merchant_dict
        db["Customer"] = customer_dict
        db.close()
        return redirect(url_for("purchaseHistory"))

    detail = "{} {}".format(customer.get_first_name(), customer.get_last_name())
    profile_pic = customer.get_profile_picture()
    return render_template("Customer/review.html", profile_pic=profile_pic, details=detail, product=product, form=form)


@app.route("/web_rewards")
def web_rewards():
    db = shelve.open("customer.db", 'r')
    customers_dict = db["Customer"]
    email = session["user"]
    customer = customers_dict.get(email)
    profile_pic = customer.get_profile_picture()
    detail = "{} {}".format(customer.get_first_name(), customer.get_last_name())
    customer_point = customer.get_points()
    customer_point_usable = customer.get_points_usable()
    db.close()
    CWR_dict = {}
    try:
        db = shelve.open('WebReward.db', 'r')
        CWR_dict = db['WebRewards']
    except:
        db = shelve.open('WebReward.db', "c")
        db["WebRewards"] = CWR_dict

    db.close()
    List_iron = []
    List_bronze = []
    List_silver = []
    List_gold = []
    List_platinum = []
    List_diamond = []

    cust_chosen_wr_cart = list(dict.fromkeys(customer.get_rewards_indiv()))
    # print(cust_chosen_wr_cart)

    cust_wr_inlist = []
    for key in CWR_dict:
        web_reward = CWR_dict.get(key)
        cust_wr_inlist.append(web_reward)

    correct = []
    for x in cust_wr_inlist:
        if x.get_count() not in cust_chosen_wr_cart:
            correct.append(x)
        else:
            pass
    # if cust_wr_inlist == None:
    #     for kok in range(len(cust_chosen_wr_cart)):
    #         cust_wr_inlist.pop(kok)
    # else:
    #     pass

    cust_wr_inlist = list(dict.fromkeys(cust_wr_inlist))
    # print(correct, "smlj")
    # print(CWR_dict, "sui")
    for i in correct:
        if i.get_rank() == "Iron":
            List_iron.append(i.get_count())
        elif i.get_rank() == "Bronze":
            List_bronze.append(i.get_count())
        elif i.get_rank() == "Silver":
            List_silver.append(i.get_count())
        elif i.get_rank() == "Gold":
            List_gold.append(i.get_count())
        elif i.get_rank() == "Platinum":
            List_platinum.append(i.get_count())
        elif i.get_rank() == "Diamond":
            List_diamond.append(i.get_count())

    shoppingCarts = {}
    shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
    try:
        if "shoppingCart" in shoppingCartDB:  # is key exist?
            shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
        else:
            print("Shopping carts has an error.")  # start with empty
    except:
        print("Error in retrieving shopVouchers from vouchers.db.")

    userShoppingCart = None  # retrieves the shopping cart object
    try:
        if session['user'] in shoppingCarts:
            userShoppingCart = shoppingCarts[session['user']]
        else:
            print("Can't retrieve the user's shopping cart.")
    except:
        print("Error occured in dictionary.")
    shoppingCartDB.close()

    return render_template("customer/customer_web_rewards.html", profile_pic=profile_pic, customer=customer, details=detail, customer_point=customer_point,
                           customer_point_usable=customer_point_usable, list_Web_rewards=correct,
                           userShoppingCart=userShoppingCart, List_iron=List_iron, List_bronze=List_bronze,
                           List_silver=List_silver, List_gold=List_gold, List_platinum=List_platinum,
                           List_diamond=List_diamond, cust_chosen_wr_cart=cust_chosen_wr_cart)

@app.route("/campaign")
def page_campaign():
    shoppingCarts = {}
    shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
    try:
        if "shoppingCart" in shoppingCartDB:  # is key exist?
            shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
        else:
            print("Shopping carts has an error.")  # start with empty
    except:
        print("Error in retrieving shopVouchers from vouchers.db.")

    userShoppingCart = ShoppingCart(session['user'])  # retrieves the shopping cart object
    try:
        if session['user'] in shoppingCarts:
            userShoppingCart = shoppingCarts[session['user']]
        else:
            print("Can't retrieve the user's shopping cart.")
    except:
        print("Error occured in dictionary.")
    shoppingCartDB.close()

    CD_dict = {}
    try:
        db = shelve.open('Campaign.db', 'r')
        CD_dict = db['Campaign']
    except:
        db = shelve.open('Campaign.db', "c")
        db["Campaign"] = CD_dict
    db.close()

    cvd_dict = {}
    try:
        db = shelve.open('CampaignVchers.db', 'r')
        cvd_dict = db['CampaignVchers']
    except:
        db = shelve.open('CampaignVchers.db', "c")
        db["CampaignVchers"] = cvd_dict
    db.close()
    show_list = []
    for key in cvd_dict:
        camp_vch = cvd_dict.get(key)
        show_list.append(camp_vch)

    current_time = date.today()

    camp_list = []
    for camp in CD_dict:
        camp_now = CD_dict.get(camp)
        camp_list.append(camp_now)
    print(camp_list,"total camp")

    # Aaralyn Part
    shoppingCarts = {}
    shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
    try:
        if "shoppingCart" in shoppingCartDB:  # is key exist?
            shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
        else:
            print("Shopping carts has an error.")  # start with empty
    except:
        print("Error in retrieving shopVouchers from vouchers.db.")

    userShoppingCart = None  # retrieves the shopping cart object
    try:
        if session['user'] in shoppingCarts:
            userShoppingCart = shoppingCarts[session['user']]
        else:
            print("Can't retrieve the user's shopping cart.")
    except:
        print("Error occured in dictionary.")
    shoppingCartDB.close()

    noOfItems = 0
    productList = []
    totalPrice = 0
    if userShoppingCart != None:
        merchant_dict = userShoppingCart.get_merchants()
        for merchantEmail in merchant_dict:
            merchantObject = merchant_dict[merchantEmail]
            product_list = merchantObject.get_products()
            for product in product_list:
                productList.append(product)
                noOfItems += 1
                totalPrice += round(product.get_totalPrice(), 2)

    return render_template("common/campaign_page.html", show_list=show_list, date=current_time, CD_dict=CD_dict,
                           userShoppingCart=userShoppingCart, camp_list=camp_list, totalPrice=totalPrice,
                           noOfItems=noOfItems,
                           productList=productList)


@app.route("/marketing_strategy")
def marketing_strategy():
    db = shelve.open("customer.db", "r")
    m_dict = db["Merchant"]
    merchant = m_dict.get(session['user'])
    return render_template("Merchant/marketing_strategy.html", merchant=merchant)


@app.route("/merchant_shopvouchers")
def merchant_shopvouchers():

    db = shelve.open("customer.db", "r")
    m_dict = db["Merchant"]
    merchant = m_dict.get(session["user"])
    db.close()

    shopVoucher_dict = {}
    db = shelve.open('shopVoucherFixedAmt.db', 'c')
    # shopVoucher_dict={merchant email:{shop voucher code: shop voucher object}}
    try:
        if 'shopVouchers' in db:  # is key exist?
            shopVoucher_dict = db['shopVouchers']  # retrieve data
        else:
            db['shopVouchers'] = shopVoucher_dict  # start with empty
    except:
        print("Error in retrieving shopVouchers from vouchers.db.")
    merchantShopVoucher_dict = {}
    try:
        if session['user'] in shopVoucher_dict:
            merchantShopVoucher_dict = shopVoucher_dict[session['user']]
        else:
            shopVoucher_dict[session['user']] = merchantShopVoucher_dict
    except:
        print("Error occured in shop voucher dictionary.")

    voucher_list=[]
    for key in merchantShopVoucher_dict:
        voucher=merchantShopVoucher_dict.get(key)
        voucher.set_status()
        merchantShopVoucher_dict[key]=voucher
        voucher_list.append(voucher)

    shopVoucher_dict[session['user']] = merchantShopVoucher_dict
    db['shopVouchers'] = shopVoucher_dict
    db.close()

    db = shelve.open('shopVouchersPercentage.db', 'c')
    shopVoucher_dict={}
    # shopVoucher_dict={merchant email:{shop voucher code: shop voucher object}}
    try:
        if 'shopVouchersPercentage' in db:  # is key exist?
            shopVoucher_dict = db['shopVouchersPercentage']  # retrieve data
        else:
            print("Error in retrieving from shopVouchersPercentage.db")
    except:
        print("Error in retrieving shopVouchers from vouchers.db.")
    merchantShopVoucher_dict = {}
    try:
        if session["user"] in shopVoucher_dict:
            merchantShopVoucher_dict = shopVoucher_dict[session['user']]
        else:
            print("Error in retrieving from shopVouchersPercentage.db")
    except:
        print("Error occured in shop voucher dictionary.")

    voucherPercentage_list=[]
    for key in merchantShopVoucher_dict:
        voucher=merchantShopVoucher_dict.get(key)
        voucher.set_status()
        merchantShopVoucher_dict[key]=voucher
        voucherPercentage_list.append(voucher)

    shopVoucher_dict[session['user']] = merchantShopVoucher_dict
    db['shopVouchersPercentage'] = shopVoucher_dict
    db.close()

    return render_template("merchant/merchant_shopvouchers.html",voucher_list=voucher_list,
                           voucherPercentage_list=voucherPercentage_list,merchant=merchant)


@app.route("/merchant_create_fixed_amount_voucher", methods=['GET', 'POST'])
def create_merchant_shop_voucher_fixed_amount():
    warningDate = 0
    db = shelve.open("customer.db", "r")
    m_dict = db["Merchant"]
    merchant = m_dict.get(session["user"])
    db.close()
    warningmessage = ""
    create_shopvoucher_fixedAmt_form = CreateMerchantShopVoucherFixedAmt(request.form)
    # maybe i can just add more validation like the name cannot be the same or wtv
    if request.method == 'POST' and create_shopvoucher_fixedAmt_form.validate():

        # custom validaiton
        startdate = create_shopvoucher_fixedAmt_form.startingDate.data
        enddate = create_shopvoucher_fixedAmt_form.endingDate.data
        if enddate < startdate:
            warningDate = 1
            warningmessage = "End Date cannot be before Start Date."
            return render_template("merchant/create_merchant_shopvoucher_fixedAmt.html", merchant=merchant,
                                   form=create_shopvoucher_fixedAmt_form,
                                   warningDate=warningDate, warningmessage=warningmessage)

        elif startdate < date.today():
            warningDate = 1
            warningmessage = "Start Date cannot be before today's date."
            return render_template("merchant/create_merchant_shopvoucher_fixedAmt.html", merchant=merchant,
                                   form=create_shopvoucher_fixedAmt_form,
                                   warningDate=warningDate, warningmessage=warningmessage)

        elif startdate > enddate:
            warningDate = 1
            warningmessage = "Start Date cannot be after End Date."
            return render_template("merchant/create_merchant_shopvoucher_fixedAmt.html", merchant=merchant,
                                   form=create_shopvoucher_fixedAmt_form,
                                   warningDate=warningDate, warningmessage=warningmessage)

        elif enddate < date.today():
            warningDate = 1
            warningmessage = "End Date cannot be before Today's Date."
            return render_template("merchant/create_merchant_shopvoucher_fixedAmt.html", merchant=merchant,
                                   form=create_shopvoucher_fixedAmt_form,
                                   warningDate=warningDate, warningmessage=warningmessage)

        shopVoucher_dict = {}
        db = shelve.open('shopVoucherFixedAmt.db', 'c')
        # shopVoucher_dict={merchant email:{shop voucher code: shop voucher object}}
        try:
            if 'shopVouchers' in db:  # is key exist?
                shopVoucher_dict = db['shopVouchers']  # retrieve data
            else:
                db['shopVouchers'] = shopVoucher_dict  # start with empty
        except:
            print("Error in retrieving shopVouchers from vouchers.db.")
        merchantShopVoucher_dict = {}
        try:
            if session['user'] in shopVoucher_dict:
                merchantShopVoucher_dict = shopVoucher_dict[session['user']]
            else:
                shopVoucher_dict[session['user']] = merchantShopVoucher_dict
        except:
            print("Error occured in shop voucher dictionary.")

        voucher = shopVoucherFixedAmt(create_shopvoucher_fixedAmt_form.name.data,
                                      create_shopvoucher_fixedAmt_form.startingDate.data,
                                      create_shopvoucher_fixedAmt_form.endingDate.data,
                                      create_shopvoucher_fixedAmt_form.minSpend.data,
                                      create_shopvoucher_fixedAmt_form.usageQuantity.data)

        voucher.set_status()

        voucher.set_fixedAmt(create_shopvoucher_fixedAmt_form.fixedAmtOff.data)
        merchantShopVoucher_dict[voucher.get_code()] = voucher
        shopVoucher_dict[session['user']] = merchantShopVoucher_dict
        db['shopVouchers'] = shopVoucher_dict

        # testcodes
        shopVoucher_dict = db['shopVouchers']
        merchantShopVoucher_dict = shopVoucher_dict[session['user']]
        voucher = merchantShopVoucher_dict[voucher.get_code()]
        print(voucher.get_name(), "was stored in shopVoucherFixedAmt.db successfully with voucher code==",
              voucher.get_code())

        db.close()

        return redirect(url_for('merchant_shopvouchers'))
    return render_template("merchant/create_merchant_shopvoucher_fixedAmt.html", merchant=merchant,
                           form=create_shopvoucher_fixedAmt_form,
                           warningDate=warningDate, warningmessage=warningmessage)


@app.route('/update_merchant_shopvoucher_fixedAmt/<code>/', methods=['GET', 'POST'])
def update_merchant_fixedAmtVoucher(code):
    warningmessage = ""
    warningDate = 0
    db = shelve.open("customer.db", "r")
    m_dict = db['Merchant']
    merchant = m_dict.get(session['user'])
    db.close()
    update_shopvoucher_fixedAmt_form = CreateMerchantShopVoucherFixedAmt(request.form)
    if request.method == 'POST' and update_shopvoucher_fixedAmt_form.validate():
        startdate = update_shopvoucher_fixedAmt_form.startingDate.data
        enddate = update_shopvoucher_fixedAmt_form.endingDate.data
        if enddate < startdate:
            warningDate = 1
            warningmessage = "End Date cannot be before Start Date."
            return render_template("merchant/update_merchant_shopvoucher_fixedAmt.html", merchant=merchant,
                                   form=update_shopvoucher_fixedAmt_form,
                                   warningDate=warningDate, warningmessage=warningmessage)

        elif startdate < date.today():
            warningDate = 1
            warningmessage = "Start Date cannot be before today's date."
            return render_template("merchant/update_merchant_shopvoucher_fixedAmt.html", merchant=merchant,
                                   form=update_shopvoucher_fixedAmt_form,
                                   warningDate=warningDate, warningmessage=warningmessage)

        elif startdate > enddate:
            warningDate = 1
            warningmessage = "Start Date cannot be after End Date."
            return render_template("merchant/update_merchant_shopvoucher_fixedAmt.html", merchant=merchant,
                                   form=update_shopvoucher_fixedAmt_form,
                                   warningDate=warningDate, warningmessage=warningmessage)



        elif enddate < date.today():
            warningDate = 1
            warningmessage = "End Date cannot be before Today's Date."
            return render_template("merchant/update_merchant_shopvoucher_fixedAmt.html", merchant=merchant,
                                   form=update_shopvoucher_fixedAmt_form,
                                   warningDate=warningDate, warningmessage=warningmessage)
        shopVoucher_dict = {}
        db = shelve.open('shopVoucherFixedAmt.db', 'w')
        shopVoucher_dict = db['shopVouchers']
        merchantShopVoucher_dict = shopVoucher_dict[session['user']]

        voucher = merchantShopVoucher_dict.get(code)
        voucher.set_name(update_shopvoucher_fixedAmt_form.name.data)
        voucher.set_startingDate(update_shopvoucher_fixedAmt_form.startingDate.data)
        voucher.set_endingDate(update_shopvoucher_fixedAmt_form.endingDate.data)
        voucher.set_minSpend(update_shopvoucher_fixedAmt_form.minSpend.data)
        voucher.set_usageQuantity(update_shopvoucher_fixedAmt_form.usageQuantity.data)
        voucher.set_fixedAmt(update_shopvoucher_fixedAmt_form.fixedAmtOff.data)

        voucher.set_status()

        shopVoucher_dict[session['user']] = merchantShopVoucher_dict
        db['shopVouchers'] = shopVoucher_dict
        db.close()
        return redirect(url_for('merchant_shopvouchers'))
    else:
        shopVoucher_dict = {}
        db = shelve.open('shopVoucherFixedAmt.db', 'c')
        shopVoucher_dict = db['shopVouchers']
        merchantShopVoucher_dict = shopVoucher_dict[session['user']]
        db.close()

        voucher = merchantShopVoucher_dict.get(code)
        update_shopvoucher_fixedAmt_form.name.data = voucher.get_name()
        update_shopvoucher_fixedAmt_form.startingDate.data = voucher.get_startingDate()
        update_shopvoucher_fixedAmt_form.endingDate.data = voucher.get_endingDate()
        update_shopvoucher_fixedAmt_form.minSpend.data = voucher.get_minSpend()
        update_shopvoucher_fixedAmt_form.usageQuantity.data = voucher.get_usageQuantity()
        update_shopvoucher_fixedAmt_form.fixedAmtOff.data = voucher.get_fixedAmt()

        return render_template("merchant/update_merchant_shopvoucher_fixedAmt.html", merchant=merchant,
                               form=update_shopvoucher_fixedAmt_form,
                               warningDate=warningDate, warningmessage=warningmessage)


@app.route("/deleteShopVoucher/<code>", methods=['POST'])
def delete_shopvoucher(code):
    shopVoucher_dict = {}
    db = shelve.open('shopVoucherFixedAmt.db', 'w')
    shopVoucher_dict = db['shopVouchers']
    merchantShopVoucher_dict = shopVoucher_dict[session['user']]

    merchantShopVoucher_dict.pop(code)

    shopVoucher_dict[session['user']] = merchantShopVoucher_dict
    db['shopVouchers'] = shopVoucher_dict
    db.close()

    return redirect(url_for('merchant_shopvouchers'))


# starting on the shopvoucher percentage off
@app.route("/merchant_create_percentage_voucher", methods=['GET', 'POST'])
def create_merchant_shop_voucher_percentage():
    warningDate = 0
    warningmessage = ""
    db = shelve.open("customer.db", "r")
    m_dict = db["Merchant"]
    merchant = m_dict.get(session["user"])
    db.close()
    create_shopvoucher_percentage_form = CreateMerchantShopVoucherPercentage(request.form)
    if request.method == 'POST' and create_shopvoucher_percentage_form.validate():

        # custom validaiton
        startdate = create_shopvoucher_percentage_form.startingDate.data
        enddate = create_shopvoucher_percentage_form.endingDate.data
        if enddate < startdate:
            warningDate = 1
            warningmessage = "End Date cannot be before Start Date."
            return render_template("merchant/create_merchant_shopvoucher_percentage.html", merchant=merchant,
                                   form=create_shopvoucher_percentage_form,
                                   warningDate=warningDate, warningmessage=warningmessage)

        elif startdate < date.today():
            warningDate = 1
            warningmessage = "Start Date cannot be before today's date."
            return render_template("merchant/create_merchant_shopvoucher_percentage.html", merchant=merchant,
                                   form=create_shopvoucher_percentage_form,
                                   warningDate=warningDate, warningmessage=warningmessage)

        elif startdate > enddate:
            warningDate = 1
            warningmessage = "Start Date cannot be after End Date."
            return render_template("merchant/create_merchant_shopvoucher_percentage.html", merchant=merchant,
                                   form=create_shopvoucher_percentage_form,
                                   warningDate=warningDate, warningmessage=warningmessage)

        elif enddate < date.today():
            warningDate = 1
            warningmessage = "End Date cannot be before Today's Date."
            return render_template("merchant/create_merchant_shopvoucher_percentage.html", merchant=merchant,
                                   form=create_shopvoucher_percentage_form,
                                   warningDate=warningDate, warningmessage=warningmessage)

        shopVoucher_dict = {}
        db = shelve.open('shopVouchersPercentage.db', 'c')
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
            if session['user'] in shopVoucher_dict:
                merchantShopVoucher_dict = shopVoucher_dict[session['user']]
            else:
                shopVoucher_dict[session['user']] = merchantShopVoucher_dict
        except:
            print("Error occured in shop voucher dictionary.")


        voucher = shopVoucherPercentage(create_shopvoucher_percentage_form.name.data,
                                        create_shopvoucher_percentage_form.startingDate.data,
                                        create_shopvoucher_percentage_form.endingDate.data,
                                        create_shopvoucher_percentage_form.minSpend.data,
                                        create_shopvoucher_percentage_form.usageQuantity.data,
                                        create_shopvoucher_percentage_form.percentageOff.data)

        voucher.set_status()

        if create_shopvoucher_percentage_form.CappedPrice.data == 0:
            voucher.set_cappedAmtType("noLimit")
        else:
            voucher.set_cappedAmtType("setAmt")
            voucher.set_cappedAmt(create_shopvoucher_percentage_form.CappedPrice.data)

        merchantShopVoucher_dict[voucher.get_code()] = voucher
        shopVoucher_dict[session['user']] = merchantShopVoucher_dict
        db['shopVouchersPercentage'] = shopVoucher_dict

        # testcodes
        shopVoucher_dict = db['shopVouchersPercentage']
        merchantShopVoucher_dict = shopVoucher_dict[session['user']]
        voucher = merchantShopVoucher_dict[voucher.get_code()]
        print(voucher.get_name(), "was stored in shopVouchersPercentage.db successfully with voucher code==",
              voucher.get_code(), voucher.get_discountType())
        db.close()

        return redirect(url_for('merchant_shopvouchers'))
    return render_template("merchant/create_merchant_shopvoucher_percentage.html", merchant=merchant,
                           form=create_shopvoucher_percentage_form,
                           warningDate=warningDate, warningmessage=warningmessage)


@app.route('/update_merchant_shopvoucher_percentage/<code>/', methods=['GET', 'POST'])
def update_merchant_percentageVoucher(code):
    warningmessage = ""
    warningDate = 0
    db = shelve.open("customer.db", "r")
    m_dict = db["Merchant"]
    merchant = m_dict.get(session['user'])
    db.close()
    update_shopvoucher_percentage_form = CreateMerchantShopVoucherPercentage(request.form)
    if request.method == 'POST' and update_shopvoucher_percentage_form.validate():
        startdate = update_shopvoucher_percentage_form.startingDate.data
        enddate = update_shopvoucher_percentage_form.endingDate.data
        if enddate < startdate:
            warningDate = 1
            warningmessage = "End Date cannot be before Start Date."
            return render_template("merchant/update_merchant_shopvoucher_percentage.html", merchant=merchant,
                                   form=update_shopvoucher_percentage_form,
                                   warningDate=warningDate, warningmessage=warningmessage)

        elif startdate < date.today():
            warningDate = 1
            warningmessage = "Start Date cannot be before today's date."
            return render_template("merchant/update_merchant_shopvoucher_percentage.html", merchant=merchant,
                                   form=update_shopvoucher_percentage_form,
                                   warningDate=warningDate, warningmessage=warningmessage)

        elif startdate > enddate:
            warningDate = 1
            warningmessage = "Start Date cannot be after End Date."
            return render_template("merchant/update_merchant_shopvoucher_percentage.html", merchant=merchant,
                                   form=update_shopvoucher_percentage_form,
                                   warningDate=warningDate, warningmessage=warningmessage)

        elif enddate < date.today():
            warningDate = 1
            warningmessage = "End Date cannot be before Today's Date."
            return render_template("merchant/update_merchant_shopvoucher_percentage.html", merchant=merchant,
                                   form=update_shopvoucher_percentage_form,
                                   warningDate=warningDate, warningmessage=warningmessage)
        shopVoucher_dict = {}
        db = shelve.open('shopVouchersPercentage.db', 'c')
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
            if session['user'] in shopVoucher_dict:
                merchantShopVoucher_dict = shopVoucher_dict[session['user']]
            else:
                shopVoucher_dict[session['user']] = merchantShopVoucher_dict
        except:
            print("Error occured in shop voucher dictionary.")

        voucher = merchantShopVoucher_dict.get(code)
        voucher.set_name(update_shopvoucher_percentage_form.name.data)
        voucher.set_startingDate(update_shopvoucher_percentage_form.startingDate.data)
        voucher.set_endingDate(update_shopvoucher_percentage_form.endingDate.data)
        voucher.set_minSpend(update_shopvoucher_percentage_form.minSpend.data)
        voucher.set_usageQuantity(update_shopvoucher_percentage_form.usageQuantity.data)
        voucher.set_percentageOff(update_shopvoucher_percentage_form.percentageOff.data)
        if update_shopvoucher_percentage_form.CappedPrice.data == 0:
            voucher.set_cappedAmtType("noLimit")
        else:
            voucher.set_cappedAmtType("setAmt")
            voucher.set_cappedAmt(update_shopvoucher_percentage_form.CappedPrice.data)
        voucher.set_status()

        merchantShopVoucher_dict[voucher.get_code()] = voucher
        shopVoucher_dict[session['user']] = merchantShopVoucher_dict
        db['shopVouchersPercentage'] = shopVoucher_dict
        db.close()
        return redirect(url_for('merchant_shopvouchers'))
    else:
        shopVoucher_dict = {}
        db = shelve.open('shopVouchersPercentage.db', 'r')
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
            if session['user'] in shopVoucher_dict:
                merchantShopVoucher_dict = shopVoucher_dict[session['user']]
            else:
                shopVoucher_dict[session['user']] = merchantShopVoucher_dict
        except:
            print("Error occured in shop voucher dictionary.")
        db.close()

        voucher = merchantShopVoucher_dict.get(code)
        update_shopvoucher_percentage_form.name.data = voucher.get_name()
        update_shopvoucher_percentage_form.startingDate.data = voucher.get_startingDate()
        update_shopvoucher_percentage_form.endingDate.data = voucher.get_endingDate()
        update_shopvoucher_percentage_form.minSpend.data = voucher.get_minSpend()
        update_shopvoucher_percentage_form.usageQuantity.data = voucher.get_usageQuantity()
        update_shopvoucher_percentage_form.percentageOff.data = voucher.get_percentageOff()
        update_shopvoucher_percentage_form.CappedPrice.data = voucher.get_cappedAmt()

        return render_template("merchant/update_merchant_shopvoucher_percentage.html", merchant=merchant,
                               form=update_shopvoucher_percentage_form,
                               warningDate=warningDate, warningmessage=warningmessage)


@app.route("/deleteShopVoucherPercentage/<code>", methods=['POST'])
def delete_shopvoucher_percentage(code):
    shopVoucher_dict = {}
    db = shelve.open('shopVouchersPercentage.db', 'c')
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
        if session['user'] in shopVoucher_dict:
            merchantShopVoucher_dict = shopVoucher_dict[session['user']]
        else:
            shopVoucher_dict[session['user']] = merchantShopVoucher_dict
    except:
        print("Error occured in shop voucher dictionary.")

    merchantShopVoucher_dict.pop(code)

    shopVoucher_dict[session['user']] = merchantShopVoucher_dict
    db['shopVouchersPercentage'] = shopVoucher_dict
    db.close()

    return redirect(url_for('merchant_shopvouchers'))


@app.route("/discountPromo_page")
def discountPromotions():
    db = shelve.open("customer.db", "r")
    m_dict = db["Merchant"]
    merchant = m_dict.get(session['user'])
    db.close()
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
        if session['user'] in discountPromo_dict:
            merchantDiscounts_dict = discountPromo_dict[session['user']]
        else:
            discountPromo_dict[session['user']] = merchantDiscounts_dict
    except:
        print("Error occured in shop discounts dictionary.")

    discountList=[]
    for discount in merchantDiscounts_dict:
        merchantDiscounts_dict[discount].set_status()
        discountList.append(merchantDiscounts_dict[discount])

    discountPromo_dict[session['user']] = merchantDiscounts_dict
    DiscountPromodb['discountPromo'] = discountPromo_dict
    DiscountPromodb.close()

    return render_template("merchant/discountPromo_page.html", merchant=merchant, discountList=discountList)


# store the basic info into a temporary db which the key will be "discountPromoBasicInfo"
# then direct it to the add product page where they can submit the product and then from there add it to the correct db


@app.route("/create_discountPromotion", methods=['GET', 'POST'])
def create_discount_promo():
    db = shelve.open("customer.db", "r")
    m_dict = db['Merchant']
    merchant = m_dict.get(session['user'])
    db.close()
    warningDate = 0
    warningmessage = ""
    # db["discountPromo"]={email:{discountPromoCode:discountPromoObject}}
    create_discountPromo_form = CreateProductDiscount(request.form)
    if request.method == 'POST' and create_discountPromo_form.validate():
        # maybe i can just add more validation like the name cannot be the same or wtv
        # custom validaiton
        startdate = create_discountPromo_form.startingDate.data
        enddate = create_discountPromo_form.endingDate.data
        if enddate < startdate:
            warningDate = 1
            warningmessage = "End Date cannot be before Start Date."
            return render_template("merchant/create_discountPromo.html", merchant=merchant,
                                   form=create_discountPromo_form,
                                   warningDate=warningDate, warningmessage=warningmessage)

        elif startdate < date.today():
            warningDate = 1
            warningmessage = "Start Date cannot be before today's date."
            return render_template("merchant/create_discountPromo.html", merchant=merchant,
                                   form=create_discountPromo_form,
                                   warningDate=warningDate, warningmessage=warningmessage)

        elif startdate > enddate:
            warningDate = 1
            warningmessage = "Start Date cannot be after End Date."
            return render_template("merchant/create_discountPromo.html", merchant=merchant,
                                   form=create_discountPromo_form,
                                   warningDate=warningDate, warningmessage=warningmessage)

        elif enddate < date.today():
            warningDate = 1
            warningmessage = "End Date cannot be before Today's Date."
            return render_template("merchant/create_discountPromo.html", merchant=merchant,
                                   form=create_discountPromo_form,
                                   warningDate=warningDate, warningmessage=warningmessage)

        discountPromoBasicInfo_dict = {}
        db = shelve.open('temporary.db', 'c')
        try:
            if 'discountPromoBasicInfo' in db:
                discountPromoBasicInfo_dict = db["discountPromoBasicInfo"]
            else:
                db["discountPromoBasicInfo"] = discountPromoBasicInfo_dict
        except:
            print("Error occured in shop Temporary dictionary.")

        discountPromoBasicInfo_dict["name"] = create_discountPromo_form.name.data
        discountPromoBasicInfo_dict["startingDate"] = create_discountPromo_form.startingDate.data
        discountPromoBasicInfo_dict["endingDate"] = create_discountPromo_form.endingDate.data

        db["discountPromoBasicInfo"] = discountPromoBasicInfo_dict
        db.close()

        return redirect(url_for('discount_promo_addProduct'))
    return render_template("merchant/create_discountPromo.html", merchant=merchant, form=create_discountPromo_form,
                           warningDate=warningDate,
                           warningmessage=warningmessage)


@app.route("/create_discountPromo_addProduct")
def discount_promo_addProduct():
    # place jk merchant products inside
    db = shelve.open('customer.db', 'r')
    muser_dict = db["Merchant"]
    db.close()
    merchant = muser_dict.get(session['user'])
    products_dict = merchant.get_products()
    product_list = []
    for key in products_dict:
        product = products_dict.get(key)
        product_list.append(product)

    # searching thru the list if product has been used
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
        if session['user'] in discountPromo_dict:
            merchantDiscounts_dict = discountPromo_dict[session['user']]
        else:
            discountPromo_dict[session['user']] = merchantDiscounts_dict
    except:
        print("Error occured in shop discounts dictionary.")

    usedProductCode_list = []
    for count in merchantDiscounts_dict:
        usedProductCode_list.append(merchantDiscounts_dict[count].get_productCode())

    for product in product_list:
        for usedID in usedProductCode_list:
            if product.get_product_id() == usedID:
                product_list.remove(product)
                break

    return render_template("merchant/discountPromo_addProduct.html", merchant=merchant, product_list=product_list)


@app.route("/create_discountPromo/<id>/", methods=['GET', 'POST'])
def editing_product_discountPromo(id):
    # place all merchant products inside
    db = shelve.open('customer.db', 'r')
    muser_dict = db["Merchant"]
    db.close()
    merchant = muser_dict.get(session['user'])
    products_dict = merchant.get_products()
    print(products_dict)
    chosenProduct = None
    for key in products_dict:
        if key == id:
            chosenProduct = products_dict[key]

    create_discountPromo_form_1 = CreateProductDiscount_1(request.form)
    if request.method == 'POST' and create_discountPromo_form_1.validate():
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
            if session['user'] in discountPromo_dict:
                merchantDiscounts_dict = discountPromo_dict[session['user']]
            else:
                discountPromo_dict[session['user']] = merchantDiscounts_dict
        except:
            print("Error occured in shop discounts dictionary.")


        discountProduct = DiscountProduct(chosenProduct.get_product_name(), id, chosenProduct.get_quantity(),
                                          chosenProduct.get_product_price(),
                                          create_discountPromo_form_1.discount.data,
                                          create_discountPromo_form_1.purchaseLimit.data)
        if discountProduct.get_purchaseLimit() == 0:
            discountProduct.set_purchaseLimitType("noLimit")
        else:
            discountProduct.set_purchaseLimitType("setAmt")

        discountPromoBasicInfo_dict = {}
        db = shelve.open('temporary.db', 'c')
        try:
            if 'discountPromoBasicInfo' in db:
                discountPromoBasicInfo_dict = db["discountPromoBasicInfo"]
            else:
                db["discountPromoBasicInfo"] = discountPromoBasicInfo_dict
        except:
            print("Error occured in shop Temporary dictionary.")
        db.close()
        discount = discountPromo(discountPromoBasicInfo_dict["name"], discountPromoBasicInfo_dict["startingDate"],
                                 discountPromoBasicInfo_dict["endingDate"],
                                 id, discountProduct)
        discount.set_status()


        merchantDiscounts_dict[discount.get_code()] = discount
        discountPromo_dict[session['user']] = merchantDiscounts_dict
        DiscountPromodb['discountPromo'] = discountPromo_dict
        DiscountPromodb.close()

        # test codes

        return redirect(url_for('discountPromotions'))
    return render_template("merchant/create_discountPromo_ending.html", merchant=merchant, chosenProduct=chosenProduct,
                           form=create_discountPromo_form_1)


@app.route('/update_discountPromo_basicInfo/<code>/', methods=['GET', 'POST'])
def update_discountPromo_basicInfo(code):
    db = shelve.open("customer.db", "r")
    m_dict = db["Merchant"]
    merchant = m_dict.get(session['user'])
    db.close()
    warningDate = 0
    warningmessage = ""
    # db["discountPromo"]={email:{discountPromoCode:discountPromoObject}}
    update_discountPromo_basicInfo_form = CreateProductDiscount(request.form)
    if request.method == 'POST' and update_discountPromo_basicInfo_form.validate():
        # maybe i can just add more validation like the name cannot be the same or wtv
        # custom validaiton
        startdate = update_discountPromo_basicInfo_form.startingDate.data
        enddate = update_discountPromo_basicInfo_form.endingDate.data
        if enddate < startdate:
            warningDate = 1
            warningmessage = "End Date cannot be before Start Date."
            return render_template("merchant/update_discountPromo_basicInfo.html", merchant=merchant,
                                   form=update_discountPromo_basicInfo_form,
                                   warningDate=warningDate, warningmessage=warningmessage)

        elif startdate < date.today():
            warningDate = 1
            warningmessage = "Start Date cannot be before today's date."
            return render_template("merchant/update_discountPromo_basicInfo.html", merchant=merchant,
                                   form=update_discountPromo_basicInfo_form,
                                   warningDate=warningDate, warningmessage=warningmessage)

        elif startdate > enddate:
            warningDate = 1
            warningmessage = "Start Date cannot be after End Date."
            return render_template("merchant/update_discountPromo_basicInfo.html", merchant=merchant,
                                   form=update_discountPromo_basicInfo_form,
                                   warningDate=warningDate, warningmessage=warningmessage)

        elif enddate < date.today():
            warningDate = 1
            warningmessage = "End Date cannot be before Today's Date."
            return render_template("merchant/update_discountPromo_basicInfo.html", merchant=merchant,
                                   form=update_discountPromo_basicInfo_form,
                                   warningDate=warningDate, warningmessage=warningmessage)
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
            if session['user'] in discountPromo_dict:
                merchantDiscounts_dict = discountPromo_dict[session['user']]
            else:
                discountPromo_dict[session['user']] = merchantDiscounts_dict
        except:
            print("Error occured in shop discounts dictionary.")

        discount = merchantDiscounts_dict.get(code)
        discount.set_name(update_discountPromo_basicInfo_form.name.data)
        discount.set_startingDate(update_discountPromo_basicInfo_form.startingDate.data)
        discount.set_endingDate(update_discountPromo_basicInfo_form.endingDate.data)

        discount.set_status()

        merchantDiscounts_dict[code] = discount
        discountPromo_dict[session['user']] = merchantDiscounts_dict
        DiscountPromodb['discountPromo'] = discountPromo_dict
        DiscountPromodb.close()

        session["discountCode"] = code

        return redirect(url_for('update_discountPromo_productInfo', ))
    else:
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
            if session['user'] in discountPromo_dict:
                merchantDiscounts_dict = discountPromo_dict[session['user']]
            else:
                discountPromo_dict[session['user']] = merchantDiscounts_dict
        except:
            print("Error occured in shop discounts dictionary.")

        DiscountPromodb.close()

        discount = merchantDiscounts_dict.get(code)
        update_discountPromo_basicInfo_form.name.data = discount.get_name()
        update_discountPromo_basicInfo_form.startingDate.data = discount.get_startingDate()
        update_discountPromo_basicInfo_form.endingDate.data = discount.get_endingDate()

        return render_template("merchant/update_discountPromo_basicInfo.html", merchant=merchant,
                               form=update_discountPromo_basicInfo_form,
                               warningDate=warningDate, warningmessage=warningmessage)


@app.route('/update_discountPromo_productInfo', methods=['GET', 'POST'])
def update_discountPromo_productInfo():
    db = shelve.open("customer.db", "r")
    m_dict = db["Merchant"]
    merchant = m_dict.get(session['user'])
    db.close()
    update_discountPromo_productInfo_form = CreateProductDiscount_1(request.form)
    if request.method == 'POST' and update_discountPromo_productInfo_form.validate():
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
            if session['user'] in discountPromo_dict:
                merchantDiscounts_dict = discountPromo_dict[session['user']]
            else:
                discountPromo_dict[session['user']] = merchantDiscounts_dict
        except:
            print("Error occured in shop discounts dictionary.")

        code = session["discountCode"]

        discount = merchantDiscounts_dict.get(code)
        discountProduct = discount.get_productObject()
        discountProduct.set_discount(update_discountPromo_productInfo_form.discount.data)
        discountProduct.set_purchaseLimit(update_discountPromo_productInfo_form.purchaseLimit.data)
        if discountProduct.get_purchaseLimit() == 0:
            discountProduct.set_purchaseLimitType("noLimit")
        else:
            discountProduct.set_purchaseLimitType("setAmt")

        merchantDiscounts_dict[code] = discount
        discountPromo_dict[session['user']] = merchantDiscounts_dict
        DiscountPromodb['discountPromo'] = discountPromo_dict
        DiscountPromodb.close()

        session.pop("discountCode", None)

        return redirect(url_for('discountPromotions'))
    else:

        db = shelve.open('customer.db', 'r')
        muser_dict = db["Merchant"]
        db.close()
        merchant = muser_dict.get(session['user'])
        products_dict = merchant.get_products()

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
            if session['user'] in discountPromo_dict:
                merchantDiscounts_dict = discountPromo_dict[session['user']]
            else:
                discountPromo_dict[session['user']] = merchantDiscounts_dict
        except:
            print("Error occured in shop discounts dictionary.")
        DiscountPromodb.close()

        code = session["discountCode"]

        discount = merchantDiscounts_dict.get(code)
        discountProduct = discount.get_productObject()
        update_discountPromo_productInfo_form.discount.data = discountProduct.get_discount()
        update_discountPromo_productInfo_form.purchaseLimit.data = discountProduct.get_purchaseLimit()

        productid = discountProduct.get_code()
        chosenProduct = None
        for key in products_dict:
            if key == productid:
                chosenProduct = products_dict[key]

        return render_template("merchant/update_discountPromo_productInfo.html", merchant=merchant,
                               form=update_discountPromo_productInfo_form, chosenProduct=chosenProduct)


@app.route("/deleteDiscountPromo/<code>", methods=['POST'])
def deleteDiscountPromo(code):
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
        if session['user'] in discountPromo_dict:
            merchantDiscounts_dict = discountPromo_dict[session['user']]
        else:
            discountPromo_dict[session['user']] = merchantDiscounts_dict
    except:
        print("Error occured in shop discounts dictionary.")

    merchantDiscounts_dict.pop(code)

    discountPromo_dict[session['user']] = merchantDiscounts_dict
    DiscountPromodb['discountPromo'] = discountPromo_dict
    DiscountPromodb.close()

    return redirect(url_for('discountPromotions'))


@app.route("/individual_product_page/<productID>",methods=['GET', 'POST'])
def show_individual_product(productID):

    chosenProduct = None
    merchantEmail = ""
    #search through the merchant objects to see if the product belongs to them and then pass in the merchant email
    db = shelve.open('customer.db', 'r')
    muser_dict = db["Merchant"]
    # merchant = muser_dict.get()
    db.close()
    for merchant in muser_dict:
        productz_dict = muser_dict[merchant].get_products()
        for id in productz_dict:
            if id == productID:
                merchantEmail = merchant
                chosenProduct = productz_dict[id]
                # print("merchant Email:",merchantEmail)

    #getting products from the same shop
    db = shelve.open('customer.db', 'r')
    muser_dict = db["Merchant"]
    db.close()
    merchant = muser_dict.get(merchantEmail)
    product_dict = merchant.get_products()
    tproduct = len(product_dict)
    prod = product_dict.get(productID)
    review = prod.get_review()
    avg = 0
    divide = len(review)
    rated = 0
    lastreview = "NIL"
    lastrating = "NIL"
    for x in product_dict:
        rated += len(product_dict[x].get_review())
    for i in review:
        avg += int(i.get_rating())
    if divide != 0:
        avg = avg/divide
    if len(review) != 0:
        latest = review[-1]
        lastreview = latest.get_review()
        lastrating = latest.get_rating()
    # print(latest.get_rating())
    avg = int(avg)
    blank = 5-avg
    product_list = []
    for key in product_dict:
        product_list.append(key)
    # print(avg)
    # print(blank)
    merchantproductlist = []
    for product_id in product_dict:
        if productID != product_id:
            merchantproductlist.append(product_dict[product_id])

    #retrieving products of the same category
    sameCat_productList=[]
    for merchantKey in muser_dict:
        if merchantKey != merchantEmail:
            merchant = muser_dict.get(merchantKey)
            products_dict = merchant.get_products()
            for productcode in products_dict:
                if products_dict[productcode].get_product_cat()==chosenProduct.get_product_cat():
                    sameCat_productList.append(products_dict[productcode])

    #getting the other merchant discount Promos
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
        if merchantEmail in discountPromo_dict:
            merchantDiscounts_dict = discountPromo_dict[merchantEmail]
        else:
            discountPromo_dict[merchantEmail] = merchantDiscounts_dict
    except:
        print("Error occured in shop discounts dictionary.")
    DiscountPromodb.close()

    otherProductDP_dict={}#{productID:[discount,discountedPrice]}
    for product in merchantproductlist:
        for count in merchantDiscounts_dict:
            if merchantDiscounts_dict[count].get_productCode() == product.get_product_id():
                discount=merchantDiscounts_dict[count].get_productObject().get_discount()
                discountedPrice=((100-discount)/100)*product.get_product_price()
                otherProductDP_dict[product.get_product_id()]=[discount,discountedPrice]



    #getting the merchant discounts promotions
    discountPromo_dict = {}
    DiscountPromodb = shelve.open('discountPromo.db', 'r')
    try:
        if 'discountPromo' in DiscountPromodb:  # is key exist?
            discountPromo_dict = DiscountPromodb['discountPromo']  # retrieve data
        else:
            DiscountPromodb['discountPromo'] = discountPromo_dict  # start with empty
    except:
        print("Error in retrieving discountPromo from discountPromo.db.")
    merchantDiscounts_dict = {}
    try:
        if merchantEmail in discountPromo_dict:
            merchantDiscounts_dict = discountPromo_dict[merchantEmail]
        else:
            discountPromo_dict[merchantEmail] = merchantDiscounts_dict
    except:
        print("Error occured in shop discounts dictionary.")

    discountPrice=0
    purchaseLimit=0
    for discount in merchantDiscounts_dict:
        merchantDiscountPromo=merchantDiscounts_dict[discount] #discountPromo Object
        if (merchantDiscountPromo.get_productObject()).get_code() == productID:
            if merchantDiscountPromo.get_status() == "Ongoing":
                discountPromo=(merchantDiscountPromo.get_productObject()).get_discount()
                discountPrice=round(chosenProduct.get_product_price()*(100-discountPromo)/100,2)
                if (merchantDiscountPromo.get_productObject()).get_purchaseLimit() != 0:
                    purchaseLimit=(merchantDiscountPromo.get_productObject()).get_purchaseLimit()

    #Getting merchant vouchers
    shopVoucher_dict = {}
    fixeddb = shelve.open('shopVoucherFixedAmt.db', 'c')
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
        if merchantEmail in shopVoucher_dict:
            merchantShopVoucher_dict = shopVoucher_dict[merchantEmail]
        else:
            shopVoucher_dict[merchantEmail] = merchantShopVoucher_dict
    except:
        print("Error occured in shop voucher dictionary.")
    fixeddb.close()

    voucherFixedAmt_list=[]
    for key in merchantShopVoucher_dict:
        voucher=merchantShopVoucher_dict.get(key)
        if voucher.get_status() == "Ongoing" and voucher.get_usageQuantity()>0:
            voucherFixedAmt_list.append(voucher)

    db = shelve.open('shopVouchersPercentage.db', 'c')
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
        if merchantEmail in shopVoucher_dict:
            merchantShopVoucher_dict = shopVoucher_dict[merchantEmail]
        else:
            shopVoucher_dict[merchantEmail] = merchantShopVoucher_dict
    except:
        print("Error occured in shop voucher dictionary.")

    voucherPercentage_list=[]
    for key in merchantShopVoucher_dict:
        voucher = merchantShopVoucher_dict.get(key)
        if voucher.get_status() == "Ongoing" and voucher.get_usageQuantity()>0:
            voucherPercentage_list.append(voucher)
    db.close()

    userShoppingCart=None
    inFavourites=False
    inShoppingCart=False
    loggedIn=False

    #checking if user is logged in
    try:
        userEmail=session['user']
    except:
        userEmail = None

    noOfItems=0 #for the nav bar
    productList=[]
    totalPrice=0
    if userEmail != None:
        loggedIn=True

        shoppingCarts = {}
        shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
        try:
            if "shoppingCart" in shoppingCartDB:  # is key exist?
                shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
            else:
                shoppingCartDB["shoppingCart"] = shoppingCarts  # start with empty
        except:
            print("Error in retrieving shopVouchers from vouchers.db.")

        userShoppingCart = ShoppingCart(session['user'])  # retrieves the shopping cart object
        try:
            if session['user'] in shoppingCarts:
                userShoppingCart = shoppingCarts[session['user']]
            else:
                shoppingCarts[session['user']] = userShoppingCart
        except:
            print("Error occured in dictionary.")
        shoppingCartDB.close()

        inShoppingCartQuantity=0
        inShoppingCart=False
        merchant_dict=userShoppingCart.get_merchants()
        for merchEmail in merchant_dict:
            product_list=merchant_dict[merchEmail].get_products()
            for sortbyproductObject in product_list:
                if sortbyproductObject.get_productID() == productID:
                    inShoppingCart=True
                    db = shelve.open('temporary.db', 'c')
                    inShoppingCartQuantity = db["individualProductQuantity"]
                    db.close()
                    break
                if inShoppingCart ==True:
                    break

        #checking in favourites
        favourites_dict={}
        favouritesDB=shelve.open('purchaseHistory.db', 'c')
        try:
            if "favourites" in favouritesDB:  # is key exist?
                favourites_dict = favouritesDB["favourites"]  # retrieve data
            else:
                favouritesDB["favourites"]=favourites_dict # start with empty
        except:
            print("Error in retrieving Shopping cart from shoppingcartDB.db.")

        userFavourites = Favourite()
        try:
            if session['user'] in favourites_dict:
                userFavourites = favourites_dict[session['user']]
            else:
                favourites_dict[session['user']] = userFavourites
        except:
            print("Error occured in dictionary.")
        favouritesDB.close()

        inFavourites = False
        for item in userFavourites.get_favouritedItems():
            if item.get_productID() == productID:
                inFavourites=True
                break

        shoppingCarts = {}
        shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
        try:
            if "shoppingCart" in shoppingCartDB:  # is key exist?
                shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
            else:
                print("Shopping carts has an error.")  # start with empty
        except:
            print("Error in retrieving shopVouchers from vouchers.db.")

        userShoppingCart = None  # retrieves the shopping cart object
        try:
            if session['user'] in shoppingCarts:
                userShoppingCart = shoppingCarts[session['user']]
            else:
                print("Can't retrieve the user's shopping cart.")
        except:
            print("Error occured in dictionary.")
        shoppingCartDB.close()

        #for the navbar

        productList=[]
        totalPrice=0
        if userShoppingCart != None:
            merchant_dict=userShoppingCart.get_merchants()
            for merchantEmail in merchant_dict:
                merchantObject=merchant_dict[merchantEmail]
                product_list=merchantObject.get_products()
                for product in product_list:
                    productList.append(product)
                    noOfItems+=1
                    totalPrice+=round(product.get_totalPrice(),2)

    warning=0
    quantity_form = GetQuantity(request.form)
    if request.method == 'POST' and quantity_form.validate():
        quantity = quantity_form.quantity.data

        if purchaseLimit != 0:
            if quantity > int(purchaseLimit):
                warning = 1
                return render_template("common/individual_product_page.html", avg=avg, lastreview=lastreview, lastrating=lastrating, blank=blank, rated=rated, divide=divide, tproduct=tproduct, merchant=merchant, chosenProduct=chosenProduct,
                                       merchantEmail=merchantEmail,
                                       discountPrice=discountPrice, purchaseLimit=purchaseLimit,
                                       voucherFixedAmt_list=voucherFixedAmt_list,
                                       voucherPercentage_list=voucherPercentage_list, productID=productID,
                                       quantity_form=quantity_form,
                                       inShoppingCart=inShoppingCart, inFavourites=inFavourites,
                                       merchantProductList=merchantproductlist,
                                       otherProductDP_dict=otherProductDP_dict,
                                       warning=warning,loggedIn=loggedIn,noOfItems=noOfItems,
                                       productList=productList,totalPrice=totalPrice,sameCat_productList=sameCat_productList)

        if quantity > chosenProduct.get_quantity():
            warning = 2
            return render_template("common/individual_product_page.html", avg=avg, lastreview=lastreview,
                                   lastrating=lastrating, blank=blank, rated=rated, divide=divide, tproduct=tproduct,
                                   merchant=merchant, chosenProduct=chosenProduct,
                                   merchantEmail=merchantEmail,
                                   discountPrice=discountPrice, purchaseLimit=purchaseLimit,
                                   voucherFixedAmt_list=voucherFixedAmt_list,
                                   voucherPercentage_list=voucherPercentage_list, productID=productID,
                                   quantity_form=quantity_form,
                                   inShoppingCart=inShoppingCart, inFavourites=inFavourites,
                                   merchantProductList=merchantproductlist,
                                   otherProductDP_dict=otherProductDP_dict,
                                   warning=warning, loggedIn=loggedIn, noOfItems=noOfItems,
                                   productList=productList, totalPrice=totalPrice,
                                   sameCat_productList=sameCat_productList)

        db = shelve.open('temporary.db', 'c')
        db["individualProductQuantity"] = quantity
        db.close()

        if loggedIn==True:
            if inShoppingCart == False:
                return redirect(url_for('addingToCart', productID=productID,merchantEmail=merchantEmail,discountedPrice=discountPrice))
            else:
                return redirect(url_for('updateQuantity', productID=productID,merchantEmail=merchantEmail))
        else:
            return redirect(url_for('login'))

    return render_template("common/individual_product_page.html", avg=avg, blank=blank, lastreview=lastreview, lastrating=lastrating, divide=divide, rated=rated, tproduct=tproduct, merchant=merchant, chosenProduct=chosenProduct,merchantEmail=merchantEmail,
                           discountPrice=discountPrice, purchaseLimit=purchaseLimit, voucherFixedAmt_list=voucherFixedAmt_list,
                           voucherPercentage_list=voucherPercentage_list, productID=productID, quantity_form=quantity_form,
                           inShoppingCart=inShoppingCart, inFavourites=inFavourites, merchantProductList=merchantproductlist,
                           otherProductDP_dict=otherProductDP_dict, warning=warning, loggedIn=loggedIn, noOfItems=noOfItems,
                           productList=productList, totalPrice=totalPrice,sameCat_productList=sameCat_productList)


@app.route("/display_comment/<email>/<productID>")
def display_comment(email, productID):
    db = shelve.open("customer.db", "r")
    merchant_dict = db["Merchant"]
    merchant = merchant_dict.get(email)
    product_list = merchant.get_products()
    product = product_list.get(productID)
    print(product)
    review = product.get_review()
    rated = len(review)
    return render_template("common/product_review.html", productID=productID, merchant=merchant, review=review,
                           product=product, rated=rated)


@app.route("/addtoCart/<productID>/<merchantEmail>/<discountedPrice>", methods=['GET', 'POST'])
def addingToCart(productID, merchantEmail, discountedPrice):
    # storing it as shoppingCartDB.db["shoppingCarts"]={userEmail:userShoppingCart object}
    shoppingCarts = {}
    shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
    try:
        if "shoppingCart" in shoppingCartDB:  # is key exist?
            shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
        else:
            shoppingCartDB["shoppingCart"] = shoppingCarts  # start with empty
    except:
        print("Error in retrieving shopVouchers from vouchers.db.")

    userShoppingCart = ShoppingCart(session['user'])  # retrieves the shopping cart object
    try:
        if session['user'] in shoppingCarts:
            userShoppingCart = shoppingCarts[session['user']]
        else:
            shoppingCarts[session['user']] = userShoppingCart
    except:
        print("Error occured in dictionary.")

    # getting quantity
    quantity = 0
    db = shelve.open('temporary.db', 'r')
    try:
        if 'individualProductQuantity' in db:
            quantity = db["individualProductQuantity"]
        else:
            print("Error")
    except:
        print("Error occured in shop Temporary dictionary.")
    db.close()

    chosenProduct = None
    # getting the merchant Email and chosen Product object
    db = shelve.open('customer.db', 'r')
    muser_dict = db["Merchant"]
    db.close()
    for merchant in muser_dict:
        products_dict = muser_dict[merchant].get_products()
        for id in products_dict:
            if id == productID:
                merchantEmail = merchant
                chosenProduct = products_dict[id]
                print(chosenProduct.get_product_name())

    # creating SortByProduct object
    product = SortByProduct(productID, quantity, float(chosenProduct.get_product_price()), float(discountedPrice))
    product.set_totalPrice()

    # Getting merchant vouchers
    count = 0
    vouchers_dict = {}
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
        if merchantEmail in shopVoucher_dict:
            merchantShopVoucher_dict = shopVoucher_dict[merchantEmail]
        else:
            shopVoucher_dict[merchantEmail] = merchantShopVoucher_dict
    except:
        print("Error occured in shop voucher dictionary.")
    fixeddb.close()

    for key in merchantShopVoucher_dict:
        voucher = merchantShopVoucher_dict.get(key)
        if voucher.get_status() == "Ongoing":
            count += 1
            vouchers_dict[count] = voucher

    db = shelve.open('shopVouchersPercentage.db', 'c')
    shopVoucher_dict = {}
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
        if merchantEmail in shopVoucher_dict:
            merchantShopVoucher_dict = shopVoucher_dict[merchantEmail]
        else:
            shopVoucher_dict[merchantEmail] = merchantShopVoucher_dict
    except:
        print("Error occured in shop voucher dictionary.")
    db.close()
    for key in merchantShopVoucher_dict:
        voucher = merchantShopVoucher_dict.get(key)
        if voucher.get_status() == "Ongoing":
            count += 1
            vouchers_dict[count] = voucher

    # getting merchant Name
    db = shelve.open("customer.db", "c")
    muser_dict = db["Merchant"]
    merchantName = muser_dict.get(merchantEmail).get_first_name() + " " + muser_dict.get(
        merchantEmail).get_last_name()
    db.close()

    # doing the SortByMerchant Class
    merchants_dict = userShoppingCart.get_merchants()
    print(merchants_dict)
    userChosenMerchant = None
    if merchants_dict == {}:
        userChosenMerchant = SortByMerchant(merchantEmail, vouchers_dict, merchantName)
        userChosenMerchant.add_product(product)
        userChosenMerchant.calculate_totalPrice()
        userChosenMerchant.set_savings_for_products()
        print("total Price for userChosenMerchant:", userChosenMerchant.get_totalPrice())
    new = True
    for key in merchants_dict:
        if key == merchantEmail:
            new = False
            userChosenMerchant = merchants_dict[key]
            userChosenMerchant.add_product(product)
            userChosenMerchant.calculate_totalPrice()
            userChosenMerchant.set_savings_for_products()
            print("total Price for userChosenMerchant:", userChosenMerchant.get_totalPrice())
    if new:
        userChosenMerchant = SortByMerchant(merchantEmail, vouchers_dict, merchantName)
        userChosenMerchant.add_product(product)
        userChosenMerchant.calculate_totalPrice()
        userChosenMerchant.set_savings_for_products()
        print("total Price for userChosenMerchant:", userChosenMerchant.get_totalPrice())

    # Doing the User shopping cart object
    userShoppingCart.add_merchant(merchantEmail, userChosenMerchant)
    print("shopping cart dict for merchants:", userShoppingCart.get_merchants())
    userShoppingCart.calculate_totalPrice()
    print("shopping cart total price:", userShoppingCart.get_totalPrice())
    userShoppingCart.calculate_savings()

    shoppingCarts[session['user']] = userShoppingCart
    print(shoppingCarts[session['user']])
    shoppingCartDB["shoppingCart"] = shoppingCarts
    shoppingCartDB.close()

    return redirect(url_for('show_individual_product', productID=productID))


# updating the quantity
@app.route("/updateQuantity/<productID>/<merchantEmail>", methods=['GET', 'POST'])
def updateQuantity(productID, merchantEmail):
    shoppingCarts = {}
    shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
    try:
        if "shoppingCart" in shoppingCartDB:  # is key exist?
            shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
        else:
            shoppingCartDB["shoppingCart"] = shoppingCarts  # start with empty
    except:
        print("Error in retrieving shopVouchers from vouchers.db.")

    userShoppingCart = ShoppingCart(session['user'])  # retrieves the shopping cart object
    try:
        if session['user'] in shoppingCarts:
            userShoppingCart = shoppingCarts[session['user']]
        else:
            shoppingCarts[session['user']] = userShoppingCart
    except:
        print("Error occured in dictionary.")

    merchant_dict = userShoppingCart.get_merchants()
    sortbymerchantObject = None
    for merchEmail in merchant_dict:
        if merchEmail == merchantEmail:
            sortbymerchantObject = merchant_dict[merchEmail]

    # getting quantity
    quantity = 0
    db = shelve.open('temporary.db', 'r')
    try:
        if 'individualProductQuantity' in db:
            quantity = db["individualProductQuantity"]
        else:
            print("Error")
    except:
        print("Error occured in shop Temporary dictionary.")
    db.close()

    product_list = []
    product_list = sortbymerchantObject.get_products()
    for sortbyproductObject in product_list:
        if sortbyproductObject.get_productID() == productID:
            sortbyproductObject.set_quantity(quantity)
            sortbyproductObject.set_totalPrice()
            break

    merchant_dict[merchantEmail].set_productList(product_list)

    userShoppingCart.set_merchants(merchant_dict)
    userShoppingCart.calculate_totalPrice()
    userShoppingCart.calculate_savings()

    shoppingCarts[session['user']] = userShoppingCart
    shoppingCartDB["shoppingCart"] = shoppingCarts
    shoppingCartDB.close()

    return redirect(url_for('shopping_cart'))


@app.route("/shopping_cart")
# [shoppingCart]={"UserEmail":shoppingCartObject}
def shopping_cart():
    # checking if user is logged in

    if session['user'] is None:
        return redirect(url_for("login", id=2))

    try:
        userEmail = session['user']
    except:
        userEmail = None

    userShoppingCart = None
    merchantObject_list = []
    merchantProductdict = []

    if userEmail != None:
        shoppingCarts = {}
        shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
        try:
            if "shoppingCart" in shoppingCartDB:  # is key exist?
                shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
            else:
                print("Shopping carts has an error.")  # start with empty
        except:
            print("Error in retrieving shopVouchers from vouchers.db.")

        userShoppingCart = None  # retrieves the shopping cart object
        try:
            if session['user'] in shoppingCarts:
                userShoppingCart = shoppingCarts[session['user']]
            else:
                print("Can't retrieve the user's shopping cart.")
        except:
            print("Error occured in dictionary.")

        merchant_dict = {}
        merchantObject_list = []  # list of SortByMerchant Objects
        merchantProductdict = {}  # {merchantEmail:productList}
        productsList = []  # [productObject]
        print("userShoppingCart:", userShoppingCart)
        if userShoppingCart != None:
            merchant_dict = userShoppingCart.get_merchants()
            for merchantObject in merchant_dict:
                userchoseMerchant = merchant_dict.get(merchantObject)  # getting sortbymerchant object
                merchantObject_list.append(userchoseMerchant)
                productsList = userchoseMerchant.get_products()
                merchantProductdict[userchoseMerchant.get_merchantEmail()] = productsList

    # getting user object
    db = shelve.open("customer.db", "r")
    customer_dict = db["Customer"]
    customer = customer_dict.get(session['user'])

    return render_template("common/shopping_cart.html", userShoppingCart=userShoppingCart,
                           merchantProductdict=merchantProductdict,
                           merchantObject_list=merchantObject_list, userEmail=userEmail, customer=customer)


# deleting of product
@app.route("/deleteFromCart/<productID>/<merchantEmail>", methods=['GET', 'POST'])
def deleteFromCart(productID, merchantEmail):
    shoppingCarts = {}
    shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
    try:
        if "shoppingCart" in shoppingCartDB:  # is key exist?
            shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
        else:
            print("Shopping carts has an error.")  # start with empty
    except:
        print("Error in retrieving shopVouchers from vouchers.db.")

    userShoppingCart = None  # retrieves the shopping cart object
    try:
        if session['user'] in shoppingCarts:
            userShoppingCart = shoppingCarts[session['user']]
        else:
            print("Can't retrieve the user's shopping cart.")
    except:
        print("Error occured in dictionary.")

    print("Email", merchantEmail)
    merchantObject = None
    merchants_dict = userShoppingCart.get_merchants()
    print(merchants_dict)
    for key in merchants_dict:
        if key == merchantEmail:
            merchantObject = merchants_dict[key]
            break
    print("merchantObject", merchantObject)

    merchantObject.delete_product(productID)
    if merchantObject.get_products() == []:
        userShoppingCart.delete_merchant(merchantObject.get_merchantEmail())
    else:
        userShoppingCart.add_merchant(merchantEmail, merchantObject)  # updating

    shoppingCarts[session['user']] = userShoppingCart
    shoppingCartDB["shoppingCart"] = shoppingCarts
    shoppingCartDB.close()

    return redirect(url_for('shopping_cart'))


@app.route("/processingQuantity", methods=['POST'])
def getting_quantities():
    quantityInfo = request.get_json(force=True)
    print("quantityInfo:", quantityInfo)

    quantitylist = []
    for item in quantityInfo:
        quantitylist.append(int(item))
    print("in the processing", quantitylist)

    return redirect(url_for('checkout'))


@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    shoppingCarts = {}
    shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
    try:
        if "shoppingCart" in shoppingCartDB:  # is key exist?
            shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
        else:
            print("Shopping carts has an error.")  # start with empty
    except:
        print("Error in retrieving shopVouchers from vouchers.db.")

    userShoppingCart = None  # retrieves the shopping cart object
    try:
        if session['user'] in shoppingCarts:
            userShoppingCart = shoppingCarts[session['user']]
        else:
            print("Can't retrieve the user's shopping cart.")
    except:
        print("Error occured in dictionary.")

    merchant_dict={}
    merchantVouchers_dict_sc={}
    if userShoppingCart != None:
        merchant_dict = userShoppingCart.get_merchants()  # {merchantEmail:sortbymerchant object}

        # Getting merchant vouchers
        for merchantEmail in merchant_dict:

            count = 0
            merchantVouchers_dict_sc = {}  # {merchantEmail:vouchers_dict}
            vouchers_dict = {}
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
                if merchantEmail in shopVoucher_dict:
                    merchantShopVoucher_dict = shopVoucher_dict[merchantEmail]
                else:
                    shopVoucher_dict[merchantEmail] = merchantShopVoucher_dict
            except:
                print("Error occured in shop voucher dictionary.")
            fixeddb.close()

            for key in merchantShopVoucher_dict:
                voucher = merchantShopVoucher_dict.get(key)
                if voucher.get_status() == "Ongoing" and merchant_dict[
                    merchantEmail].get_totalPrice() >= voucher.get_minSpend() and voucher.get_usageQuantity() > 0:
                    count += 1
                    vouchers_dict[count] = voucher

            db = shelve.open('shopVouchersPercentage.db', 'c')
            shopVoucher_dict = {}
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
                if merchantEmail in shopVoucher_dict:
                    merchantShopVoucher_dict = shopVoucher_dict[merchantEmail]
                else:
                    shopVoucher_dict[merchantEmail] = merchantShopVoucher_dict
            except:
                print("Error occured in shop voucher dictionary.")
            db.close()
            for key in merchantShopVoucher_dict:
                voucher = merchantShopVoucher_dict.get(key)
                if voucher.get_status() == "Ongoing" and merchant_dict[
                    merchantEmail].get_totalPrice() >= voucher.get_minSpend() and voucher.get_usageQuantity() > 0:
                    count += 1
                    vouchers_dict[count] = voucher

            print(vouchers_dict)
            merchant_dict[merchantEmail].set_availableVouchers(vouchers_dict)
            merchantVouchers_dict_sc[merchantEmail] = vouchers_dict

        userShoppingCart.set_merchants(merchant_dict)

        chosenwebvoucher = None
        if userShoppingCart.get_chosenWebsiteVoucher() != None:
            chosenwebvoucher = userShoppingCart.get_chosenWebsiteVoucher()
            print("chosenwebvoucher:", chosenwebvoucher)
            userShoppingCart.delete_website_voucher(chosenwebvoucher)

        chosenwebreward = None
        if userShoppingCart.get_chosenWebsiteReward() != None:
            chosenwebreward = userShoppingCart.get_chosenWebsiteReward()
            print("chosenwebreward:", chosenwebreward)
            userShoppingCart.delete_web_reward(chosenwebreward)

        userShoppingCart.calculate_totalPrice()
        userShoppingCart.calculate_savings()

        if chosenwebvoucher != None:
            userShoppingCart.set_website_voucher(chosenwebvoucher)

        if chosenwebreward != None:
            userShoppingCart.set_web_reward(chosenwebreward)

        shoppingCarts[session['user']] = userShoppingCart
        shoppingCartDB["shoppingCart"] = shoppingCarts
        shoppingCartDB.close()

    # getting user object
    db = shelve.open("customer.db", "r")
    customer_dict = db["Customer"]
    customer = customer_dict.get(session['user'])

    return render_template("common/checkout.html", merchant_dict=merchant_dict,
                           merchantVouchers_dict_sc=merchantVouchers_dict_sc,
                           userShoppingCart=userShoppingCart, customer=customer)


# still need to do for the merchant voucher
@app.route("/showingShopVoucher/<merchantEmail>", methods=['GET', 'POST'])
def showingShopVoucher(merchantEmail):
    shoppingCarts = {}
    shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
    try:
        if "shoppingCart" in shoppingCartDB:  # is key exist?
            shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
        else:
            print("Shopping carts has an error.")  # start with empty
    except:
        print("Error in retrieving shopVouchers from vouchers.db.")

    userShoppingCart = None  # retrieves the shopping cart object
    try:
        if session['user'] in shoppingCarts:
            userShoppingCart = shoppingCarts[session['user']]
        else:
            print("Can't retrieve the user's shopping cart.")
    except:
        print("Error occured in dictionary.")

    merchant_dict = userShoppingCart.get_merchants()
    merchantObject = merchant_dict[merchantEmail]
    vouchers_dict = merchantObject.get_availableVouchers()  # {count:voucherObject}

    # getting user object
    db = shelve.open("customer.db", "r")
    customer_dict = db["Customer"]
    customer = customer_dict.get(session['user'])
    m_dict = db["Merchant"]
    merchant = m_dict.get(merchantEmail)
    db.close()

    return render_template("common/showingMerchantVouchers.html", customer=customer, merchant=merchant,
                           vouchers_dict=vouchers_dict, merchantEmail=merchantEmail)


@app.route("/choosingShopVoucher/<merchantEmail>/<int:count>", methods=['GET', 'POST'])
def choosingShopVoucher(merchantEmail, count):
    shoppingCarts = {}
    shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
    try:
        if "shoppingCart" in shoppingCartDB:  # is key exist?
            shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
        else:
            print("Shopping carts has an error.")  # start with empty
    except:
        print("Error in retrieving shopVouchers from vouchers.db.")

    userShoppingCart = None  # retrieves the shopping cart object
    try:
        if session['user'] in shoppingCarts:
            userShoppingCart = shoppingCarts[session['user']]
        else:
            print("Can't retrieve the user's shopping cart.")
    except:
        print("Error occured in dictionary.")

    merchant_dict = userShoppingCart.get_merchants()
    merchantObject = merchant_dict[merchantEmail]
    merchantObject.set_usedVoucher(count)
    print("savings for each merchant:", merchantObject.get_savings())

    merchant_dict[merchantEmail] = merchantObject
    userShoppingCart.set_merchants(merchant_dict)
    userShoppingCart.calculate_totalPrice()
    userShoppingCart.calculate_savings()

    shoppingCarts[session['user']] = userShoppingCart
    shoppingCartDB["shoppingCart"] = shoppingCarts
    shoppingCartDB.close()

    return redirect(url_for('checkout'))


# still need to do for website voucher

@app.route("/gettingCampaignVoucher/<voucherid>", methods=['GET', 'POST'])
def gettingCampaignVoucher(voucherid):
    # cvd_dict[Campaign_voucher_percent.get_voucher_id()] = Campaign_voucher_percent
    cvd_dict = {}
    db = shelve.open('CampaignVchers.db', 'c')
    try:
        if 'CampaignVchers' in db:
            cvd_dict = db['CampaignVchers']
        else:
            db['CampaignVchers'] = cvd_dict
    except:
        db["CampaignVouchers"] = {}

    db.close()
    print("cvd_dict:", cvd_dict)

    shoppingCarts = {}
    shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
    try:
        if "shoppingCart" in shoppingCartDB:  # is key exist?
            shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
        else:
            print("Shopping carts has an error.")  # start with empty
    except:
        print("Error in retrieving shopVouchers from vouchers.db.")

    userShoppingCart = None  # retrieves the shopping cart object
    try:
        if session['user'] in shoppingCarts:
            userShoppingCart = shoppingCarts[session['user']]
        else:
            print("Can't retrieve the user's shopping cart.")
    except:
        print("Error occured in dictionary.")

    chosenWebsiteVoucher = None
    print(voucherid)
    for id in cvd_dict:
        if id == voucherid:
            chosenWebsiteVoucher = cvd_dict[id]

    print(chosenWebsiteVoucher)
    if userShoppingCart != None:
        if chosenWebsiteVoucher != None:
            userShoppingCart.set_website_voucher(chosenWebsiteVoucher)
        else:
            print("chosenWebsiteVoucher is None.", chosenWebsiteVoucher)

        shoppingCarts[session['user']] = userShoppingCart
        shoppingCartDB["shoppingCart"] = shoppingCarts

        shoppingCartDB.close()

    return redirect(url_for('checkout'))


@app.route("/changingCampaignVoucher/<voucherid>", methods=['GET', 'POST'])
def changingCampaignVoucher(voucherid):
    cvd_dict = {}
    db = shelve.open('CampaignVchers.db', 'c')
    try:
        if 'CampaignVchers' in db:
            cvd_dict = db['CampaignVchers']
        else:
            db['CampaignVchers'] = cvd_dict
    except:
        db["CampaignVouchers"] = {}

    db.close()
    print("cvd_dict:", cvd_dict)

    shoppingCarts = {}
    shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
    try:
        if "shoppingCart" in shoppingCartDB:  # is key exist?
            shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
        else:
            print("Shopping carts has an error.")  # start with empty
    except:
        print("Error in retrieving shopVouchers from vouchers.db.")

    userShoppingCart = None  # retrieves the shopping cart object
    try:
        if session['user'] in shoppingCarts:
            userShoppingCart = shoppingCarts[session['user']]
        else:
            print("Can't retrieve the user's shopping cart.")
    except:
        pass
        print("Error occured in dictionary.")

    chosenWebsiteVoucher = None
    print(voucherid)
    for id in cvd_dict:
        if id == voucherid:
            chosenWebsiteVoucher = cvd_dict[id]

    if chosenWebsiteVoucher == None:
        print("chosenWebsiteVoucher is None.", chosenWebsiteVoucher)
    else:
        previousVoucher = userShoppingCart.get_chosenWebsiteVoucher()
        userShoppingCart.delete_website_voucher(previousVoucher)
        userShoppingCart.set_website_voucher(chosenWebsiteVoucher)

    shoppingCarts[session['user']] = userShoppingCart
    shoppingCartDB["shoppingCart"] = shoppingCarts

    shoppingCartDB.close()

    return redirect(url_for('checkout'))


# still need to do for website reward
@app.route("/gettingWebsiteReward/<rewardID>", methods=['GET', 'POST'])
def gettingWebsiteReward(rewardID):
    CWR_dict = {}
    db = shelve.open('WebReward.db', 'c')

    try:
        if 'WebRewards' in db:
            CWR_dict = db['WebRewards']
        else:
            db['WebRewards'] = CWR_dict
    except:
        print("Error")
    db.close()

    shoppingCarts = {}
    shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
    try:
        if "shoppingCart" in shoppingCartDB:  # is key exist?
            shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
        else:
            print("Shopping carts has an error.")  # start with empty
    except:
        print("Error in retrieving shopVouchers from vouchers.db.")

    userShoppingCart = None  # retrieves the shopping cart object
    try:
        if session['user'] in shoppingCarts:
            userShoppingCart = shoppingCarts[session['user']]
        else:
            print("Can't retrieve the user's shopping cart.")
    except:
        print("Error occured in dictionary.")

    chosenWebReward = None
    for id in CWR_dict:
        if id == rewardID:
            chosenWebReward = CWR_dict[id]

    if chosenWebReward != None:
        userShoppingCart.set_web_reward(chosenWebReward)
    else:
        print("Chosen web reward = None", chosenWebReward)

    shoppingCarts[session['user']] = userShoppingCart
    shoppingCartDB["shoppingCart"] = shoppingCarts

    shoppingCartDB.close()

    return redirect(url_for('checkout'))


@app.route("/changingWebsiteReward/<rewardID>", methods=['GET', 'POST'])
def changingWebsiteReward(rewardID):
    CWR_dict = {}
    db = shelve.open('WebReward.db', 'c')

    try:
        if 'WebRewards' in db:
            CWR_dict = db['WebRewards']
        else:
            db['WebRewards'] = CWR_dict
    except:
        print("Error")
    db.close()

    shoppingCarts = {}
    shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
    try:
        if "shoppingCart" in shoppingCartDB:  # is key exist?
            shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
        else:
            print("Shopping carts has an error.")  # start with empty
    except:
        print("Error in retrieving shopVouchers from vouchers.db.")

    userShoppingCart = None  # retrieves the shopping cart object
    try:
        if session['user'] in shoppingCarts:
            userShoppingCart = shoppingCarts[session['user']]
        else:
            print("Can't retrieve the user's shopping cart.")
    except:
        print("Error occured in dictionary.")

    chosenWebReward = None
    for id in CWR_dict:
        if id == rewardID:
            chosenWebReward = CWR_dict[id]

    if chosenWebReward != None:
        previousReward = userShoppingCart.get_chosenWebsiteReward()
        userShoppingCart.delete_web_reward(previousReward)
        userShoppingCart.set_web_reward(chosenWebReward)
    else:
        print("Chosen web reward = None", chosenWebReward)

    shoppingCarts[session['user']] = userShoppingCart
    shoppingCartDB["shoppingCart"] = shoppingCarts

    shoppingCartDB.close()

    return redirect(url_for('checkout'))


@app.route("/payment", methods=['GET', 'POST'])
def payment():
    # retriving shopping cart
    shoppingCarts = {}
    shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
    try:
        if "shoppingCart" in shoppingCartDB:  # is key exist?
            shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
        else:
            print("Shopping carts has an error.")  # start with empty
    except:
        print("Error in retrieving Shopping cart from shoppingcartDB.db.")

    userShoppingCart = ShoppingCart(session['user'])  # retrieves the shopping cart object
    try:
        if session['user'] in shoppingCarts:
            userShoppingCart = shoppingCarts[session['user']]
        else:
            print("Can't retrieve the user's shopping cart.")
    except:
        print("Error occured in dictionary.")
    shoppingCartDB.close()

    # retrieving the customer delivery address
    db = shelve.open("customer.db", 'c')
    customers_dict = db["Customer"]
    customerObject = customers_dict[session['user']]
    db.close()

    address = customerObject.get_address()
    zipcode = customerObject.get_zipcode()
    city = customerObject.get_city()

    # retrieving the customer credit card info
    card = None
    credit_card = customerObject.get_credit_card()
    for x in range(len(credit_card)):
        if credit_card[x].get_default() == 1:
            card = credit_card[x].get_credit_card()
    delivery_address = deliveryAddress(address, zipcode, city)
    paymentDetail = PaymentInfo(userShoppingCart, delivery_address, credit_card)

    db = shelve.open('temporary.db', 'c')
    db["paymentDetail"] = paymentDetail
    db.close()

    # getting user object
    db = shelve.open("customer.db", "r")
    customer_dict = db["Customer"]
    customer = customer_dict.get(session['user'])

    return render_template("common/payment.html", address=address, zipcode=zipcode, city=city, card=card,
                           paymentDetail=paymentDetail, customer=customer)


@app.route("/payment2", methods=['GET', 'POST'])
def payment2():
    # retriving shopping cart
    shoppingCarts = {}
    shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
    try:
        if "shoppingCart" in shoppingCartDB:  # is key exist?
            shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
        else:
            print("Shopping carts has an error.")  # start with empty
    except:
        print("Error in retrieving Shopping cart from shoppingcartDB.db.")

    userShoppingCart = None  # retrieves the shopping cart object
    try:
        if session['user'] in shoppingCarts:
            userShoppingCart = shoppingCarts[session['user']]
        else:
            print("Can't retrieve the user's shopping cart.")
    except:
        print("Error occured in dictionary.")
    shoppingCartDB.close()

    # retrieving the customer delivery address
    db = shelve.open("customer.db", 'c')
    customers_dict = db["Customer"]
    customerObject = customers_dict[session['user']]
    db.close()

    address = customerObject.get_address()
    zipcode = customerObject.get_zipcode()
    city = customerObject.get_city()

    # retrieving the customer credit card info
    card = None
    credit_card = customerObject.get_credit_card()
    for x in range(len(credit_card)):
        if credit_card[x].get_default() == 1:
            card = credit_card[x].get_credit_card()

    delivery_address = deliveryAddress(address, zipcode, city)
    paymentDetail = PaymentInfo(userShoppingCart, delivery_address, credit_card)
    paymentDetail.set_shippingOption("ES")

    db = shelve.open('temporary.db', 'c')
    db["paymentDetail"] = paymentDetail
    db.close()

    # getting user object
    db = shelve.open("customer.db", "r")
    customer_dict = db["Customer"]
    customer = customer_dict.get(session['user'])

    return render_template("common/payment2.html", address=address, zipcode=zipcode, city=city, card=card,
                           paymentDetail=paymentDetail, customer=customer)


@app.route("/placeOrder", methods=['GET', 'POST'])
def placeOrder():
    # retriving shopping cart
    shoppingCarts = {}
    shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
    try:
        if "shoppingCart" in shoppingCartDB:  # is key exist?
            shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
        else:
            print("Shopping carts has an error.")  # start with empty
    except:
        print("Error in retrieving Shopping cart from shoppingcartDB.db.")

    userShoppingCart = None  # retrieves the shopping cart object
    try:
        if session['user'] in shoppingCarts:
            userShoppingCart = shoppingCarts[session['user']]
        else:
            print("Can't retrieve the user's shopping cart.")
    except:
        print("Error occured in dictionary.")

    purchaseHistory_dict = {}
    purchaseHistoryDB = shelve.open('purchaseHistory.db', 'c')
    try:
        if "purchaseHistory" in purchaseHistoryDB:  # is key exist?
            purchaseHistory_dict = purchaseHistoryDB["purchaseHistory"]  # retrieve data
        else:
            purchaseHistoryDB["purchaseHistory"] = purchaseHistory_dict  # start with empty
    except:
        print("Error in retrieving Shopping cart from shoppingcartDB.db.")

    userPurchaseHist = WholePurchaseHistory()
    try:
        if session['user'] in purchaseHistory_dict:
            userPurchaseHist = purchaseHistory_dict[session['user']]
        else:
            purchaseHistory_dict[session['user']] = userPurchaseHist
    except:
        print("Error occured in dictionary.")

    # retrievin the purchaseDetails
    paymentDetail = None
    Tempdb = shelve.open('temporary.db', 'c')
    try:
        if "paymentDetail" in Tempdb:  # is key exist?
            paymentDetail = Tempdb["paymentDetail"]  # retrieve data
        else:
            print("Unable to retrieve from the temporary db")
    except:
        print("Error in retrieving Shopping cart from shoppingcartDB.db.")
    Tempdb.close()
    # print("payment detail:", paymentDetail)

    currentPurchaseHist = PurchaseHistory(userShoppingCart, session['user'], paymentDetail)
    admin_order = {}
    try:
        db = shelve.open("customer.db", "c")
        admin_order = db["Orders"]
    except:
        db = shelve.open("customer.db", "c")
        db["Orders"] = admin_order


    admin_order[str(uuid4())] = currentPurchaseHist
    db["Orders"] = admin_order

    db.close()
    userPurchaseHist.add_purchaseHistory(currentPurchaseHist)
    purchaseHistory_dict[session['user']] = userPurchaseHist
    purchaseHistoryDB["purchaseHistory"] = purchaseHistory_dict
    purchaseHistoryDB.close()

    merchant_dict=userShoppingCart.get_merchants()
    for merchantEmail in merchant_dict:
        usedVoucher=merchant_dict[merchantEmail].get_usedVoucher()
        if usedVoucher != None:
            if usedVoucher.get_discountType() == "fixedAmt":
                shopVoucher_dict = {}
                db = shelve.open('shopVoucherFixedAmt.db', 'c')
                # shopVoucher_dict={merchant email:{shop voucher code: shop voucher object}}
                try:
                    if 'shopVouchers' in db:  # is key exist?
                        shopVoucher_dict = db['shopVouchers']  # retrieve data
                    else:
                        print("shopVouchers don't exist.")  # start with empty
                except:
                    print("Error in retrieving shopVouchers from vouchers.db.")
                merchantShopVoucher_dict = {}
                try:
                    if merchantEmail in shopVoucher_dict:
                        merchantShopVoucher_dict = shopVoucher_dict[merchantEmail]
                    else:
                        print("Error in retreiving info from shop voucher fixed amt.")
                except:
                    print("Error occured in shop voucher dictionary.")

                for key in merchantShopVoucher_dict:
                    if usedVoucher is not None:
                        if merchantShopVoucher_dict[key].get_code() == usedVoucher.get_code() and merchantShopVoucher_dict[key].get_fixedAmt() == usedVoucher.get_fixedAmt():
                            currentquantity = merchantShopVoucher_dict[key].get_usageQuantity()
                            currentquantity -= 1
                            merchantShopVoucher_dict[key].set_usageQuantity(currentquantity)
                            break

                shopVoucher_dict[merchantEmail] = merchantShopVoucher_dict
                db['shopVouchers'] = shopVoucher_dict
                db.close()
            else:
                shopVoucher_dict={}
                percentagedb = shelve.open('shopVouchersPercentage.db', 'c')
                # shopVoucher_dict={merchant email:{shop voucher code: shop voucher object}}
                try:
                    if 'shopVouchersPercentage' in percentagedb:  # is key exist?
                        shopVoucher_dict = percentagedb['shopVouchersPercentage']  # retrieve data
                    else:
                        print("Error in retrieiving the percentage shop vouchers.")
                except:
                    print("Error in retrieving shopVouchers from vouchers.db.")
                merchantShopVoucherPercentage_dict = {}
                try:
                    if merchantEmail in shopVoucher_dict:
                        merchantShopVoucher_dict = shopVoucher_dict[merchantEmail]
                    else:
                        print("Unable to retreive from shop voucher percentage.")
                except:
                    print("Error occured in shop voucher dictionary.")

                for key in merchantShopVoucherPercentage_dict:
                    if usedVoucher is not None:
                        if merchantShopVoucherPercentage_dict[key].get_code() == usedVoucher.get_code() and merchantShopVoucherPercentage_dict[key].get_percentageOff() == usedVoucher.get_percentageOff():
                            currentquantity = merchantShopVoucherPercentage_dict[key].get_usageQuantity()
                            currentquantity -= 1
                            merchantShopVoucherPercentage_dict[key].set_usageQuantity(currentquantity)
                            break

                shopVoucher_dict[merchantEmail] = merchantShopVoucherPercentage_dict
                percentagedb['shopVouchersPercentage'] = shopVoucher_dict
                percentagedb.close()


        shoppingCarts = {}
        shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
        try:
            if "shoppingCart" in shoppingCartDB:  # is key exist?
                shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
            else:
                print("Shopping carts has an error.")  # start with empty
        except:
            print("Error in retrieving shopVouchers from vouchers.db.")

        userShoppingCart = None  # retrieves the shopping cart object
        try:
            if session['user'] in shoppingCarts:
                userShoppingCart = shoppingCarts[session['user']]
            else:
                print("Can't retrieve the user's shopping cart.")
        except:
            print("Error occured in dictionary.")

        db.close()

    db = shelve.open("customer.db", 'c')
    customers_dict = db["Customer"]
    email = customers_dict.get(session['user'])
    if userShoppingCart.get_chosenWebsiteReward() is None:
        points_checkout = paymentDetail.get_subTotal() / 10
        cust_up = email.get_points_usable() + points_checkout
        email.set_points_usable(int(cust_up))

        cust_nup = email.get_points() + points_checkout
        email.set_points(int(cust_nup))

        print(cust_up, "point useable")
        print(cust_nup, "point non-useable")

        db["Customer"] = customers_dict
        db.close()


        db = shelve.open("customer.db", 'c')
        customers_dict = db["Customer"]
        email = customers_dict.get(session['user'])

        # wr_chosen = None
        # print(wr_chosen)
        # email.update_rewards_indiv(wr_chosen)
        # db["Customer"] = customers_dict
        # db.close()
        # print(email.get_rewards_indiv(), "lalalalalaalalallalla")
    else:
        wr_chosen_minus = userShoppingCart.get_chosenWebsiteReward().get_points()

        print(wr_chosen_minus ,"points to minus")
        points_checkout = paymentDetail.get_subTotal() / 10

        cust_up = email.get_points_usable() + points_checkout - wr_chosen_minus
        email.set_points_usable(int(cust_up))

        cust_nup = email.get_points() + points_checkout
        email.set_points(int(cust_nup))

        print(cust_up, "point useable")
        print(cust_nup, "point non-useable")

        db["Customer"] = customers_dict
        db.close()


        db = shelve.open("customer.db", 'c')
        customers_dict = db["Customer"]
        email = customers_dict.get(session['user'])

        wr_chosen = userShoppingCart.get_chosenWebsiteReward().get_count()
        print(wr_chosen)
        email.update_rewards_indiv(wr_chosen)
        db["Customer"] = customers_dict
        db.close()
        print(email.get_rewards_indiv(), "lalalalalaalalallalla")

    # Junkai Adds transaction to the Merchant
    db = shelve.open("purchaseHistory.db", "r")
    purchase_history_dict = db["purchaseHistory"]
    db.close()
    list_prices = []
    list_merchants = []
    user_purchase_history = purchase_history_dict.get(session["user"])
    for count in user_purchase_history.get_purchaseHistory():
        list_prices.append(
            user_purchase_history.get_purchaseHistory().get(
                count).get_paymentDetails().get_shoppingCartObject().get_totalDiscountedPrice())
        merchants_dict2 = user_purchase_history.get_purchaseHistory().get(
            count).get_paymentDetails().get_shoppingCartObject().get_merchants()
        for merchant_email in merchants_dict2:
            list_merchants.append(merchant_email)
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    db = shelve.open("customer.db", "c")
    muser_dict = db["Merchant"]
    merchant = muser_dict.get(list_merchants[-1])
    transactions_list = merchant.get_transactions()
    merchant_balance = merchant.get_balance()
    wallet = Wallet(merchant_balance)
    wallet.top_up_amt(list_prices[-1])
    merchant.set_balance(wallet.get_balance())
    transaction_action = Transactions("Sales", list_prices[-1], d1, wallet.get_balance())
    transactions_list.append(transaction_action)
    db["Merchant"] = muser_dict
    db.close()
    # Junkai opens Db again to add the ADMIN FEE
    db = shelve.open("customer.db", "c")
    muser_dict = db["Merchant"]
    admin_dict = db["Admin"]
    merchant = muser_dict.get(list_merchants[-1])
    transactions_list = merchant.get_transactions()
    merchant_balance = merchant.get_balance()
    wallet = Wallet(merchant_balance)
    admin_tax = list_prices[-1] * 0.01
    wallet.withdraw_amt(admin_tax)
    merchant.set_balance(wallet.get_balance())
    transaction_admin_tax = Transactions("Admin Tax", admin_tax, d1, wallet.get_balance())
    transactions_list.append(transaction_admin_tax)
    db["Merchant"] = muser_dict
    for admin in admin_dict:
        admin_obj = admin_dict.get(admin)
        admins_wallet = Wallet(admin_obj.get_balance())
        admins_wallet.top_up_amt(admin_tax)
        admin_obj.set_balance(admins_wallet.get_balance())
        transaction_admin_tax = Transactions("Admin Tax", admin_tax, d1, admins_wallet.get_balance())
        admin_obj.add_transaction(transaction_admin_tax)
    db["Admin"] = admin_dict
    db.close()
    # Junkai reduce da quantity
    db = shelve.open("purchaseHistory.db", "r")
    purchase_history_dict = db["purchaseHistory"]
    db.close()
    customer_whole_purchase_history_obj = purchase_history_dict.get(session["user"])
    purchase_history_by_count = customer_whole_purchase_history_obj.get_purchaseHistory()
    list_users_purchases = []
    merchant_purchase = {}
    for count in purchase_history_by_count:
        purchase_history_obj = purchase_history_by_count.get(count)
        list_users_purchases.append(purchase_history_obj)
    latest_purchase = list_users_purchases[-1]
    for sbm_obj in latest_purchase.get_merchants():
        merchant_email = sbm_obj.get_merchantEmail()
        merchant_purchase[merchant_email] = []
        for sbp_obj in sbm_obj.get_products():
            product_id_and_quantity = sbp_obj.get_productID(), str(sbp_obj.get_quantity())
            merchant_purchase[merchant_email].append(list(product_id_and_quantity))
    db = shelve.open("customer.db", "c")
    musers_dict = db["Merchant"]
    db2 = shelve.open("products.db", "c")
    for merchant_email in merchant_purchase:
        list_all_purchases_for_this_merchant = merchant_purchase.get(merchant_email)
        for productId_quantity in list_all_purchases_for_this_merchant:
            merchants_products = musers_dict.get(merchant_email).get_products()
            product_object = merchants_products.get(productId_quantity[0])
            updated_quantity = product_object.get_quantity() - int(productId_quantity[1])
            product_object.set_quantity(updated_quantity)
            inventory_dict = db2["inventory" + merchant_email]
            inventory_obj = inventory_dict.get(product_object.get_inventory_name())
            inventory_obj.set_quantity(updated_quantity)
            db2["inventory" + merchant_email] = inventory_dict
    db["Merchant"] = musers_dict
    db.close()

    # reset the user's shopping cart
    userShoppingCart = ShoppingCart(session['user'])
    shoppingCarts[session['user']] = userShoppingCart
    shoppingCartDB["shoppingCart"] = shoppingCarts
    shoppingCartDB.close()

    return redirect(url_for('purchaseHistory'))


@app.route("/purchaseHistory", methods=['GET', 'POST'])
def purchaseHistory():
    purchaseHistory_dict = {}
    purchaseHistoryDB = shelve.open('purchaseHistory.db', 'c')
    cust = shelve.open("customer.db", "r")
    customer = cust["Customer"].get(session["user"])
    profile_pic = customer.get_profile_picture()
    detail = "{} {}".format(customer.get_first_name(), customer.get_last_name())
    try:
        if "purchaseHistory" in purchaseHistoryDB:  # is key exist?
            purchaseHistory_dict = purchaseHistoryDB["purchaseHistory"]  # retrieve data
        else:
            purchaseHistoryDB["purchaseHistory"] = purchaseHistory_dict  # start with empty
    except:
        print("Error in retrieving Shopping cart from shoppingcartDB.db.")

    userPurchaseHist = WholePurchaseHistory()
    try:
        if session['user'] in purchaseHistory_dict:
            userPurchaseHist = purchaseHistory_dict[session['user']]
        else:
            purchaseHistory_dict[session['user']] = userPurchaseHist
    except:
        print("Error occured in dictionary.")

    userPH_list = []
    userPH_dict = userPurchaseHist.get_purchaseHistory()
    count = len(userPH_dict)
    if count != 0:
        for key in userPH_dict:
            userPH_list.append(userPH_dict[count])
            count -= 1
    for userPh in userPH_list:
        for merchant in userPh.get_merchants():
            for product in merchant.get_products():
                print(merchant.get_merchantEmail())

    return render_template("customer/purchaseHistory.html", details=detail, profile_pic=profile_pic,
                           userPH_list=userPH_list)


@app.route("/addToFavourite/<productid>", methods=['GET', 'POST'])
def addToFavourite(productid):
    favourites_dict = {}
    favouritesDB = shelve.open('purchaseHistory.db', 'c')
    try:
        if "favourites" in favouritesDB:  # is key exist?
            favourites_dict = favouritesDB["favourites"]  # retrieve data
        else:
            favouritesDB["favourites"] = favourites_dict  # start with empty
    except:
        print("Error in retrieving Shopping cart from shoppingcartDB.db.")

    userFavourites = Favourite()
    try:
        if session['user'] in favourites_dict:
            userFavourites = favourites_dict[session['user']]
        else:
            favourites_dict[session['user']] = userFavourites
    except:
        print("Error occured in dictionary.")

    favouriteItem = FavouriteItem(productid)
    userFavourites.add_favourite(favouriteItem)

    favourites_dict[session['user']] = userFavourites
    favouritesDB["favourites"] = favourites_dict
    favouritesDB.close()

    return redirect(url_for('show_individual_product', productID=productid))


@app.route("/deleteFromFavourite/<productid>", methods=['GET', 'POST'])
def deleteFromFavourite(productid):
    favourites_dict = {}
    favouritesDB = shelve.open('purchaseHistory.db', 'c')
    try:
        if "favourites" in favouritesDB:  # is key exist?
            favourites_dict = favouritesDB["favourites"]  # retrieve data
        else:
            favouritesDB["favourites"] = favourites_dict  # start with empty
    except:
        print("Error in retrieving Shopping cart from shoppingcartDB.db.")

    userFavourites = Favourite()
    try:
        if session['user'] in favourites_dict:
            userFavourites = favourites_dict[session['user']]
        else:
            favourites_dict[session['user']] = userFavourites
    except:
        print("Error occured in dictionary.")

    deleteFavourite = None
    for item in userFavourites.get_favouritedItems():
        if item.get_productID() == productid:
            deleteFavourite = item
    if deleteFavourite != None:
        userFavourites.delete_favourite(deleteFavourite)

    favourites_dict[session['user']] = userFavourites
    favouritesDB["favourites"] = favourites_dict
    favouritesDB.close()

    return redirect(url_for('show_individual_product', productID=productid))


@app.route("/favourites", methods=['GET','POST'])
def favourites():
    #checking if user is logged in
    try:
        userEmail = session['user']
    except:
        userEmail = None

    if userEmail is None:
        return redirect(url_for("login", id=2))

    favourites_dict = {}
    favouritesDB = shelve.open('purchaseHistory.db', 'c')
    try:
        if "favourites" in favouritesDB:  # is key exist?
            favourites_dict = favouritesDB["favourites"]  # retrieve data
        else:
            favouritesDB["favourites"] = favourites_dict  # start with empty
    except:
        print("Error in retrieving Shopping cart from shoppingcartDB.db.")

    userFavourites = Favourite()
    try:
        if session['user'] in favourites_dict:
            userFavourites = favourites_dict[session['user']]
        else:
            favourites_dict[session['user']] = userFavourites
    except:
        print("Error occured in dictionary.")
    favouritesDB.close()

    favouriteList=[]
    favouritesList = userFavourites.get_favouritedItems()
    length=len(favouritesList)-1
    while length>=0:
        favouriteList.append(favouritesList[length])
        length-=1
    favourite_num = userFavourites.get_numItems()
    db = shelve.open("customer.db", "r")
    cust_dict = db["Customer"]
    customer = cust_dict.get(session['user'])
    profile_pic = customer.get_profile_picture()
    details = "{} {}".format(customer.get_first_name(), customer.get_last_name())
    db.close()
    return render_template("customer/favourites.html", favouriteList=favouriteList, favourite_num=favourite_num, details=details, profile_pic=profile_pic)

#the ones that u first added to your lastest add
@app.route("/favourites_previouslyAdded",methods=['GET','POST'])
def favourites_previouslyAdded():
    #checking if user is logged in
    try:
        userEmail=session['user']
    except:
        userEmail = None

    if userEmail is None:
        return redirect(url_for("login", id=2))

    favourites_dict = {}
    favouritesDB = shelve.open('purchaseHistory.db', 'c')
    try:
        if "favourites" in favouritesDB:  # is key exist?
            favourites_dict = favouritesDB["favourites"]  # retrieve data
        else:
            favouritesDB["favourites"] = favourites_dict  # start with empty
    except:
        print("Error in retrieving Shopping cart from shoppingcartDB.db.")

    userFavourites = Favourite()
    try:
        if session['user'] in favourites_dict:
            userFavourites = favourites_dict[session['user']]
        else:
            favourites_dict[session['user']] = userFavourites
    except:
        print("Error occured in dictionary.")
    favouritesDB.close()

    favouriteList = userFavourites.get_favouritedItems()
    favourite_num = userFavourites.get_numItems()


    return render_template("customer/favourites.html",favouriteList=favouriteList,favourite_num=favourite_num)

#Price high to low
@app.route("/favourites_priceHtoL",methods=['GET','POST'])
def favourites_priceHtoL():
    #checking if user is logged in
    try:
        userEmail=session['user']
    except:
        userEmail = None

    if userEmail is None:
        return redirect(url_for("login", id=2))

    favourites_dict = {}
    favouritesDB = shelve.open('purchaseHistory.db', 'c')
    try:
        if "favourites" in favouritesDB:  # is key exist?
            favourites_dict = favouritesDB["favourites"]  # retrieve data
        else:
            favouritesDB["favourites"] = favourites_dict  # start with empty
    except:
        print("Error in retrieving Shopping cart from shoppingcartDB.db.")

    userFavourites = Favourite()
    try:
        if session['user'] in favourites_dict:
            userFavourites = favourites_dict[session['user']]
        else:
            favourites_dict[session['user']] = userFavourites
    except:
        print("Error occured in dictionary.")
    favouritesDB.close()

    favouritesList = userFavourites.get_favouritedItems()
    favourite_num = userFavourites.get_numItems()
    favouriteList=[]
    priceList=[]
    for x in favouritesList:
        if x.get_discountedPrice()==0:
            price=x.get_originalPrice()
        else:
            price=x.get_discountedPrice()
        priceList.append(price)

    priceList.sort(reverse=True)

    originalLen=len(favouritesList)
    currentLen=0

    while currentLen != originalLen:
        for y in priceList:

            for x in favouritesList:
                if x.get_discountedPrice()==0:
                    price=x.get_originalPrice()
                else:
                    price=x.get_discountedPrice()

                if y==price:
                    favouriteList.append(x)
                    currentLen+=1
                    break

    return render_template("customer/favourites_priceHtoL.html",favouriteList=favouriteList,favourite_num=favourite_num)

@app.route("/favourites_priceLtoH",methods=['GET','POST'])
def favourites_priceLtoH():
    #checking if user is logged in
    try:
        userEmail=session['user']
    except:
        userEmail = None

    if userEmail is None:
        return redirect(url_for("login", id=2))

    favourites_dict = {}
    favouritesDB = shelve.open('purchaseHistory.db', 'c')
    try:
        if "favourites" in favouritesDB:  # is key exist?
            favourites_dict = favouritesDB["favourites"]  # retrieve data
        else:
            favouritesDB["favourites"] = favourites_dict  # start with empty
    except:
        print("Error in retrieving Shopping cart from shoppingcartDB.db.")

    userFavourites = Favourite()
    try:
        if session['user'] in favourites_dict:
            userFavourites = favourites_dict[session['user']]
        else:
            favourites_dict[session['user']] = userFavourites
    except:
        print("Error occured in dictionary.")
    favouritesDB.close()

    favouritesList = userFavourites.get_favouritedItems()
    favourite_num = userFavourites.get_numItems()
    favouriteList=[]
    priceList=[]
    for x in favouritesList:
        if x.get_discountedPrice()==0:
            price=x.get_originalPrice()
        else:
            price=x.get_discountedPrice()
        priceList.append(price)

    priceList.sort()

    originalLen=len(favouritesList)
    currentLen=0

    while currentLen != originalLen:
        for y in priceList:

            for x in favouritesList:
                if x.get_discountedPrice()==0:
                    price=x.get_originalPrice()
                else:
                    price=x.get_discountedPrice()

                if y==price:
                    favouriteList.append(x)
                    currentLen+=1
                    break

    return render_template("customer/favourites_priceLtoH.html",favouriteList=favouriteList,favourite_num=favourite_num)

# MERCHANT SIDE


# Home
@app.route("/merchant", methods=["GET", "POST"])
def merchant_home():
    today = date.today()
    today_day = today.strftime("%d")
    list_seven_days = []
    for i in range(0, 7):
        week_day = int(today_day) - 6 + i
        week_date = today.strftime("%b") + " " + str(week_day)
        list_seven_days.append(week_date)
    weekly_products_purchased_dict = {}
    today_month = today.strftime("%m")
    today_year = today.strftime("%Y")
    today_day = today.strftime("%d")
    week_dates = []
    for i in range(0, 7):
        week_day = int(today_day) - 6 + i
        if week_day < 10:
            week_date = today_year + "-" + today_month + "-0" + str(week_day)
        else:
            week_date = today_year + "-" + today_month + "-" + str(week_day)
        week_dates.append(week_date)
    for date1 in week_dates:
        weekly_products_purchased_dict[date1] = 0
    print(weekly_products_purchased_dict)
    purchaseHistoryDB = shelve.open('purchaseHistory.db', 'c')
    purchase_history_dict = {}
    try:
        purchase_history_dict = purchaseHistoryDB["purchaseHistory"]
    except:
        print("No such key found dei")
    purchaseHistoryDB.close()
    list_purchases = []
    for customer_email in purchase_history_dict:
        customers_wholePurchaseHistory = purchase_history_dict.get(customer_email)
        customer_purchase_history = customers_wholePurchaseHistory.get_purchaseHistory()
        for count in customer_purchase_history:
            list_purchases.append(customer_purchase_history.get(count))
    for purchase_history in list_purchases:
        payment_date = purchase_history.get_paymentDetails().get_dateOfPayment()
        for sbm_obj in purchase_history.get_merchants():
            if sbm_obj.get_merchantEmail() == session["user"]:
                for sbp_obj in sbm_obj.get_products():
                    updated_amount = weekly_products_purchased_dict.get(str(payment_date)) + sbp_obj.get_quantity()
                    weekly_products_purchased_dict[str(payment_date)] = updated_amount
    db = shelve.open("customer.db", "r")
    muser_dict = {}
    try:
        muser_dict = db["Merchant"]
    except:
        print("Error for merchant dict")
    db.close()
    merchant = muser_dict.get(session['user'])
    merchant_list_of_products = []
    merchant_products_dictionary = merchant.get_products()
    wallet_balance = merchant.get_balance()
    for key in merchant_products_dictionary:
        merchant_list_of_products.append(key)
    number_of_products = len(merchant_list_of_products)
    db = shelve.open('to_do.db', 'c')
    td_dict = {}
    try:
        td_dict = db['td_item' + session['user']]
    except:
        print('error')
    db.close()
    td_list = []
    for key in td_dict:
        td_item = td_dict.get(key)
        td_list.append(td_item)
    create_td_form = TdForm(request.form)
    if request.method == 'POST' and create_td_form.validate():
        db = shelve.open('to_do.db', "c")
        td_item = To_do(create_td_form.td_item.data)
        td_dict[td_item.get_td_item()] = td_item
        db["td_item" + session['user']] = td_dict
        db.close()
        return redirect(url_for('merchant_home'))
    return render_template('merchant/merchant_home.html', merchant=merchant, form=create_td_form, count=len(td_list),
                           td_list=td_list, user=merchant, number_of_products=number_of_products,
                           wallet_balance=wallet_balance, list_seven_days=list_seven_days,
                           weekly_products_purchased_dict=weekly_products_purchased_dict)


@app.route('/deleteTd/<id>', methods=['POST'])
def delete_td(id):
    td_dict = {}
    db = shelve.open('to_do.db', 'w')
    try:
        td_dict = db["td_item" + session['user']]
    except:
        print('error')
    td_dict.pop(id)
    db['td_item' + session["user"]] = td_dict
    db.close()
    return redirect(url_for('merchant_home'))


@app.route("/merchant_orders")
def merchant_orders():
    db = shelve.open("customer.db", "r")
    musers_dict = {}
    try:
        musers_dict = db["Merchant"]
    except:
        print("error retrieving merchants")
    db.close()
    merchant = musers_dict.get(session["user"])
    return render_template("merchant/merchant_orders.html", merchant=merchant)


@app.route("/completed_orders")
def completed_orders():
    db = shelve.open("customer.db", "r")
    musers_dict = {}
    try:
        musers_dict = db["Merchant"]
    except:
        print("error retrieving merchants")
    db.close()
    merchant = musers_dict.get(session["user"])
    purchaseHistoryDB = shelve.open('purchaseHistory.db', 'r')
    purchase_history_dict = purchaseHistoryDB["purchaseHistory"]
    purchaseHistoryDB.close()
    list_purchases = []
    for customer_email in purchase_history_dict:
        customers_wholePurchaseHistory = purchase_history_dict.get(customer_email)
        customer_purchase_history = customers_wholePurchaseHistory.get_purchaseHistory()
        for count in customer_purchase_history:
            list_purchases.append(customer_purchase_history.get(count))
    merchant_user_products = {}
    for purchase_history in list_purchases:
        for sbm_obj in purchase_history.get_merchants():
            merchant_user_products[sbm_obj.get_merchantEmail()] = []
    for purchase_history in list_purchases:
        for sbm_obj in purchase_history.get_merchants():
            list_products = merchant_user_products.get(sbm_obj.get_merchantEmail())
            for product in sbm_obj.get_products():
                list_products.append(product)
                merchant_user_products[sbm_obj.get_merchantEmail()] = list_products
    list_merchant_orders = merchant_user_products.get(session["user"])
    if list_merchant_orders is None:
        list_merchant_orders = []
    else:
        pass
    return render_template("merchant/view_completed_orders.html", merchant=merchant, list_orders=list_merchant_orders,
                           list_length=len(list_merchant_orders))

# Products
@app.route("/merchant_products", methods=["GET", "POSt"])
def merchant_products():
    db = shelve.open('customer.db', 'r')
    muser_dict = db["Merchant"]
    db.close()
    merchant = muser_dict.get(session['user'])
    products_dict = merchant.get_products()
    product_list = []
    for key in products_dict:
        product = products_dict.get(key)
        product_list.append(product)
    return render_template("merchant/merchant_products.html", merchant=merchant, product_list=product_list)


@app.route("/merchant_add_product", methods=["GET", "POST"])
def merchant_add_product():
    db = shelve.open("customer.db", "r")
    m_dict = db["Merchant"]
    merchant = m_dict.get(session["user"])
    db.close()
    db = shelve.open("products.db", "c")
    inventory_dict = {}
    try:
        inventory_dict = db['inventory' + session['user']]
    except:
        print("error")
    db.close()
    inventory_list = []
    inventory_names = []
    inventory_cat = []
    for key in inventory_dict:
        inventory_item = inventory_dict.get(key)
        inventory_list.append(inventory_item)
        inventory_names.append(inventory_item.get_name())
        inventory_cat.append(inventory_item.get_category())
    add_product_form = CreateProductForm(request.form)
    if request.method == 'POST' and add_product_form.validate():
        db = shelve.open('customer.db', "c")
        muser_dict = {}
        try:
            muser_dict = db["Merchant"]
        except:
            print("Error in retrieving products from customer.db.")
        inventory_name = request.form.get("inventory_name")
        if inventory_name == "":
            inventory_quantity = 0
        else:
            inventory_object = inventory_dict.get(inventory_name)
            inventory_quantity = inventory_object.get_quantity()
        product = SubCategory(add_product_form.product_cat.data, add_product_form.product_name.data,
                              add_product_form.product_price.data, add_product_form.product_desc.data,
                              add_product_form.product_sub_cat.data, inventory_quantity, inventory_name,
                              add_product_form.base.data)
        merchant = muser_dict.get(session['user'])
        m_products_dict = merchant.get_products()
        m_products_dict[product.get_product_id()] = product
        merchant.set_products(m_products_dict)
        db["Merchant"] = muser_dict
        db.close()
        # Store Inside Products DB
        db = shelve.open("products.db", "c")
        products_dict = {}
        try:
            products_dict = db["products"]
            inventory_dict = db["inventory" + session['user']]
        except:
            print("Error in retrieving products from products.db.")
        if inventory_name != "":
            inventory_object = inventory_dict.get(inventory_name)
            inventory_object.set_product_assigned(product)
            db["inventory" + session['user']] = inventory_dict
        else:
            print("no inventory selected for this product")
        products_dict[product.get_product_id()] = product
        db["products"] = products_dict
        db.close()
        return redirect(url_for('merchant_products'))
    return render_template("merchant/add_new_product.html",
                           form=add_product_form, merchant=merchant,
                           inventory_list=inventory_list, inventory_names=inventory_names, inventory_cat=inventory_cat,
                           inventory_length=len(inventory_list))

@app.route('/delete_product/<id>', methods=['POST'])
def delete_product(id):
    dbm = shelve.open('customer.db', 'w')
    muser_dict = dbm['Merchant']
    merchant = muser_dict.get(session["user"])
    product_dict = merchant.get_products()
    product_dict.pop(id)
    merchant.set_products(product_dict)
    dbm["Merchant"] = muser_dict
    dbm.close()
    db = shelve.open('products.db', "w")
    products_dict = db['products']
    inventory_dict = db["inventory" + session['user']]
    product = products_dict.get(id)
    inventory_name = product.get_inventory_name()
    inventory_object = inventory_dict.get(inventory_name)
    if inventory_object is None:
        pass
    else:
        inventory_object.set_product_assigned(None)
    db["inventory" + session['user']] = inventory_dict
    products_dict.pop(id)
    db["products"] = products_dict
    db.close()
    return redirect(url_for('merchant_products'))


@app.route('/update_product/<id>/', methods=['GET', 'POST'])
def update_product(id):
    db = shelve.open("products.db", "r")
    inventory_dict = {}
    try:
        inventory_dict = db['inventory' + session['user']]
    except:
        print("error")
    db.close()
    inventory_list = []
    inventory_names = []
    inventory_cat = []
    for key in inventory_dict:
        inventory_item = inventory_dict.get(key)
        inventory_list.append(inventory_item)
        inventory_names.append(inventory_item.get_name())
        inventory_cat.append(inventory_item.get_category())
    update_product_form = CreateProductForm(request.form)
    if request.method == 'POST' and update_product_form.validate():
        db = shelve.open('customer.db', 'w')
        muser_dict = db['Merchant']
        merchant = muser_dict.get(session["user"])
        products_dict = merchant.get_products()
        product = products_dict.get(id)
        product.set_product_cat(update_product_form.product_cat.data)
        product.set_product_name(update_product_form.product_name.data)
        product.set_product_price(update_product_form.product_price.data)
        product.set_product_desc(update_product_form.product_desc.data)
        product.set_sub_cat(update_product_form.product_sub_cat.data)
        inventory_name = request.form.get("inventory_name")
        if inventory_name == "":
            inventory_quantity = 0
        else:
            inventory_object = inventory_dict.get(inventory_name)
            inventory_quantity = inventory_object.get_quantity()
        product.set_inventory_name(inventory_name)
        product.set_quantity(inventory_quantity)
        merchant.set_products(products_dict)
        db['Merchant'] = muser_dict
        db.close()
        db = shelve.open("products.db", "c")
        products_dict = {}
        try:
            products_dict = db["products"]
            inventory_dict = db["inventory" + session['user']]
        except:
            print("Error in retrieving products from products.db.")
        # update the product in products.db
        products_dict[product.get_product_id()] = product
        db["products"] = products_dict
        # set the assigned inventory a product
        if inventory_name != "":
            inventory_object = inventory_dict.get(inventory_name)
            inventory_object.set_product_assigned(product)
            db["inventory" + session['user']] = inventory_dict
            db.close()
        else:
            pass
        return redirect(url_for('merchant_products'))
    else:
        db = shelve.open('customer.db', 'r')
        muser_dict = db['Merchant']
        db.close()
        merchant = muser_dict.get(session["user"])
        products_dict = merchant.get_products()
        product = products_dict.get(id)
        update_product_form.product_cat.data = product.get_product_cat()
        update_product_form.product_name.data = product.get_product_name()
        update_product_form.product_price.data = product.get_product_price()
        update_product_form.product_desc.data = product.get_product_desc()
        update_product_form.product_sub_cat.data = product.get_sub_cat()
        inventory_name = product.get_inventory_name()
        if inventory_name != "":
            db = shelve.open("products.db", "r")
            inventory_dict = {}
            try:
                inventory_dict = db["inventory" + session['user']]
            except:
                print("error")
            inventory_category = inventory_dict.get(inventory_name).get_category()
            inventory_quantity = inventory_dict.get(inventory_name).get_quantity()
            db.close()
        else:
            inventory_category = None
            inventory_quantity = product.get_quantity()
        db = shelve.open("customer.db", 'r')
        m_dict = db['Merchant']
        merchant = m_dict.get(session['user'])

        return render_template('merchant/update_product.html', form=update_product_form, merchant=merchant,
                               inventory_list=inventory_list, inventory_names=inventory_names,
                               inventory_cat=inventory_cat, inventory_item_name=inventory_name,
                               inventory_item_category=inventory_category, inventory_item_quantity=inventory_quantity
                               , inventory_length=len(inventory_list))


@app.route('/view_product/<product>', methods=['POST'])
def view_product(product):
    db = shelve.open('customer.db', 'r')
    musers_dict = db['Merchant']
    db.close()
    merchant = musers_dict.get(session["user"])
    products_dict = merchant.get_products()
    product_detail = products_dict.get(product)
    rating = 0
    for i in product_detail.get_review():
        rating += int(i.get_rating())
    if len(product_detail.get_review()) == 0:
        avg = 0
    else:
        avg = rating / len(product_detail.get_review())
    purchaseHistoryDB = shelve.open('purchaseHistory.db', 'r')
    try:
        purchase_history_dict = purchaseHistoryDB["purchaseHistory"]
    except:
        print("error purchase_history_dict")
        purchase_history_dict = {}
    purchaseHistoryDB.close()
    list_purchases = []
    for customer_email in purchase_history_dict:
        customers_wholePurchaseHistory = purchase_history_dict.get(customer_email)
        customer_purchase_history = customers_wholePurchaseHistory.get_purchaseHistory()
        for count in customer_purchase_history:
            list_purchases.append(customer_purchase_history.get(count))
    merchant_user_products = {}
    for purchase_history in list_purchases:
        for sbm_obj in purchase_history.get_merchants():
            merchant_user_products[sbm_obj.get_merchantEmail()] = []
    for purchase_history in list_purchases:
        for sbm_obj in purchase_history.get_merchants():
            list_products = merchant_user_products.get(sbm_obj.get_merchantEmail())
            for product1 in sbm_obj.get_products():
                list_products.append(product1)
                merchant_user_products[sbm_obj.get_merchantEmail()] = list_products
    list_merchant_orders = merchant_user_products.get(session["user"])
    if list_merchant_orders is None:
        list_merchant_orders = []
    else:
        pass
    product_id_dict = {}
    for order in list_merchant_orders:
        product_id_dict[order.get_productID()] = []
    for order in list_merchant_orders:
        product_id_dict.get(order.get_productID()).append(order.get_quantity())
    if product in product_id_dict:
        products_sold = sum(product_id_dict.get(product))
    else:
        products_sold = 0
    return render_template("merchant/view_product.html", product=product_detail, avg=avg, merchant=merchant,
                           products_sold=products_sold)


@app.route("/merchant_inventory", methods=["POST", "GET"])
def merchant_inventory():
    db = shelve.open("customer.db", "r")
    m_dict = db["Merchant"]
    merchant = m_dict.get(session['user'])
    inventory_dict = {}
    db = shelve.open("products.db", "r")
    try:
        inventory_dict = db['inventory' + session['user']]
    except:
        print("error in retrieving inventory")
    db.close()
    inventory_list = []
    inventory_names = []
    for key in inventory_dict:
        inventory_item = inventory_dict.get(key)
        inventory_list.append(inventory_item)
        inventory_names.append(inventory_item.get_name())
    create_inventory_form = InventoryForm(request.form)
    if request.method == "POST" and create_inventory_form.validate():
        db = shelve.open("products.db", "c")
        try:
            inventory_dict = db["inventory" + session['user']]
        except:
            print("Error in retrieving inventory for this user")
        inventory = Inventory(0, create_inventory_form.inventory_category.data,
                              create_inventory_form.inventory_name.data, create_inventory_form.inventory_price.data)
        choices = ["XS", "S", "M", "L", "XL"]
        inventory_dict_of_sizes = inventory.get_dict_of_sizes()
        for i in choices:
            size_object = SizeAndQuantity(i, 0)
            inventory_dict_of_sizes[size_object.get_size_name()] = size_object
        print(inventory.get_dict_of_sizes())
        inventory_dict[inventory.get_name()] = inventory
        db["inventory" + session['user']] = inventory_dict
        db.close()
        return redirect(url_for("merchant_inventory"))
    return render_template("merchant/merchant_inventory.html", merchant=merchant, form=create_inventory_form,
                           inventory_list=inventory_list, inventory_names=inventory_names)



@app.route("/delete_inventory/<name>", methods=['POST'])
def delete_inventory(name):
    db = shelve.open("products.db", "c")
    dbm = shelve.open('customer.db', "c")
    musers_dict = {}
    inventory_dict = {}
    try:
        musers_dict = dbm["Merchant"]
        inventory_dict = db["inventory" + session['user']]
    except:
        print("error")
    merchant = musers_dict.get(session['user'])
    merchant_products_dict = merchant.get_products()
    print(inventory_dict.get(name))
    product_assigned_w_inv = inventory_dict.get(name).get_product_assigned()
    if product_assigned_w_inv is None:
        inventory_dict.pop(name)
        db["inventory" + session['user']] = inventory_dict
    else:
        product = merchant_products_dict.get(product_assigned_w_inv.get_product_id())
        product.set_inventory_name("")
        product.set_quantity(0)
        merchant.set_products(merchant_products_dict)
        inventory_dict.pop(name)
        dbm["Merchant"] = musers_dict
        db["inventory" + session['user']] = inventory_dict
    db.close()
    dbm.close()
    return redirect(url_for("merchant_inventory"))


@app.route("/view_inventory/<name>/", methods=["POST", "GET"])
def view_inventory(name):
    db = shelve.open("products.db", "c")
    inventory_dict = {}
    try:
        inventory_dict = db["inventory" + session["user"]]
    except:
        print("error")
    inventory_item = inventory_dict.get(name)
    size_form = SizeForm(request.form)
    shirt_sizes = []
    shirt_size_objects = []
    db2 = shelve.open("customer.db", "r")
    merchant_dict = db2["Merchant"]
    merchant = merchant_dict.get(session['user'])
    sup = merchant.get_supplier()
    supplier = None
    for x in sup:
        if x.get_product() == name:
            supplier = x.get_name()
    for i in inventory_item.get_dict_of_sizes():
        shirt_sizes.append(i)
        shirt_size_objects.append(inventory_item.get_dict_of_sizes().get(i))
    add_quantity_form = SizeForm(request.form)
    quantity_list = []
    add_quantity_others_form = QtyForm(request.form)
    if request.method == "POST" and add_quantity_others_form.validate():
        inventory_item.add_quantity(add_quantity_others_form.quantity_to_add.data)
        db["inventory" + session["user"]] = inventory_dict
        # store in the new quantity in products_dict for merchant
        db2 = shelve.open("customer.db", "c")
        musers_dict = {}
        try:
            musers_dict = db2["Merchant"]
        except:
            print("error retrieving merchant from line 422")
        merchant = musers_dict.get(session["user"])
        products_dict = merchant.get_products()
        product = None
        try:
            print(inventory_item)
            product = products_dict.get(inventory_item.get_product_assigned().get_product_id())
        except:
            print("error in retrieving in line 426")
        if product is None:
            pass
        else:
            product.set_quantity(inventory_item.get_quantity())
        db2["Merchant"] = musers_dict
        db2.close()
        db3 = shelve.open("customer.db", "c")
        musers_dict = db3["Merchant"]
        merchant = musers_dict.get(session["user"])
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        merchant_balance = merchant.get_balance()
        wallet = Wallet(merchant_balance)
        wallet.withdraw_amt(add_quantity_others_form.total_cost_nosize.data)
        merchant.set_balance(wallet.get_balance())
        transaction_action = Transactions("Supplies", add_quantity_others_form.total_cost_nosize.data, d1,
                                          wallet.get_balance())
        merchant.get_transactions().append(transaction_action)
        db3["Merchant"] = musers_dict
        db3.close()
        return redirect(url_for("merchant_inventory"))
    if request.method == "POST" and add_quantity_form.validate():
        obj_size = inventory_item.get_dict_of_sizes().get(add_quantity_form.shirt_size.data)
        obj_size.add_qty(add_quantity_form.size_qty.data)
        inventory_item.get_dict_of_sizes()[obj_size.get_size_name()] = obj_size
        for i in shirt_size_objects:
            quantity_list.append(i.get_qty())
        inventory_item.set_quantity(sum(quantity_list))
        print(inventory_dict.get(inventory_item.get_name()).get_quantity())
        db["inventory" + session["user"]] = inventory_dict
        # store in the new quantity in products_dict for merchant
        db2 = shelve.open("customer.db", "c")
        musers_dict = {}
        try:
            musers_dict = db2["Merchant"]
        except:
            print("error retrieving merchant from line 422")
        merchant = musers_dict.get(session["user"])
        products_dict = merchant.get_products()
        product = None
        try:
            print(inventory_item)
            product = products_dict.get(inventory_item.get_product_assigned().get_product_id())
        except:
            print("error in retrieving in line 426")

        if product is None:
            pass
        else:
            product.set_quantity(sum(quantity_list))
        db2["Merchant"] = musers_dict
        db2.close()
        db3 = shelve.open("customer.db", "c")
        musers_dict = db3["Merchant"]
        merchant = musers_dict.get(session["user"])
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        merchant_balance = merchant.get_balance()
        wallet = Wallet(merchant_balance)
        wallet.withdraw_amt(add_quantity_form.total_cost.data)
        merchant.set_balance(wallet.get_balance())
        transaction_action = Transactions("Supplies", add_quantity_form.total_cost.data, d1, wallet.get_balance())
        merchant.get_transactions().append(transaction_action)
        db3["Merchant"] = musers_dict
        db3.close()
        return redirect(url_for("merchant_inventory"))
    db.close()
    return render_template("merchant/view_inventory.html", merchant=merchant, size_form=size_form,
                           inventory_item=inventory_item, supplier=supplier,
                           choices=shirt_sizes, shirt_size_objects=shirt_size_objects, form=add_quantity_form,
                           form2=add_quantity_others_form)


# Finances
@app.route("/merchant_myincome")
def merchant_myincome():
    db = shelve.open("customer.db", "r")
    musers_dict = {}
    try:
        musers_dict = db["Merchant"]
    except:
        print("error retrieving merchants")
    db.close()
    merchant = musers_dict.get(session["user"])
    purchaseHistoryDB = shelve.open('purchaseHistory.db', 'r')
    purchase_history_dict = {}
    try:
        purchase_history_dict = purchaseHistoryDB["purchaseHistory"]
    except:
        print("no such key dei")
    purchaseHistoryDB.close()
    list_purchases = []
    for customer_email in purchase_history_dict:
        customers_wholePurchaseHistory = purchase_history_dict.get(customer_email)
        customer_purchase_history = customers_wholePurchaseHistory.get_purchaseHistory()
        for count in customer_purchase_history:
            list_purchases.append(customer_purchase_history.get(count))
    merchant_user_products = {}
    for purchase_history in list_purchases:
        for sbm_obj in purchase_history.get_merchants():
            merchant_user_products[sbm_obj.get_merchantEmail()] = []
    for purchase_history in list_purchases:
        for sbm_obj in purchase_history.get_merchants():
            list_products = merchant_user_products.get(sbm_obj.get_merchantEmail())
            for product in sbm_obj.get_products():
                list_products.append(product)
                merchant_user_products[sbm_obj.get_merchantEmail()] = list_products
    list_merchant_orders = merchant_user_products.get(session["user"])
    if list_merchant_orders is None:
        list_merchant_orders = []
    else:
        pass
    category_dict = {}
    for sbp_obj in list_merchant_orders:
        product_category = sbp_obj.get_productObject().get_product_cat()
        category_dict[product_category] = SalesIncome(product_category)
    for sbp_obj in list_merchant_orders:
        product_category = sbp_obj.get_productObject().get_product_cat()
        category_income_obj = category_dict.get(product_category)
        category_income_obj.add_quantity(sbp_obj.get_quantity())
        category_income_obj.add_sales(sbp_obj.get_totalPrice())
    return render_template("merchant/merchant_myincome.html", merchant=merchant, category_dict=category_dict)


@app.route("/merchant_mywallet", methods=["GET", "POST"])
def merchant_mywallet():
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    month_year_today = today.strftime("%B %Y")
    withdraw_form = WithdrawForm(request.form)
    topup_form = TopUpForm(request.form)
    db = shelve.open("customer.db", "c")
    muser_dict = db["Merchant"]
    merchant = muser_dict.get(session['user'])
    transactions_list = merchant.get_transactions()
    merchant_balance = merchant.get_balance()
    wallet = Wallet(merchant_balance)
    if request.method == "POST" and withdraw_form.validate():
        wallet.withdraw_amt(withdraw_form.withdraw_amount.data)
        merchant.set_balance(wallet.get_balance())
        transaction_action = Transactions("Withdrawal", withdraw_form.withdraw_amount.data, d1, wallet.get_balance())
        transactions_list.append(transaction_action)
        db["Merchant"] = muser_dict
        db.close()
        return redirect(url_for("merchant_mywallet"))
    if request.method == "POST" and topup_form.validate():
        wallet.top_up_amt(topup_form.top_up_amt.data)
        merchant.set_balance(wallet.get_balance())
        transaction_action = Transactions("Top-Up", topup_form.top_up_amt.data, d1, wallet.get_balance())
        transactions_list.append(transaction_action)
        db["Merchant"] = muser_dict
        db.close()
        return redirect(url_for("merchant_mywallet"))
    db.close()
    return render_template("merchant/merchant_mywallet.html", form1=withdraw_form,
                           form2=topup_form, user=merchant, merchant=merchant, month_year_today=month_year_today)


@app.route("/view_transactions")
def view_transactions():
    db = shelve.open("customer.db", "r")
    muser_dict = {}
    try:
        muser_dict = db["Merchant"]
    except:
        print("error in retrieving merchants")
    db.close()
    merchant = muser_dict.get(session["user"])
    transaction_list = merchant.get_transactions()
    return render_template("merchant/view_transactions.html", merchant=merchant, transaction_list=transaction_list,
                           list_length=len(transaction_list))

# MERCHANT DATA INSIGHTS
@app.route("/merchant_insights")
def merchant_insights():
    db = shelve.open("purchaseHistory.db", "r")
    try:
        purchase_history_dict = db["purchaseHistory"]
    except:
        purchase_history_dict = {}
        print("no purchase history dict available")
    db.close()
    list_purchases = []
    for customer_email in purchase_history_dict:
        customers_wholePurchaseHistory = purchase_history_dict.get(customer_email)
        customer_purchase_history = customers_wholePurchaseHistory.get_purchaseHistory()
        for count in customer_purchase_history:
            list_purchases.append(customer_purchase_history.get(count))
    merchant_user_products = {}
    for purchase_history in list_purchases:
        for sbm_obj in purchase_history.get_merchants():
            merchant_user_products[sbm_obj.get_merchantEmail()] = []
    for purchase_history in list_purchases:
        for sbm_obj in purchase_history.get_merchants():
            list_products = merchant_user_products.get(sbm_obj.get_merchantEmail())
            for product in sbm_obj.get_products():
                list_products.append(product)
                merchant_user_products[sbm_obj.get_merchantEmail()] = list_products
    list_merchant_orders = merchant_user_products.get(session["user"])
    if list_merchant_orders is None:
        list_merchant_orders = []
    else:
        pass
    category_dict = {}
    for sbp_obj in list_merchant_orders:
        product_category = sbp_obj.get_productObject().get_product_cat()
        category_dict[product_category] = SalesIncome(product_category)
    for sbp_obj in list_merchant_orders:
        product_category = sbp_obj.get_productObject().get_product_cat()
        category_income_obj = category_dict.get(product_category)
        category_income_obj.add_quantity(sbp_obj.get_quantity())
        category_income_obj.add_sales(sbp_obj.get_totalPrice())
    dict_dates = []
    db = shelve.open("customer.db", "r")
    musers_dict = db["Merchant"]
    db.close()
    merchant = musers_dict.get(session["user"])
    transaction_list = merchant.get_transactions()
    for transaction in transaction_list:
        dict_dates.append(transaction.get_transaction_date())
    list_dates_sorted = sorted(dict_dates)
    sorted_dict = {}
    for date_insights in list_dates_sorted:
        sorted_dict[date_insights] = 0
    for transaction in transaction_list:
        if transaction.get_transaction_date() not in sorted_dict:
            print("transaction over the weekly date")
        else:
            sorted_dict[transaction.get_transaction_date()] = transaction.get_balance_after_transaction()
    today = date.today()
    today_day = today.strftime("%d")
    list_seven_days = []
    for i in range(0, 7):
        week_day = int(today_day) - 6 + i
        week_date = today.strftime("%b") + " " + str(week_day)
        list_seven_days.append(week_date)
    db = shelve.open("purchaseHistory.db", "r")
    purchases_dict = db["purchaseHistory"]
    db.close()
    # merchant Insights on customer
    merchant_customer = {}
    for customer_email in purchases_dict:
        customer = purchases_dict.get(customer_email)
        customer_purchaseH = customer.get_purchaseHistory()
        for count in customer_purchaseH:
            purchase = customer_purchaseH.get(count)
            for sbm_obj in purchase.get_merchants():
                merchant_email = sbm_obj.get_merchantEmail()
                merchant_customer[merchant_email] = {}
    for customer_email in purchases_dict:
        customer = purchases_dict.get(customer_email)
        customer_purchaseH = customer.get_purchaseHistory()
        for count in customer_purchaseH:
            purchase = customer_purchaseH.get(count)
            for sbm_obj in purchase.get_merchants():
                merchant_email = sbm_obj.get_merchantEmail()
                merchant_customer[merchant_email][customer_email] = []
    for customer_email in purchases_dict:
        customer = purchases_dict.get(customer_email)
        customer_purchaseH = customer.get_purchaseHistory()
        for count in customer_purchaseH:
            purchase = customer_purchaseH.get(count)
            for sbm_obj in purchase.get_merchants():
                merchant_email = sbm_obj.get_merchantEmail()
                for sbp_obj in sbm_obj.get_products():
                    merchant_customer[merchant_email][customer_email].append(sbp_obj.get_quantity())
    db = shelve.open("customer.db", "r")
    customers_dict = db["Customer"]
    db.close()
    merchant_customer_insights = merchant_customer.get(session["user"])
    print("Merchant hasnt sold any products")
    list_merchants_customers_gender = []
    try:
        for customer in merchant_customer_insights:
            customer_obj = customers_dict.get(customer)
            list_merchants_customers_gender.append(customer_obj.get_gender())
    except:
        print("this merchant has no transactions")
    try:
        percentage_male = str("{:.1f}".format(
            (list_merchants_customers_gender.count("Male") / len(list_merchants_customers_gender)) * 100)) + "%"
        percentage_female = str("{:.1f}".format(
            (list_merchants_customers_gender.count("Female") / len(list_merchants_customers_gender)) * 100)) + "%"
    except ZeroDivisionError:
        print("No customers have bought your products")
        percentage_male = 0
        percentage_female = 0
    db = shelve.open("customer.db", "r")
    customer_dict = db["Customer"]
    db.close()
    merchant_customer_obj = merchant_customer.get(session["user"])
    merchant_popular_customer = {}
    try:
        for customer in merchant_customer_obj:
            merchant_popular_customer[customer] = sum(merchant_customer_obj.get(customer))
    except:
        print("This merchant has no insights")
    print(merchant_popular_customer)
    popular_customer = None
    highest_value = 0
    for customer in merchant_popular_customer:
        if merchant_popular_customer.get(customer) > highest_value:
            popular_customer = customer
        else:
            highest_value = merchant_popular_customer.get(customer)
    best_customer_obj = customer_dict.get(popular_customer)
    try:
        full_name = best_customer_obj.get_first_name() + " " + best_customer_obj.get_last_name()
    except:
        print("this merchant has no insights")
        full_name = "None"
    popular_category = None
    highest_value_category = 0
    for category in category_dict:
        if category_dict.get(category).get_quantity() > highest_value_category:
            popular_category = category
        else:
            highest_value_category = category_dict.get(category).get_quantity()
    return render_template("merchant/merchant_insights.html", merchant=merchant,
                           category_dict=category_dict, sorted_dict=sorted_dict, list_seven_days=list_seven_days
                           , merchant_customer=merchant_customer, male=percentage_male, female=percentage_female
                           , best_customer=full_name, best_customer_email=popular_customer, popular_category=popular_category)


@app.route("/login_merchant", methods=["POST", "GET"])
def merchant_login():
    form = LoginForm(request.form)
    db = shelve.open("customer.db", "c")
    merchant_dict = {}
    try:
        if 'Merchant' in db:
            merchant_dict = db['Merchant']
        else:
            db["Merchant"] = merchant_dict
    except:
        print("File cannot be found ")
    if request.method == "POST":
        if form.email.data in db["Merchant"]:
            acc = merchant_dict.get(form.email.data)
            hashed = hashlib.sha3_256(form.password.data.encode())
            if acc.get_password() == hashed.hexdigest():
                session['user'] = acc.get_email()
                return redirect(url_for("merchant_home"))
            else:
                return render_template("Merchant/login_merchant.html", form=form, warning=1)
        else:
            return render_template("Merchant/login_merchant.html", form=form, warning=1)
    db.close()

    return render_template("Merchant/login_merchant.html", form=form)


@app.route("/createaccount_merchant", methods=["POST", "GET"])
def create_merchant():
    form = Merchant_create(request.form)
    validation = True
    password = form.password.data
    if request.method == 'POST':
        merchant_dict = {}
        db = shelve.open("customer.db", 'c')
        try:
            if 'Merchant' in db:
                merchant_dict = db['Merchant']
            else:
                db["Merchant"] = merchant_dict
        except:
            print("File cannot be found ")
        if form.email.data in db["Merchant"] and form.password.data != form.password_confirm.data:
            return render_template("Merchant/create_merchant.html", form=form, warning=1)
        elif form.email.data in db["Merchant"]:
            return render_template("Merchant/create_merchant.html", form=form, warning=2)
        elif form.password.data != form.password_confirm.data:
            return render_template("Merchant/create_merchant.html", form=form, warning=3)
        elif len(form.password.data) < 8:
            return render_template("Merchant/create_merchant.html", form=form, warning=4)
        elif len(form.password.data) > 20:
            return render_template("Merchant/create_merchant.html", form=form, warning=4)
        elif len(form.password.data) < 20:
            for i in range(0, len(form.password.data)):
                if (password[i].isalpha() == False) and (password[i].isdigit() == False):
                    return render_template("Customer/createaccount.html", form=form, warning=4)
                else:
                    hashed = hashlib.sha3_256(form.password.data.encode())
                    merchant = Merchant(form.first_name.data, form.last_name.data, form.email.data, form.phone.data,
                                        hashed.hexdigest())
                    merchant.set_cid(str(uuid4()))
                    date = datetime.now()
                    year = date.strftime("%Y")
                    month = date.strftime("%B")
                    day = date.strftime("%d")
                    merchant.set_date_joined("{} {} {}".format(day, month, year))
                    merchant.set_password_change([date.year, date.month, date.day])
                    merchant_dict[merchant.get_email()] = merchant
                    db["Merchant"] = merchant_dict
                    db.close()
                    return redirect(url_for("create_merchant1", id=merchant.get_email()))
        else:
            pass

    return render_template("Merchant/create_merchant.html", form=form)


@app.route("/createaccount1_merchant", methods=["POST", "GET"])
def create_merchant1():
    form = CreateAccountForm2(request.form)
    email = request.args.get('id')
    db = shelve.open("customer.db", 'c')
    merchant_dict = db["Merchant"]
    merchant = merchant_dict.get(email)
    if request.method == "POST":
        merchant.set_security_qn1(form.security_qn1.data)
        merchant.set_security_qn2(form.security_qn2.data)
        merchant.set_security_qn3(form.security_qn3.data)
        db["Merchant"] = merchant_dict
        db.close()
        return redirect(url_for("merchant_login"))
    db.close()
    return render_template("Merchant/create_merchant2.html", form=form)


@app.route("/merchant_setting")
def merchant_setting():
    db = shelve.open("customer.db", 'r')
    merchant_dict = db["Merchant"]
    merchant = merchant_dict.get(session['user'])
    main_address = merchant.get_main_address()
    main_address_postal = merchant.get_main_address_postal()
    main_address_unit = merchant.get_main_address_unit()
    storage_address = merchant.get_storage_address()
    storage_address_postal = merchant.get_storage_address_postal()
    storage_address_unit = merchant.get_storage_address_unit()
    email = session['user']
    form = edit_address(request.form)
    name = merchant_dict[email].get_first_name()
    db.close()
    return render_template("Merchant/merchant_setting.html", merchant=merchant, name=name, form=form, email=email,
                           main_address=main_address, main_address_postal=main_address_postal,
                           main_address_unit=main_address_unit, storage_address=storage_address,
                           storage_address_postal=storage_address_postal, storage_address_unit=storage_address_unit)


@app.route("/merchant_edit_main", methods=["POST", "GET"])
def edit_main_address():
    db = shelve.open("customer.db", 'c')
    merchant_dict = db["Merchant"]
    merchant = merchant_dict.get(session['user'])
    form = edit_address(request.form)
    if request.method == "POST":
        merchant.set_main_address(form.address.data)
        merchant.set_main_address_postal(form.postal.data)
        merchant.set_main_address_unit(form.unit.data)
        db["Merchant"] = merchant_dict
        db.close()
        return redirect(url_for("merchant_setting"))
    return render_template("Merchant/merchant_edit_main_address.html", form=form)


@app.route("/merchant_edit_store", methods=["POST", "GET"])
def edit_storage_address():
    db = shelve.open("customer.db", 'c')
    merchant_dict = db["Merchant"]
    merchant = merchant_dict.get(session['user'])
    form = edit_address(request.form)
    if request.method == "POST":
        merchant.set_storage_address(form.address.data)
        merchant.set_storage_address_postal(form.postal.data)
        merchant.set_storage_address_unit(form.unit.data)
        db["Merchant"] = merchant_dict
        db.close()
        return redirect(url_for("merchant_setting"))
    return render_template("Merchant/merchant_edit_store_address.html", form=form)


@app.route("/clear_storage")
def clear_storage_address():
    db = shelve.open("customer.db", 'c')
    merchant_dict = db["Merchant"]
    merchant = merchant_dict.get(session['user'])
    merchant.set_storage_address("")
    merchant.set_storage_address_postal("")
    merchant.set_storage_address_unit("")
    db["Merchant"] = merchant_dict
    db.close()
    return redirect(url_for('merchant_setting'))


@app.route("/clear_main")
def clear_main_address():
    db = shelve.open("customer.db", 'c')
    merchant_dict = db["Merchant"]
    merchant = merchant_dict.get(session['user'])
    merchant.set_main_address("")
    merchant.set_main_address_postal("")
    merchant.set_main_address_unit("")
    db["Merchant"] = merchant_dict
    db.close()
    return redirect(url_for('merchant_setting'))


@app.route("/supplier", methods=["GET", "POST"])
def supplier():
    db = shelve.open("customer.db", 'c')
    merchant_dict = db["Merchant"]
    merchant = merchant_dict.get(session['user'])
    supplier = merchant.get_supplier()
    db.close()
    db = shelve.open("products.db", "c")
    inventory_dict = {}
    try:
        inventory_dict = db["inventory" + session['user']]
    except:
        print("error line 2968")
    db.close()
    # print(supplier)
    return render_template("Merchant/supplier.html", merchant=merchant, supplier=supplier, inventory=inventory_dict)


@app.route("/add_supplier", methods=["GET", "POST"])
def add_supplier():
    form = Add_supplier(request.form)
    db = shelve.open("products.db", "c")
    inventory_dict = db["inventory" + session['user']]
    form.product.choices = [(inventory_dict[i].get_name()) for i in inventory_dict]
    db.close()
    if request.method == "POST":
        name = form.company.data
        product = form.product.data
        email = form.email.data
        phone = form.phone.data
        supplier = Supplier(name, email, phone, product)
        db = shelve.open("customer.db", 'c')
        merchant_dict = db["Merchant"]
        merchant = merchant_dict.get(session['user'])
        merchant.add_supplier(supplier)
        db["Merchant"] = merchant_dict
        db.close()

        return redirect(url_for("supplier"))
    return render_template("Merchant/add_supplier.html", form=form)


@app.route("/supplier_delete/<id>", methods=["POST", "GET"])
def supplier_delete(id):
    db = shelve.open("customer.db", 'c')
    merchant_dict = db["Merchant"]
    merchant = merchant_dict.get(session['user'])
    supplier = merchant.get_supplier()
    for i in supplier:
        if i.get_name() == id:
            supplier.remove(i)
    db["Merchant"] = merchant_dict
    db.close()
    return redirect(url_for("supplier"))


@app.route("/supplier_individual/<id>", methods=["POST", "GET"])
def supplier_individual(id):
    form = Supplier_quantity(request.form)
    db = shelve.open("customer.db", 'c')
    merchant_dict = db["Merchant"]
    merchant = merchant_dict.get(session['user'])
    supplier = merchant.get_supplier()
    db = shelve.open("products.db", "c")
    inventory_dict = db["inventory" + session['user']]
    for i in supplier:
        if i.get_name() == id:
            inventory = inventory_dict[i.get_product()]
            supplier = i
    if request.method == "POST":
        inventory.set_quantity(inventory.get_quantity() + form.quantity.data)
        db["inventory" + session['user']] = inventory_dict
        db.close()
    return render_template("Merchant/supplier_individual.html", supplier=supplier, merchant=merchant,
                           inventory=inventory, form=form)


@app.route("/edit_supplier/<id>", methods=["POST", "GET"])
def edit_supplier(id):
    form = Add_supplier(request.form)
    db = shelve.open("products.db", "c")
    inventory_dict = db["inventory" + session['user']]
    form.product.choices = [(inventory_dict[i].get_name()) for i in inventory_dict]
    if request.method == "POST":
        name = form.company.data
        product = form.product.data
        email = form.email.data
        phone = form.phone.data
        db = shelve.open("customer.db", 'c')
        merchant_dict = db["Merchant"]
        merchant = merchant_dict.get(session['user'])
        for i in merchant.get_supplier():
            if i.get_name() == id:
                i.set_product(product)
                i.set_name(name)
                i.set_email(email)
                i.set_phone(phone)
        db["Merchant"] = merchant_dict
        db.close()
        return redirect(url_for("supplier"))
    else:
        db = shelve.open("customer.db", 'r')
        merchant_dict = db["Merchant"]
        merchant = merchant_dict.get(session['user'])
        for i in merchant.get_supplier():
            if i.get_name() == id:
                print("he")
                supplier = i
                form.company.data = supplier.get_name()
                form.product.data = supplier.get_product()
                form.email.data = supplier.get_email()
                form.phone.data = supplier.get_phone()

    return render_template("Merchant/add_supplier.html", form=form, merchant=merchant)


@app.route("/merchant_account", methods=["GET", "POST"])
def shop_setting():
    db = shelve.open("customer.db", 'c')
    merchant_dict = db["Merchant"]
    merchant = merchant_dict.get(session['user'])
    return render_template("Merchant/merchant_account.html", merchant=merchant, user=merchant)


@app.route("/merchant_delete", methods=["POST", "GET"])
def merchant_delete():
    email = session['user']
    db = shelve.open("customer.db", 'c')
    merchant_dict = db["Merchant"]
    merchant_dict.pop(email)
    db["Merchant"] = merchant_dict
    db.close()
    session["user"] = None
    return redirect(url_for("home"))


@app.route("/merchant_change_password", methods=["POST", "GET"])
def merchant_change_password():
    form = Editpassword(request.form)
    if request.method == "POST":
        db = shelve.open("customer.db", 'c')
        merchant_dict = db["Merchant"]
        merchant = merchant_dict.get(session['user'])
        hashed = hashlib.sha3_256(form.current_password.data.encode())
        hashs = hashed.hexdigest()
        if hashs == merchant.get_password() and form.new_password.data == form.confirm_new_password.data:
            hashing = hashlib.sha3_256(form.new_password.data.encode())
            merchant.set_password(hashing.hexdigest())
            date = datetime.now()
            merchant.set_password_change([date.strftime("%Y"), date.strftime("%b"), date.strftime("%d")])
            db["Merchant"] = merchant_dict
            db.close()
            return redirect(url_for("shop_setting"))
    return render_template("Merchant/merchant_edit_password.html", form=form)


@app.route("/merchant_review")
def merchant_review():
    db = shelve.open("customer.db", 'r')
    merchant_dict = db["Merchant"]
    merchant = merchant_dict.get(session['user'])
    product = merchant.get_products()
    product_list = product.values()
    return render_template("Merchant/merchant_review.html", merchant=merchant, product_list=product_list)


@app.route("/merchant_review/<id>")
def review_detail(id):
    db = shelve.open("customer.db", 'r')
    merchant_dict = db["Merchant"]
    merchant = merchant_dict.get(session['user'])
    product = merchant.get_products()
    individual = product.get(id)
    review = individual.get_review()
    name = individual.get_product_name()
    return render_template("Merchant/merchant_review_detail.html", merchant=merchant, review=review, name=name)


@app.route("/merchant_profile")
def merchant_profile():
    email = session['user']
    db = shelve.open("customer.db", 'c')
    merchant_dict = db["Merchant"]
    merchant = merchant_dict.get(email)

    return render_template("Merchant/merchant_profile.html", merchant=merchant)


@app.route("/merchant_edit_profile", methods=["GET", "POST"])
def edit_merchant_profile():
    form = Edit_shop_profile(request.form)
    email = session['user']
    db = shelve.open("customer.db", 'c')
    merchant_dict = db["Merchant"]
    merchant = merchant_dict.get(email)
    if request.method == "POST":
        merchant.set_phone(form.phone.data)
        if merchant.get_email() != form.email.data:
            merchant_dict[form.email.data] = merchant_dict[email]
            merchant_dict.pop(session['user'])
            session['user'] = form.email.data
            merchant = merchant_dict.get(session['user'])
            merchant.set_email(session['user'])
        merchant.set_shop_description(form.shop_description.data)
        merchant.set_main_address(form.address.data)
        merchant.set_main_address_unit(form.unit.data)
        merchant.set_main_address_postal(form.postal.data)

        if form.base.data != "":
            merchant.set_profile_picture(form.base.data)
        db["Merchant"] = merchant_dict
        db.close()
        return redirect(url_for("merchant_profile"))
    else:
        db = shelve.open("customer.db", 'r')
        merchant_dict = db["Merchant"]
        merchant = merchant_dict.get(email)
        form.email.data = merchant.get_email()
        form.phone.data = merchant.get_phone()
        form.shop_description.data = merchant.get_shop_description()
        form.address.data = merchant.get_main_address()
        form.postal.data = merchant.get_main_address_postal()
        form.unit.data = merchant.get_main_address_unit()
        db.close()
    return render_template("Merchant/merchant_edit_profile.html", form=form)


@app.route("/merchant_edit_details", methods=["GET", "POST"])
def merchant_edit_detail():
    form = EditMerchant(request.form)
    email = session['user']

    if request.method == "POST":
        db = shelve.open("customer.db", 'c')
        merchant_dict = db["Merchant"]
        merchant = merchant_dict.get(email)
        merchant.set_email(form.email.data)
        merchant.set_phone(form.phone.data)
        db["Merchant"] = merchant_dict
        db.close()
        return redirect(url_for('shop_setting'))
    else:
        db = shelve.open("customer.db", 'r')
        merchant_dict = db["Merchant"]
        merchant = merchant_dict.get(email)
        form.email.data = merchant.get_email()
        form.phone.data = merchant.get_phone()
        db.close()
    return render_template("Merchant/merchant_edit.html", form=form)


@app.route("/merchant_forget_password", methods=["GET", "POST"])
def merchant_forget():
    form = Forget(request.form)
    notice = "A forget password email have been sent to your email"
    if request.method == "POST":
        db = shelve.open("customer.db", 'r')
        merchant_dict = db["Merchant"]
        merchant = merchant_dict.get(form.email.data)
        email = merchant.get_email()
        token = merchant.get_cid()
        message = "We received an inquire to reset your password, if is not you, ignore this email. key in your token:{} and new password with the following link to reset your password: http://127.0.0.1:5000/merchant_forget_token".format(token)
        with app.app_context():
            msg = Message(subject="Reset Password", sender="SingtopiaSG@gmail.com", recipients=[email], body=message)
            mail.send(msg)
            return render_template("Merchant/merchant_forget_password.html", form=form, notice=notice)
    return render_template("Merchant/merchant_forget_password.html", form=form)

@app.route("/merchant_forget_token", methods=["GET", "POST"])
def merchant_token():
    form = ForgetAcc(request.form)
    db = shelve.open("customer.db", "r")
    merchant_dict = db["Merchant"]
    for i in merchant_dict:
        if merchant_dict[i].get_cid() == form.token.data:
            email = merchant_dict[i].get_email()
            return redirect(url_for("merchant_forget_2", id=email))
    return render_template("Merchant/merchant_token.html", form=form)

@app.route("/merchant_forget_password2", methods=["POST", "GET"])
def merchant_forget_2():
    form = CreateAccountForm2(request.form)
    email = request.args.get('id')
    db = shelve.open("customer.db", 'r')
    merchant_dict = db["Merchant"]
    merchant = merchant_dict.get(email)
    if request.method == "POST":
        if merchant.get_security_qn1() == form.security_qn1.data and merchant.get_security_qn2() == form.security_qn2.data and merchant.get_security_qn3() == form.security_qn3.data:
            return redirect(url_for("merchant_new_password", id=email))
        else:
            return render_template("Merchant/merchant_forget_password2.html", form=form, warning=1)
    return render_template("Merchant/merchant_forget_password2.html", form=form, warning=0)


@app.route("/merchant_new_password", methods=["GET", "POST"])
def merchant_new_password():
    form = New_password(request.form)
    email = request.args.get("id")
    if request.method == "POST":
        db = shelve.open("customer.db", 'c')
        merchant_dict = db["Merchant"]
        merchant = merchant_dict.get(email)
        hashed = hashlib.sha3_256(form.password.data.encode())
        merchant.set_password(hashed.hexdigest())
        date = datetime.now()
        merchant.set_password_change([date.strftime("%Y"), date.strftime("%b"), date.strftime("%d")])
        merchant.get_cid(str(uuid4()))
        db["Merchant"] = merchant_dict
        db.close()
        return redirect(url_for("merchant_login"))
    return render_template("Merchant/merchant_new_password.html", form=form)


# ADMIN SIDE
@app.route("/admin", methods=["POST", "GET"])
def admin_login():
    form = LoginForm(request.form)
    admin = {}
    if request.method == "POST":
        try:
            db = shelve.open("customer.db", "r")
            admin = db["Admin"]
        except:
            db = shelve.open("customer.db", "c")
            db["Admin"] = admin
        if form.email.data in admin:
            acc = db['Admin'].get(form.email.data)
            hashed = hashlib.sha3_256(form.password.data.encode())
            db.close()
            if acc.get_password() == hashed.hexdigest():
                session['user'] = acc.get_email()
                return redirect(url_for("admin_home"))
            else:
                return render_template("Admins/admin_login.html", form=form, warning=1)
        else:
            return render_template("Admins/admin_login.html", form=form, warning=1)
    return render_template("Admins/admin_login.html", form=form, warning=0)


@app.route("/admin_home")
def admin_home():
    dict = {}
    try:
        purchasehistroy = shelve.open("purchaseHistory.db", "r")
        dict = purchasehistroy["purchaseHistory"]

    except:
        purchasehistroy = shelve.open("purchaseHistory.db", "c")
        purchasehistroy["purchaseHistory"] = dict
    purchasehistroy.close()
    data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    monthlist = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                 "November", "Decemeber"]
    list = []
    type = "Sales"
    for i in dict:
        a = dict[i].get_purchaseHistory().values()
        for x in a:
            list.append(x)
    for i in list:
        x = i.get_paymentDetails()
        if str(x.get_dateOfPayment())[5:7] == "01":
            data[0] += x.get_subTotal()
        elif str(x.get_dateOfPayment())[5:7] == "02":
            data[1] += x.get_subTotal()
        elif str(x.get_dateOfPayment())[5:7] == "03":
            data[2] += x.get_subTotal()
        elif str(x.get_dateOfPayment())[5:7] == "04":
            data[3] += x.get_subTotal()
        elif str(x.get_dateOfPayment())[5:7] == "05":
            data[4] += x.get_subTotal()
        elif str(x.get_dateOfPayment())[5:7] == "06":
            data[5] += x.get_subTotal()
        elif str(x.get_dateOfPayment())[5:7] == "07":
            data[6] += x.get_subTotal()
        elif str(x.get_dateOfPayment())[5:7] == "08":
            data[7] += x.get_subTotal()
        elif str(x.get_dateOfPayment())[5:7] == "09":
            data[8] += x.get_subTotal()
        elif str(x.get_dateOfPayment())[5:7] == "10":
            data[9] += x.get_subTotal()
        elif str(x.get_dateOfPayment())[5:7] == "11":
            data[10] += x.get_subTotal()
        elif str(x.get_dateOfPayment())[5:7] == "12":
            data[11] += x.get_subTotal()
        else:
            pass
    return render_template("Admins/admin.html",data=data, header=type)


@app.route("/admin_home/<type>")
def admin_dashboard(type):
    db = shelve.open("customer.db", "r")
    data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    monthlist = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                 "November", "Decemeber"]
    merchant_dict = db["Merchant"]
    customer_dict = db["Customer"]
    if type == "Merchant":
        for i in merchant_dict:
            month = merchant_dict[i].get_date_joined().split()[1]
            if month == monthlist[0]:
                data[0] += 1
            elif month == monthlist[1]:
                data[1] += 1
            elif month == monthlist[2]:
                data[2] += 1
            elif month == monthlist[3]:
                data[3] += 1
            elif month == monthlist[4]:
                data[4] += 1
            elif month == monthlist[5]:
                data[5] += 1
            elif month == monthlist[6]:
                data[6] += 1
            elif month == monthlist[7]:
                data[7] += 1
            elif month == monthlist[8]:
                data[8] += 1
            elif month == monthlist[9]:
                data[9] += 1
            elif month == monthlist[10]:
                data[10] += 1
            elif month == monthlist[11]:
                data[11] += 1
            else:
                pass
    elif type == "Visitor":
        for x in customer_dict:
            month = customer_dict[x].get_date_joined()[1]
            print(month)
            if month == "01":
                data[0] += 1
            elif month == "02":
                data[1] += 1
            elif month == "03":
                data[2] += 1
            elif month == "04":
                data[3] += 1
            elif month == "05":
                data[4] += 1
            elif month == "06":
                data[5] += 1
            elif month == "07":
                data[6] += 1
            elif month == "08":
                data[7] += 1
            elif month == "09":
                data[8] += 1
            elif month == "10":
                data[9] += 1
            elif month == "11":
                data[10] += 1
            elif month == "12":
                data[11] += 1
            else:
                pass
    elif type == "Products":
        for merchant in merchant_dict:
            for x in merchant_dict[merchant].get_products():
                month = str(merchant_dict[merchant].get_products()[x].get_date())
                months = month[5:7]
                if months == "01":
                    data[0] += 1
                elif months == "02":
                    data[1] += 1
                elif months == "03":
                    data[2] += 1
                elif months == "04":
                    data[3] += 1
                elif months == "05":
                    data[4] += 1
                elif months == "06":
                    data[5] += 1
                elif months == "07":
                    data[6] += 1
                elif months == "08":
                    data[7] += 1
                elif months == "09":
                    data[8] += 1
                elif months == "10":
                    data[9] += 1
                elif months == "11":
                    data[10] += 1
                elif months == "12":
                    data[11] += 1
                else:
                    pass
    elif type == "Sales":
        purchasehistroy = shelve.open("purchaseHistory.db", "r")
        dict = purchasehistroy["purchaseHistory"]
        list = []
        for i in dict:
            a = dict[i].get_purchaseHistory().values()
            for x in a:
                list.append(x)
        for i in list:
            x = i.get_paymentDetails()
            if str(x.get_dateOfPayment())[5:7] == "01":
                data[0] += x.get_subTotal()
            elif str(x.get_dateOfPayment())[5:7] == "02":
                data[1] += x.get_subTotal()
            elif str(x.get_dateOfPayment())[5:7] == "03":
                data[2] += x.get_subTotal()
            elif str(x.get_dateOfPayment())[5:7] == "04":
                data[3] += x.get_subTotal()
            elif str(x.get_dateOfPayment())[5:7] == "05":
                data[4] += x.get_subTotal()
            elif str(x.get_dateOfPayment())[5:7] == "06":
                data[5] += x.get_subTotal()
            elif str(x.get_dateOfPayment())[5:7] == "07":
                data[6] += x.get_subTotal()
            elif str(x.get_dateOfPayment())[5:7] == "08":
                data[7] += x.get_subTotal()
            elif str(x.get_dateOfPayment())[5:7] == "09":
                data[8] += x.get_subTotal()
            elif str(x.get_dateOfPayment())[5:7] == "10":
                data[9] += x.get_subTotal()
            elif str(x.get_dateOfPayment())[5:7] == "11":
                data[10] += x.get_subTotal()
            elif str(x.get_dateOfPayment())[5:7] == "12":
                data[11] += x.get_subTotal()
            else:
                pass
    return render_template("Admins/admin.html", data=data, header=type)


@app.route("/admin_orders")
def all_orders():
    admin_order = {}
    try:
        db = shelve.open("customer.db", "c")
        admin_order = db["Orders"]
    except:
        db = shelve.open("customer.db", "c")
        db["Orders"] = admin_order


    abc = []
    for x in admin_order:
        abc.append(admin_order[x])
    abc.sort(key=lambda x: x.get_paymentDetails().get_dateOfPayment(), reverse=True)
    db["Orders"] = admin_order
    db.close()
    # print(abc)
    return render_template("Admins/admin_orders.html", listt=abc)

@app.route("/admin_orders/<email>/<DOP>/<subtotal>")
def detailed_orders(email, DOP, subtotal):
    db = shelve.open("customer.db", "r")
    admin_order = db["Orders"]
    abc = []
    y = None
    for x in admin_order:
        abc.append(admin_order[x])
    for x in abc:
        if (x.get_userEmail() == email) and (float(x.get_paymentDetails().get_subTotal()) == float(subtotal)) and (str(x.get_paymentDetails().get_dateOfPayment()) == str(DOP)):
            y = x
    merdict = y.get_paymentDetails().get_shoppingCartObject()

    return render_template("Admins/admin_orders_detail.html", merdict=merdict)


@app.route("/admin_inbox")
def admin_inbox():
    db = shelve.open("customer.db", "c")
    feedback = {}
    try:
        feedback = db["Feedback"]
    except:
        print("error")
    return render_template("Admins/admin_inbox.html", feedback=feedback)


@app.route("/admin_inbox_reply/<email>", methods=["POST","GET"])
def admin_reply(email):
    form = Reply(request.form)
    db = shelve.open("customer.db", "c")
    feedback = db["Feedback"]
    recipient = feedback.get(email).get_name()
    if request.method == "POST":
        people = feedback.get(email)
        people.set_reply(True)
        db["Feedback"] = feedback
        with app.app_context():
            msg = Message(subject=form.subject.data, sender="SingtopiaSG@gmail.com", recipients=[email], body=form.message.data)
            mail.send(msg)
            return redirect(url_for("admin_inbox"))
    return render_template("Admins/admin_reply.html", form=form, recipient=recipient)


@app.route("/admin_inbox_delete/<email>")
def delete_message(email):
    db = shelve.open("customer.db", "c")
    feedback = db["Feedback"]
    feedback.pop(email)
    db["Feedback"] = feedback
    db.close()
    return redirect(url_for("admin_inbox"))

@app.route("/admin_customer")
def admin_customer():
    db = shelve.open("customer.db", 'r')
    customer_dict = {}
    try:
        if 'Customer' in db:
            customer_dict = db['Customer']
        else:
            db["Customer"] = customer_dict
    except:
        print("File cannot be found ")

    customer = customer_dict

    return render_template("Admins/admin_customer.html", customer=customer)


@app.route("/admin_customer_delete", methods=["POST"])
def delete_customer():
    if request.method == "POST":
        db = shelve.open("customer.db", "c")
        customer_dict = db["Customer"]

        customer_delete = request.form["email"]
        customer_delete = customer_delete.split(",")
        for i in customer_delete:
            customer_dict.pop(i)
        db["Customer"] = customer_dict
        db.close()
    return redirect(url_for("admin_customer"))


@app.route("/admin_merchant")
def admin_merchant():
    merchant_dict = {}
    db = shelve.open("customer.db", 'r')
    try:
        if 'Merchant' in db:
            merchant_dict = db['Merchant']
        else:
            db["Merchant"] = merchant_dict
    except:
        print("File cannot be found ")

    merchant = merchant_dict
    return render_template("Admins/admin_merchant.html", merchant=merchant)


@app.route("/admin_merchant_delete", methods=["POST"])
def delete_merchant():
    if request.method == "POST":
        db = shelve.open("customer.db", "c")
        merchant_dict = db["Merchant"]

        merchant_delete = request.form["email"]
        merchant_delete = merchant_delete.split(",")
        for i in merchant_delete:
            merchant_dict.pop(i)
        db["Merchant"] = merchant_dict
        db.close()
    return redirect(url_for("admin_merchant"))


@app.route("/admin_manage")
def admin_manage():
    db = shelve.open("customer.db", 'c')
    admin_dict = {}
    try:
        if 'Admin' in db:
            admin_dict = db['Admin']
        else:
            db["Admin"] = admin_dict
    except:
        print("File cannot be found ")

    return render_template("Admins/admin_management.html", admin=admin_dict)


@app.route("/delete_admin", methods=["GET", "POST"])
def delete_admin():
    if request.method == "POST":
        db = shelve.open("customer.db", "c")
        admin_dict = db["Admin"]

        admin_delete = request.form["email"]
        admin_delete = admin_delete.split(",")
        for i in admin_delete:
            admin_dict.pop(i)
        db["Admin"] = admin_dict
        db.close()
    return redirect(url_for("admin_manage"))



@app.route("/add_admin", methods=["GET", "POST"])
def add_admin():
    form = Add_admin(request.form)
    admin_dict = {}
    password = form.password.data
    if request.method == "POST":
        db = shelve.open("customer.db", "c")
        try:
            if 'Admin' in db:
                admin_dict = db['Admin']
            else:
                db["Admin"] = admin_dict
        except:
            print("File cannot be found ")
        if form.email.data in db["Admin"]:
            return render_template("Admins/add_admin.html", form=form, warning=1)
        elif form.password.data != form.password_confirm.data:
            return render_template("Admins/add_admin.html", form=form, warning=3)
        elif len(form.password.data) < 8:
            return render_template("Admins/add_admin.html", form=form, warning=4)
        elif len(form.password.data) > 20:
            return render_template("Admins/add_admin.html", form=form, warning=4)
        elif len(form.password.data) < 20:
            for i in range(0, len(form.password.data)):
                if (password[i].isalpha() == False) and (password[i].isdigit() == False):
                    return render_template("Admins/add_admin.html", form=form, warning=4)
                else:
                    hashed = hashlib.sha3_256(form.password.data.encode())
                    admin = Admin(form.first_name.data, form.last_name.data, form.email.data, form.phone.data, hashed.hexdigest(),0)
                    admin.set_cid(str(uuid4()))
                    admin_dict[admin.get_email()] = admin
                    db["Admin"] = admin_dict
                    db.close()
                    return redirect(url_for("admin_manage"))
        else:
            pass

    return render_template("Admins/add_admin.html", form=form, warning=0)


@app.route("/admin_wallet", methods=["POST", "GET"])
def admin_wallet():
    db = shelve.open("customer.db", "c")
    admins_dict = db["Admin"]
    admin = admins_dict.get(session["user"])
    form1 = WithdrawForm(request.form)
    db.close()
    return render_template("Admins/admin_wallet.html", form1=form1, user=admin)


@app.route("/admin_customer_detail/<email>")
def customer_detail(email):
    db = shelve.open("customer.db", "r")
    customer_dict = db["Customer"]
    cust = customer_dict.get(email)
    return render_template("Admins/admin_customer_detail.html", cust=cust)


@app.route("/admin_merchant_detail/<email>")
def merchant_detail(email):
    db = shelve.open("customer.db", "r")
    merchant_dict = db["Merchant"]
    merchant = merchant_dict.get(email)
    products_dict = merchant.get_products()
    product_list = []
    for key in products_dict:
        product = products_dict.get(key)
        product_list.append(product)
    return render_template("Admins/admin_merchant_detail.html", merchant=merchant, product_list=product_list)


@app.route('/admin_view_product/<email>/<product>', methods=['POST', "GET"])
def admin_view_product(email, product):
    db = shelve.open('customer.db', 'r')
    musers_dict = db['Merchant']
    db.close()
    merchant = musers_dict.get(email)
    products_dict = merchant.get_products()
    product_detail = products_dict.get(product)
    rating = 0
    for i in product_detail.get_review():
        rating += int(i.get_rating())
    if len(product_detail.get_review()) == 0:
        avg = 0
    else:
        avg = rating / len(product_detail.get_review())
    return render_template("Admins/admin_merchant_product.html", merchant=merchant, product=product_detail, avg=avg)


@app.route("/admin_customer_delete/<id>")
def delete_cust(id):
    db = shelve.open("customer.db", "c")
    customer_dict = db["Customer"]
    customer_dict.pop(id)
    db["Customer"] = customer_dict
    db.close()
    return redirect(url_for("admin_customer"))


@app.route("/admin_merchant_delete/<id>")
def delete_merc(id):
    db = shelve.open("customer.db", "c")
    merchant_dict = db["Merchant"]
    merchant_dict.pop(id)
    db["Merchant"] = merchant_dict
    db.close()
    return redirect(url_for("admin_merchant"))


@app.route("/admin/WebRewardsForm", methods=['GET', 'POST'])
def create_web_rewards_data():
    create_Website_Rewards = CreateWebRewards(request.form)
    if request.method == 'POST' and create_Website_Rewards.validate():
        CWR_dict = {}
        db = shelve.open('WebReward.db', 'c')

        try:
            if 'WebRewards' in db:
                CWR_dict = db['WebRewards']
            else:
                db['WebRewards'] = CWR_dict
        except:
            print("Error")

        WebReward = wr.website_rwds(create_Website_Rewards.rank.data,
                                    create_Website_Rewards.web_reward_type.data,
                                    create_Website_Rewards.web_reward_name.data,
                                    create_Website_Rewards.amt_rewarded.data,
                                    create_Website_Rewards.points.data,
                                    create_Website_Rewards.start_date.data,
                                    create_Website_Rewards.end_date.data,
                                    create_Website_Rewards.reward_description.data)

        CWR_dict[WebReward.get_count()] = WebReward
        db['WebRewards'] = CWR_dict
        db.close()
        return redirect(url_for('web_rewards_data'))

    return render_template('Admins/create_web_rewards.html', form=create_Website_Rewards)


@app.route("/admin/WebRewardsData")
def web_rewards_data():
    CWR_dict = {}
    db = shelve.open('WebReward.db', 'c')
    CWR_dict = db['WebRewards']
    db.close()

    list_Web_rewards = []
    for key in CWR_dict:
        web_reward = CWR_dict.get(key)
        list_Web_rewards.append(web_reward)

    return render_template('Admins/WebRewards_data.html', count=len(list_Web_rewards),
                           list_Web_rewards=list_Web_rewards)


@app.route('/admin/delete_web_rewards', methods=['POST'])
def delete_web_rewards():
    if request.method == "POST":
        CWR_dict = {}
        db = shelve.open('WebReward.db', 'w')
        CWR_dict = db['WebRewards']

        web_rwds_count = request.get_json()
        for i in web_rwds_count:
            CWR_dict.pop(i)

        db['WebRewards'] = CWR_dict
        db.close()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/admin/CampaignForm", methods=['GET', 'POST'])
def create_campaign():
    create_Campaign = CampaignCreate(request.form)
    if request.method == "POST" and create_Campaign.validate():
        CD_dict = {}
        db = shelve.open('Campaign.db', 'c')

        try:
            if 'Campaign' in db:
                CD_dict = db['Campaign']
            else:
                db['Campaign'] = CD_dict
        except IOError:
            print("Error")

        Campaign = wc.website_camp(create_Campaign.campaign_name.data,
                                   create_Campaign.start_date.data,
                                   create_Campaign.end_date.data,
                                   create_Campaign.base.data)

        CD_dict[Campaign.get_campaign_id()] = Campaign
        db['Campaign'] = CD_dict
        db.close()
        return redirect(url_for('campaign_data'))

    return render_template('Admins/create_campaign.html', form=create_Campaign)


@app.route("/admin/CampaignData")
def campaign_data():
    CD_dict = {}
    db = shelve.open('Campaign.db', 'c')
    try:
        if 'Campaign' in db:
            CD_dict = db['Campaign']
        else:
            db['Campaign'] = CD_dict
    except:
        db['Campaign'] = {}

    CD_dict = db['Campaign']
    db.close()

    list_campaign = []
    for key in CD_dict:
        campaign_things = CD_dict.get(key)
        list_campaign.append(campaign_things)

    current_time = date.today()

    return render_template('Admins/campaign_data.html', count_camp=len(list_campaign), list_campaign=list_campaign,
                           date=current_time)


@app.route('/admin/delete_campaign', methods=['POST'])
def delete_campaign():
    if request.method == "POST":
        CD_dict = {}
        db = shelve.open('Campaign.db', 'w')
        CD_dict = db['Campaign']
        camp_count = request.get_json()
        print(camp_count)
        for i in camp_count:
            CD_dict.pop(i)

        db['Campaign'] = CD_dict
        db.close()

        db = shelve.open('CampaignVchers.db', 'w')
        cvd_dict = db['CampaignVchers']

        vc_in_camp = []
        for i in cvd_dict:
            if cvd_dict[i].get_campaign_origin() in camp_count:
                vc_in_camp.append(i)

        for key in vc_in_camp:
            cvd_dict.pop(key)

        db['CampaignVchers'] = cvd_dict
        db.close()

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/admin/CampaignVouchersForm", methods=['GET', 'POST'])
def create_campaign_vouchers():
    Create_Campaign_vouchers = CreateCampaignVouchers(request.form)

    if request.method == "POST" and Create_Campaign_vouchers.validate():
        cvd_dict = {}
        db = shelve.open('CampaignVchers.db', 'c')

        try:
            if 'CampaignVchers' in db:
                cvd_dict = db['CampaignVchers']
            else:
                db['CampaignVchers'] = cvd_dict
        except IOError:
            print("Error")

        Campaign_voucher_price = cv.campaign_vouchers_price(Create_Campaign_vouchers.discount_amt.data,
                                                            Create_Campaign_vouchers.minimum_spendage.data,
                                                            request.form.get("campaign_origin"))

        cvd_dict[Campaign_voucher_price.get_voucher_id()] = Campaign_voucher_price
        db['CampaignVchers'] = cvd_dict

        db.close()

        return redirect(url_for('campaign_vouchers_data'))

    if request.method == "GET":
        CD_dict = {}
        db = shelve.open('Campaign.db', 'r')
        CD_dict = db['Campaign']
        db.close()

        list_campaign = CD_dict.values()
        current_time = date.today()
        return render_template('Admins/create_campaign_vouchers.html', form=Create_Campaign_vouchers,
                               list_campaign=list_campaign, date=current_time)


@app.route("/admin/CampaignVouchersForm2", methods=['GET', 'POST'])
def create_campaign_vouchers2():
    Create_Campaign_vouchers2 = CreateCampaignVouchers2(request.form)
    if request.method == "POST" and Create_Campaign_vouchers2.validate():
        cvd_dict = {}
        db = shelve.open('CampaignVchers.db', 'c')

        try:
            if 'CampaignVchers' in db:
                cvd_dict = db['CampaignVchers']
            else:
                db['CampaignVchers'] = cvd_dict
        except IOError:
            print("Error")

        Campaign_voucher_percent = cv.campaign_vouchers_percentage(Create_Campaign_vouchers2.discount_amt.data,
                                                                   Create_Campaign_vouchers2.minimum_spendage.data,
                                                                   request.form.get("campaign_origin"))

        cvd_dict[Campaign_voucher_percent.get_voucher_id()] = Campaign_voucher_percent
        db['CampaignVchers'] = cvd_dict
        db.close()
        return redirect(url_for('campaign_vouchers_data'))

    if request.method == "GET":
        CD_dict = {}
        db = shelve.open('Campaign.db', 'r')
        CD_dict = db['Campaign']
        db.close()

        list_campaign = CD_dict.values()

        return render_template('Admins/create_campaign_vouchers2.html', form=Create_Campaign_vouchers2,
                               list_campaign=list_campaign)


@app.route("/admin/CampaignVouchersData")
def campaign_vouchers_data():
    cvd_dict = {}
    db = shelve.open('CampaignVchers.db', 'c')
    try:
        if 'CampaignVchers' in db:
            cvd_dict = db['CampaignVchers']
        else:
            db['CampaignVchers'] = cvd_dict
    except:
        db["CampaignVouchers"] = {}

    cvd_dict = db['CampaignVchers']
    db.close()

    CD_dict = {}
    db = shelve.open('Campaign.db', 'c')
    try:
        if 'Campaign' in db:
            CD_dict = db['Campaign']
        else:
            db['Campaign'] = CD_dict
    except:
        db["Campaign"] = {}

    CD_dict = db['Campaign']
    db.close()

    list_campaign_vouchers = []

    for key in cvd_dict:
        campaign_voucher_things = cvd_dict.get(key)
        list_campaign_vouchers.append(campaign_voucher_things)

    current_time = date.today()
    # print(list_campaign_vouchers)
    # print(cvd_dict)
    return render_template('Admins/campaign_vouchers_data.html', count_camp_vchers=len(list_campaign_vouchers),
                           list_campaign_vouchers=list_campaign_vouchers,
                           campaign_table=CD_dict, date=current_time)


@app.route("/view_admin_transactions")
def view_admin_transactions():
    db = shelve.open("customer.db", "r")
    admin = db["Admin"].get(session["user"])
    db.close()
    transactions_list = admin.get_transactions()
    return render_template("Admins/view_admin_transactions.html", transaction_list=transactions_list)


@app.route('/admin/delete_campaign_vouchers', methods=['POST'])
def delete_campaign_vouchers():
    if request.method == "POST":
        cvd_dict = {}
        db = shelve.open('CampaignVchers.db', 'w')
        cvd_dict = db['CampaignVchers']

        camp_vouchers_count = request.get_json()
        for i in camp_vouchers_count:
            cvd_dict.pop(i)

        db['CampaignVchers'] = cvd_dict
        db.close()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route("/merchant_store/<m_email>", methods=["GET", "POST"])
def page_merchant(m_email):
    product_list_show_all = []
    merchant_num = None
    db = shelve.open('customer.db', 'r')
    muser_dict = db["Merchant"]
    merchant = muser_dict.get(m_email)
    db.close()
    print(m_email)
    for i in muser_dict:
        if i == m_email:
            merchant = muser_dict.get(m_email)
            products_dict = merchant.get_products()
            merchant_number = merchant.get_phone()
            merchant_num = merchant_number
            for key in products_dict:
                product = products_dict.get(key)
                product_list_show_all.append(product)
    rate = 0
    star = 0
    merchant = muser_dict.get(m_email)
    product = merchant.get_products()
    for x in product:
        rate += len(product[x].get_review())
        for review in product[x].get_review():
            star += int(review.get_rating())
    if rate != 0:
        star = star / rate
    star = round(star)
    print(merchant_num)
    datetoday = date.today()
    date_limit = timedelta(days=30)

    #Aaralyn Part
    shoppingCarts = {}
    shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
    try:
        if "shoppingCart" in shoppingCartDB:  # is key exist?
            shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
        else:
            print("Shopping carts has an error.")  # start with empty
    except:
        print("Error in retrieving shopVouchers from vouchers.db.")

    userShoppingCart = None  # retrieves the shopping cart object
    try:
        if session['user'] in shoppingCarts:
            userShoppingCart = shoppingCarts[session['user']]
        else:
            print("Can't retrieve the user's shopping cart.")
    except:
        print("Error occured in dictionary.")
    shoppingCartDB.close()

    noOfItems=0
    productList=[]
    totalPrice=0
    if userShoppingCart != None:
        merchant_dict=userShoppingCart.get_merchants()
        for merchantEmail in merchant_dict:
            merchantObject=merchant_dict[merchantEmail]
            product_list=merchantObject.get_products()
            for product in product_list:
                productList.append(product)
                noOfItems+=1
                totalPrice += round(product.get_totalPrice(), 2)

       #Getting merchant vouchers
    voucher_list=[]
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
        if m_email in shopVoucher_dict:
            merchantShopVoucher_dict = shopVoucher_dict[m_email]
        else:
            shopVoucher_dict[m_email] = merchantShopVoucher_dict
    except:
        print("Error occured in shop voucher dictionary.")
    fixeddb.close()

    for key in merchantShopVoucher_dict:
        voucher=merchantShopVoucher_dict.get(key)
        if voucher.get_status() == "Ongoing" and voucher.get_usageQuantity()>0:
            voucher_list.append(voucher)

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
        if m_email in shopVoucher_dict:
            merchantShopVoucher_dict = shopVoucher_dict[m_email]
        else:
            shopVoucher_dict[m_email] = merchantShopVoucher_dict
    except:
        print("Error occured in shop voucher dictionary.")

    for key in merchantShopVoucher_dict:
        voucher = merchantShopVoucher_dict.get(key)
        if voucher.get_status() == "Ongoing" and voucher.get_usageQuantity()>0:
            voucher_list.append(voucher)
    db.close()

    return render_template("common/merchant_products.html", userShoppingCart=userShoppingCart,noOfItems=noOfItems, merchant=merchant,
                           productList=productList,totalPrice=totalPrice, m_email=m_email, star=star, rate=rate,
                           datetoday=datetoday, date_limit=date_limit, merchant_num=merchant_num, product_list_show_all=product_list_show_all)


@app.route("/merchant_store_all/<m_email>", methods=["GET", "POST"])
def page_merchant2(m_email):
    product_list_show_all = []
    merchant_num = None
    db = shelve.open('customer.db', 'r')
    muser_dict = db["Merchant"]
    db.close()
    print(m_email)
    for i in muser_dict:
        if i == m_email:
            merchant = muser_dict.get(m_email)
            products_dict = merchant.get_products()
            for key in products_dict:
                product = products_dict.get(key)
                product_list_show_all.append(product)

    #Aaralyn Part
    shoppingCarts = {}
    shoppingCartDB = shelve.open('shoppingCartDB.db', 'c')
    try:
        if "shoppingCart" in shoppingCartDB:  # is key exist?
            shoppingCarts = shoppingCartDB["shoppingCart"]  # retrieve data
        else:
            print("Shopping carts has an error.")  # start with empty
    except:
        print("Error in retrieving shopVouchers from vouchers.db.")

    userShoppingCart = None  # retrieves the shopping cart object
    try:
        if session['user'] in shoppingCarts:
            userShoppingCart = shoppingCarts[session['user']]
        else:
            print("Can't retrieve the user's shopping cart.")
    except:
        print("Error occured in dictionary.")
    shoppingCartDB.close()

    noOfItems=0
    productList=[]
    totalPrice=0
    if userShoppingCart != None:
        merchant_dict=userShoppingCart.get_merchants()
        for merchantEmail in merchant_dict:
            merchantObject=merchant_dict[merchantEmail]
            product_list=merchantObject.get_products()
            for product in product_list:
                productList.append(product)
                noOfItems+=1
                totalPrice += round(product.get_totalPrice(), 2)

    return render_template("common/merchant_products2.html", product_list_show_all=product_list_show_all, userShoppingCart=userShoppingCart,noOfItems=noOfItems,
                           productList=productList, totalPrice=totalPrice, merchant_num=merchant_num)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
