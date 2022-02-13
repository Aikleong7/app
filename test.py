# from flask import Flask, render_template, request, redirect, url_for, session
import shelve
# from User import *
# from Forms import *
# import hashlib
# from uuid import uuid4
# from datetime import datetime
# import json
# from merchant_wallet import *
# from td import *
# from sub_category import *
# from products import *
#
# app = Flask(__name__)
# app.secret_key = "hello"
#
#
# @app.route("/")
# def home():
#     return render_template("partials/_merchant_side_navbar.html")
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
# print(x

# class Review:
#     def __init__(self, customer, product, review):
#         self.__customer = customer
#         self.__product = product
#         self.__review = review
#
#     def set_customer(self, customer):
#         self.__customer = customer
#
#     def set_product(self, product):
#         self.__product = product
#
#     def set_review(self, review):
#         self.__review = review
#
#     def get_customer(self):
#         return self.__customer
#
#     def get_product(self):
#         return self.__product
#
#     def get_review(self):
#         return self.__review
# db = shelve.open("purchaseHistory.db")
# detail = db["purchaseHistory"].get("aikleong0713@gmail.com")
# print(detail)
# history = detail.get_purchaseHistory()
# print(history)
# info = history.get(1).get_paymentDetails()
# print(info.get_subTotal())
# print(info.get_dateOfPayment())

#
# x = "111!"
# if (x.isalpha() == False) and (x.isdigit()== False):
#     print("yes")


# @app.route("/customer_forget_password", methods=["GET", "POST"])
# def customer_forget():
#     form = Forget(request.form)
#     notice = "A forget password email have been sent to your email"
#     if request.method == "POST":
#         db = shelve.open("customer.db", 'r')
#         customer_dict = db["Customer"]
#         customer = customer_dict.get(form.email.data)
#         email = customer.get_email()
#         token = customer.get_cid()
#         message = "We received an inquire to reset your password, if is not you, ignore this email. key in your token:{} and new password with the following link to reset your password: http://127.0.0.1:5000/customer_forget_token".format(
#             token)
#         with app.app_context():
#             msg = Message(subject="Reset Password", sender="SingtopiaSG@gmail.com", recipients=[email], body=message)
#             mail.send(msg)
#             return render_template("Customer/customer_forget.html", form=form, notice=notice)
#     return render_template("Customer/customer_forget.html", form=form)
#
#
# @app.route("/customer_forget_token", methods=["GET", "POST"])
# def customer_token():
#     form = ForgetAcc(request.form)
#     db = shelve.open("customer.db", "r")
#     customer_dict = db["Customer"]
#     for i in customer_dict:
#         print(customer_dict[i].get_cid())
#         if customer_dict[i].get_cid() == form.token.data:
#             email = customer_dict[i].get_email()
#             return redirect(url_for("customer_forget_2", id=email))
#     return render_template("Customer/customer_token.html", form=form)
#
# @app.route("/customer_forget_password2", methods=["POST", "GET"])
# def customer_forget_2():
#     form = CreateAccountForm2(request.form)
#     email = request.args.get('id')
#     db = shelve.open("customer.db", 'r')
#     customer_dict = db["Customer"]
#     customer = customer_dict.get(email)
#     if request.method == "POST":
#         if str(customer.get_security_qn1()) == str(form.security_qn1.data) and str(customer.get_security_qn2()) == str(
#                 form.security_qn2.data) and str(customer.get_security_qn3()) == str(form.security_qn3.data):
#             return redirect(url_for("customer_new_password", id=email))
#     return render_template("Customer/customer_forget_password2.html", form=form)
#
# @app.route("/customer_new_password", methods=["GET", "POST"])
# def customer_new_password():
#     form = New_password(request.form)
#     email = request.args.get("id")
#     if request.method == "POST":
#         db = shelve.open("customer.db", 'c')
#         customer_dict = db["Customer"]
#         customer = customer_dict.get(email)
#         hashed = hashlib.sha3_256(form.password.data.encode())
#         customer.set_password(hashed.hexdigest())
#         date = datetime.now()
#         customer.set_password_change([date.strftime("%Y"), date.strftime("%b"), date.strftime("%d")])
#         customer.set_cid(str(uuid4()))
#         db["Customer"] = customer_dict
#         db.close()
#         return redirect(url_for("login"))
#     return render_template("Customer/customer_new_password.html", form=form)
# list = [1,2,3,5]
# a = [3,5,12]
# l = []
# for x in list:
#     if x not in a:
#         l.append(x)
# print(l)
#
# x = {}
# x["abc"] = 12
# print(x)

