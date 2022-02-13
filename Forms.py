from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, IntegerField, PasswordField, \
    BooleanField, ValidationError, FileField, DecimalField, IntegerRangeField
from wtforms.fields import EmailField, DateField, FloatField
from wtforms.validators import EqualTo
from datetime import date
from wtforms.widgets import PasswordInput


# CUSTOMER
class Reply(Form):
    subject = StringField("Subject", [validators.data_required()])
    message = TextAreaField("Message", [validators.data_required()])


class ForgetAcc(Form):
    token = StringField("Token", [validators.data_required()])


class CreateAccountForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField("Email", [validators.Email(), validators.DataRequired()])
    gender = RadioField('Gender', [validators.DataRequired()], choices=[("Female", "Female"), ("Male", "Male")],
                        default="")
    phone = IntegerField("Phone", [validators.Length(min=1, max=8), validators.DataRequired()],
                         render_kw={"placeholder": "+65"})
    password = PasswordField("Password", validators=[validators.Length(min=1, max=10), validators.DataRequired(),
                                                     EqualTo('password_confirm', message="Password not match")],
                             id="password")
    password_confirm = PasswordField("Confirm", [validators.Length(min=1, max=10), validators.DataRequired()],
                                     id="password_confirm")
    show_password = BooleanField("Show password")


class CreateAccountForm1(Form):
    address = StringField("Address", [validators.Optional()])
    city = StringField("City", [validators.Optional()])
    zipcode = IntegerField("Zip code", [validators.Optional()])
    credit_card = StringField("Credit/Debit Card", [validators.Length(min=16, max=16), validators.Optional()])
    csv = PasswordField("CSV", [validators.Length(min=3, max=3), validators.Optional()], id="CSV")
    show_csv = BooleanField("Show CSV")


class CreateAccountForm2(Form):
    security_qn1 = StringField("Favourite Colour", [validators.DataRequired()])
    security_qn2 = StringField("Favourite Pet", [validators.DataRequired()])
    security_qn3 = StringField("Best Friend Name", [validators.DataRequired()])


class LoginForm(Form):
    email = EmailField("Email", [validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])


class NewCreditCard(Form):
    newcredit_card = StringField("Credit/Debit Card", [validators.Length(min=16, max=16), validators.DataRequired()])
    newcsv = PasswordField("CSV", [validators.Length(min=3, max=3), validators.DataRequired()], id="CSV")
    set_default = BooleanField("Set as Default")


class Feedback(Form):
    Name = StringField("Name", [validators.DataRequired()])
    Email = EmailField("Email", [validators.data_required()])
    Message = TextAreaField("Message", [validators.data_required()])


class Editname(Form):
    first_name = StringField("First Name", [validators.data_required()])
    last_name = StringField("Last Name", [validators.data_required()])


class Editbirthday(Form):
    birthday = DateField('Birthday', [validators.data_required()], format='%Y-%m-%d')


class Editgender(Form):
    gender = RadioField("Gender", [validators.data_required()], choices=[("Female", "Female"), ("Male", "Male")],
                        default="")


class Editemail(Form):
    email = EmailField("Email", [validators.data_required()])


class Editphone(Form):
    phone = StringField("Phone", [validators.data_required(), validators.length(min=8, max=8)])


class Editaddress(Form):
    address = StringField("Address", [validators.data_required()])
    zipcode = IntegerField("Zipcode", [validators.data_required()])
    city = StringField("City", [validators.data_required()])


class Editpassword(Form):
    current_password = PasswordField("Current Password", [validators.data_required()])
    new_password = PasswordField("New Password", [validators.data_required()])
    confirm_new_password = PasswordField("Confirm Password", [validators.data_required()])


class Profile(Form):
    image = FileField("Profile Picture", [validators.data_required()])
    base = StringField("")


class Forget(Form):
    email = EmailField("Email", [validators.data_required()])


class New_password(Form):
    password = PasswordField("New Password", [validators.data_required()])


class Review_form(Form):
    rating = StringField()
    review = TextAreaField("Review", [validators.data_required()])


class GetQuantity(Form):
    quantity = IntegerField("", [validators.DataRequired(), validators.NumberRange(min=1)], default=1)


#   MERCHANT
class CreateMerchantShopVoucherFixedAmt(Form):
    name = StringField('', [validators.Length(min=1, max=50), validators.DataRequired()],
                       render_kw={'style': 'width: 80%;margin-bottom:20px;'})
    startingDate = DateField('', format='%Y-%m-%d', validators=[validators.DataRequired()],
                             render_kw={'style': 'width: 22%;margin-bottom:20px;'})
    endingDate = DateField('', format='%Y-%m-%d', validators=[validators.DataRequired()],
                           render_kw={'style': 'width: 22%;margin-bottom:20px;'})
    minSpend = FloatField("", [validators.DataRequired(), validators.NumberRange(min=0)])
    # discountType=RadioField('', choices=[('fixedAmt', 'Fixed Amount'), ('percentage', 'Percentage')], default='fixedAmt')
    usageQuantity = IntegerField("", [validators.DataRequired(), validators.NumberRange(min=0)])
    # percentageOff=IntegerField("",[validators.Optional(),validators.NumberRange(min=3)],render_kw={"placeholder":"minimum is 3% off"},default=3)
    # maxCappedPriceType=RadioField('', choices=[('NL', 'No Limit'), ('SA', 'Set Amount')], default='NL')
    # CappedPrice=IntegerField("",[ validators.NumberRange(min=0)],default=0)
    fixedAmtOff = FloatField("", [validators.DataRequired(), validators.NumberRange(min=0)], default=0)
    # def validate_end_date(self, endingDate):
    #     if endingDate.data < self.startingDate.data:
    #         raise ValidationError("End date must not be earlier than start date.")
    #
    # def validate_start_date(self, startingDate):
    #     if startingDate.data < date.today():
    #         raise ValidationError("Start date must not be in the past")


class CreateMerchantShopVoucherPercentage(Form):
    name = StringField('', [validators.Length(min=1, max=50), validators.DataRequired()],
                       render_kw={'style': 'width: 80%; margin-left:20px;margin-bottom:20px;'})
    startingDate = DateField('', format='%Y-%m-%d', render_kw={'style': 'width: 22%;margin-bottom:20px;'})
    endingDate = DateField('', format='%Y-%m-%d', render_kw={'style': 'width: 22%;margin-bottom:20px;'})
    minSpend = FloatField("", [validators.DataRequired(), validators.NumberRange(min=0)])
    usageQuantity = IntegerField("", [validators.DataRequired(), validators.NumberRange(min=0)])
    percentageOff = IntegerField("", [validators.DataRequired(), validators.NumberRange(min=3)],
                                 render_kw={"placeholder": "minimum is 3% off"})
    # maxCappedPriceType=RadioField('',[validators.DataRequired()], choices=[('NL', 'No Limit'), ('SA', 'Set Amount')], default='NL')
    CappedPrice = FloatField("", [validators.NumberRange(min=0)], default=0)
    # can do sth like if capped price is still 0 then set it no limit automatically (since got no validation)


class CreateProductDiscount(Form):
    name = StringField('', [validators.Length(min=1, max=50), validators.DataRequired()])
    startingDate = DateField('', format='%Y-%m-%d')
    endingDate = DateField('', format='%Y-%m-%d')

    # def validate_end_date(form, endingDate):
    #     if endingDate.data < form.startingDate.data:
    #         raise ValidationError("End date must not be earlier than start date.")
    #
    # def validate_start_date(form, startingDate):
    #     if startingDate.data < date.today():
    #         raise ValidationError("Start date must not be in the past")


class CreateProductDiscount_1(Form):
    discount = IntegerField("", [validators.DataRequired(), validators.NumberRange(min=3)],render_kw={'style': 'width: 50%'})
    purchaseLimit = IntegerField("", [validators.optional(), validators.NumberRange(min=0)], default=0)

class TdForm(Form):
    td_item = StringField('A New Task!', [validators.DataRequired()])


class CreateProductForm(Form):
    product_cat = SelectField(' ', [validators.DataRequired()],
                              choices=[('', ''), ('Clothing', 'Clothing'),
                                       ('Food&Beverage', 'Food & Beverage'),
                                       ('Accessories', 'Accessories'),
                                       ('Electronics', 'Electronics'),
                                       ('Shoes', 'Shoes'),
                                       ('Home&Living', 'Home & Living'),
                                       ('Sports&Outdoor', 'Sports & Outdoor'),
                                       ('Health&Wellness', 'Health & Wellness'),
                                       ('PetNecessities', 'Pet Necessities')], default='')
    product_name = StringField('', [validators.Length(min=1, max=25),validators.DataRequired()])
    product_price = FloatField('', [validators.DataRequired()])
    product_desc = TextAreaField('', [validators.optional()])
    product_sub_cat = SelectField('', [validators.optional()],
                                  choices=["None", "Clothing Sizes", "Shoe Sizes"])
    product_img = FileField('', [validators.optional()])
    base = StringField('')


class CreateCategoryForm(Form):
    category = StringField("", [validators.Length(min=2, max=200), validators.DataRequired()])


class WithdrawForm(Form):
    withdraw_amount = FloatField("", [validators.DataRequired()])


class TopUpForm(Form):
    top_up_amt = FloatField("", [validators.DataRequired()])


class CreateMerchantForm(Form):
    first_name = StringField("", [validators.DataRequired()])
    last_name = StringField("", [validators.DataRequired()])
    phone = StringField("", [validators.DataRequired()])
    email = EmailField("", [validators.DataRequired()])
    password = PasswordField("", [validators.DataRequired()])


class LoginMerchantForm(Form):
    email = EmailField("", [validators.DataRequired()])
    password = PasswordField("", [validators.DataRequired()])


class InventoryForm(Form):
    inventory_name = StringField('', [validators.DataRequired()])
    inventory_category = SelectField(' ', [validators.DataRequired()],
                                     choices=[('', ''), ('Clothing', 'Clothing'),
                                              ('Food&Beverage', 'Food & Beverage'),
                                              ('Accessories', 'Accessories'),
                                              ('Electronics', 'Electronics'),
                                              ('Shoes', 'Shoes'),
                                              ('Home&Living', 'Home & Living'),
                                              ('Sports&Outdoor', 'Sports & Outdoor'),
                                              ('Health&Wellness', 'Health & Wellness'),
                                              ('PetNecessities', 'Pet Necessities')], default='')
    inventory_price = FloatField(" ", [validators.DataRequired()])


class SizeForm(Form):
    shirt_size = StringField("", [validators.optional()])
    size_qty = IntegerField("", [validators.DataRequired()])
    total_cost = IntegerField("", [validators.Optional()])


class QtyForm(Form):
    quantity_to_add = IntegerField("", [validators.DataRequired()])
    total_cost_nosize = IntegerField("", [validators.Optional()])


class Merchant_create(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField("Email", [validators.Email(), validators.DataRequired()])
    phone = IntegerField("Phone", [validators.Length(min=1, max=8), validators.DataRequired()],
                         render_kw={"placeholder": "+65"})
    password = PasswordField("Password", [validators.Length(min=1, max=10), validators.DataRequired(),
                                          validators.EqualTo('password_confirm', message="Password not match")],
                             id="password")
    password_confirm = PasswordField("Confirm", [validators.Length(min=1, max=10), validators.DataRequired()],
                                     id="password_confirm")
    show_password = BooleanField("Show password")


class edit_address(Form):
    address = StringField("Address", [validators.data_required()])
    unit = StringField("Unit-No", [validators.data_required()])
    postal = IntegerField("Postal Code", [validators.Length(min=6, max=6), validators.data_required()])


class Add_supplier(Form):
    company = StringField("Company", [validators.data_required()])
    product = SelectField("Product", [validators.data_required()], choices=[])
    email = EmailField("Email", [validators.data_required()])
    phone = IntegerField("Contact Number", [validators.data_required()])


class Withdraw(Form):
    withdraw_amount = IntegerField("Amount to withdraw")


class EditMerchant(Form):
    email = EmailField("Email", [validators.data_required()])
    phone = IntegerField("Contact Number", [validators.data_required()])


class Edit_shop_profile(Form):
    image = FileField("Store Profile Picture")
    base = StringField("")
    phone = IntegerField("Contact Number", [validators.data_required()])
    email = EmailField("Email", [validators.data_required()])
    shop_description = TextAreaField("Shop Description", [validators.data_required()])
    address = StringField("Store Location", [validators.data_required()])
    unit = StringField("Unit-No", [validators.data_required()])
    postal = IntegerField("Postal Code", [validators.Length(min=6, max=6), validators.data_required()])


class Supplier_quantity(Form):
    quantity = IntegerField("Quantity")


# ADMIN

class Add_admin(Form):
    first_name = StringField("First Name", [validators.data_required()])
    last_name = StringField("Last Name", [validators.data_required()])
    phone = StringField("Phone", [validators.data_required()])
    email = EmailField("Email", [validators.data_required()])
    password = PasswordField("Password", [validators.Length(min=1, max=10), validators.DataRequired(),
                                          EqualTo('password_confirm', message="Password not match")], id="password")
    password_confirm = PasswordField("Confirm", [validators.Length(min=1, max=10), validators.DataRequired()],
                                     id="password_confirm")
    show_password = BooleanField("Show password")


class CreateWebRewards(Form):
    rank = SelectField(' ', [validators.DataRequired()],
                       choices=[('', ''), ('Iron', 'Iron'),
                                ('Bronze', 'Bronze'),
                                ('Silver', 'Silver'),
                                ('Gold', 'Gold'),
                                ('Platinum', 'Platinum'),
                                ('Diamond', 'Diamond')], default='')

    web_reward_type = SelectField(' ', [validators.DataRequired()], choices=[('', ''), ('Vouchers', 'Vouchers'),
                                                                             ('Free shipping', ' Free shipping')])

    web_reward_name = StringField(' ', [validators.Length(min=10, max=200), validators.DataRequired()])
    amt_rewarded = IntegerField(' ', [validators.DataRequired()])
    points = IntegerRangeField(' ')

    start_date = DateField(' ', format='%Y-%m-%d', validators=[validators.DataRequired()])
    end_date = DateField(' ', format='%Y-%m-%d', validators=[validators.DataRequired()])

    reward_description = TextAreaField(' ', [validators.DataRequired(), validators.Length(min=10, max=70)])

    def validate_end_date(form, end_date):
        if end_date.data < form.start_date.data:
            raise ValidationError("End date must not be earlier than start date.")

    def validate_start_date(form, start_date):
        if start_date.data < date.today():
            raise ValidationError("Start date must not be in the past")


class CampaignCreate(Form):
    campaign_name = StringField(' ', [validators.Length(min=1, max=40), validators.DataRequired()])

    start_date = DateField(' ', format='%Y-%m-%d', validators=[validators.DataRequired()])
    end_date = DateField(' ', format='%Y-%m-%d', validators=[validators.DataRequired()])

    camp_img = FileField('', [validators.DataRequired()])
    base = StringField('')

    def validate_end_date(form, end_date):
        if end_date.data < form.start_date.data:
            raise ValidationError("End date must not be earlier than start date.")

    def validate_start_date(form, start_date):
        if start_date.data < date.today():
            raise ValidationError("Start date must not be in the past")


class CreateCampaignVouchers(Form):
    discount_amt = IntegerField(' ', [validators.DataRequired()])
    minimum_spendage = IntegerField(' ', [validators.DataRequired()])

    # def validate_minimum_spendage(form):
    #     if form.minimum_spendage <= form.discount_amt:
    #         raise ValidationError("minimum spendage should be higher than discount amount")


class CreateCampaignVouchers2(Form):
    discount_amt = DecimalField(' ', [validators.DataRequired()], places=2)
    minimum_spendage = IntegerField(' ', [validators.DataRequired()])

