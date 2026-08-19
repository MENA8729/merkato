from flask_wtf import FlaskForm
from wtforms import (Form, StringField, SelectField,
                     DecimalField, SubmitField, FieldList, FormField,PasswordField,BooleanField)
from wtforms.fields.numeric import FloatField
from wtforms.validators import DataRequired, Email, Length, EqualTo,NumberRange

class StockForm(FlaskForm):
    class Meta:
        csrf = False

    stock_name = StringField("Stock Name*", validators=[DataRequired()])
    stock_code = StringField("Stock Code")
    measurement = SelectField(
        "Measurement*",
        choices=[
            ("", "Choose measurement"),
            ("Piece", "Piece"),
            ("Liter", "Liter"),
            ("Kilogram", "Kilogram"),
            ("Gram", "Gram"),
            ("Package", "Package"),
            ("Box", "Box"),
            ("Bottle", "Bottle"),
            ("Dozen", "Dozen"),
            ("Meter", "Meter"),
            ("Set", "Set"),
        ],
        validators=[DataRequired()]
    )
    quantity = DecimalField("Quantity", validators=[DataRequired(), NumberRange(min=0)])
    unit_price = DecimalField("Unit Price", validators=[DataRequired(), NumberRange(min=0)])

class InventoryForm(FlaskForm):
    stocks = FieldList(FormField(StockForm), min_entries=1)
    submit = SubmitField("Save Stock")


class PurchaseForm(Form):          # plain Form — sub-form, lives inside PurchaseListForm.purchase
    product = SelectField("Product", coerce=int, validators=[DataRequired()])
    supplier = SelectField("Supplier", coerce=int, validators=[DataRequired()])
    quantity = DecimalField("Quantity", validators=[DataRequired(), NumberRange(min=0)])
    unit_price = DecimalField("Purchase Price", validators=[DataRequired(), NumberRange(min=0)])
    payment = DecimalField("Current Payment", validators=[NumberRange(min=0)], default=0)
    debt = FloatField()

class PurchaseListForm(FlaskForm):
    purchase = FieldList(FormField(PurchaseForm), min_entries=1)
    submit = SubmitField("Buy Stock")

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, Optional, Email, Length


class SupplierEntryForm(FlaskForm):
    # This is a "sub-form" — one single supplier entry.
    # We disable CSRF here because the CSRF token only needs to
    # exist once, on the parent form.
    class Meta:
        csrf = False

    name = StringField(
        "Supplier Name",
        validators=[DataRequired(message="Supplier name is required.")]
    )
    phone = StringField(
        "Phone Number",
        validators=[Optional(), Length(max=20)]
    )
    email = StringField(
        "Email Address",
        validators=[Optional(), Email(message="Enter a valid email address.")]
    )
    balance_owed = FloatField(
        "Balance Owed",
        validators=[Optional()],
        default=0.0
    )


class SupplierForm(FlaskForm):
    # The parent form: holds a *list* of SupplierEntryForm,
    # one per "Add Another Supplier" click.
    suppliers = FieldList(FormField(SupplierEntryForm), min_entries=1)
    submit = SubmitField("Save Supplier")


class CustomerEntryForm(FlaskForm):
    class Meta:
        csrf = False

    name = StringField(
        "Customer Name",
        validators=[DataRequired(message="Customer name is required.")]
    )
    phone = StringField(
        "Phone Number",
        validators=[Optional(), Length(max=20)]
    )
    email = StringField(
        "Email Address",
        validators=[Optional(), Email(message="Enter a valid email address.")]
    )
    balance_owed = FloatField(
        "Balance Owed",
        validators=[Optional()],
        default=0.0
    )


class CustomerForm(FlaskForm):
    customers = FieldList(FormField(CustomerEntryForm), min_entries=1)
    submit = SubmitField("Save Customers")


#
# with app.app_context():
#     total_deb=[]
#     total_payed=[]
#     unique_id=list(set(p.supplier_id for p in Purchase.query.all() ))
#     for i in unique_id:
#         purchase=Purchase.query.filter_by(
#             supplier_id=i
#         ).all()
#         purchase_id=(i.id for i in purchase)
#         tot_am=0
#         for k in purchase_id:
#             tot=SupplierPayment.query.filter_by(
#             purchase_id=k
#         ).all()
#             total_amount = sum(p.amount for p in tot)
#             tot_am+=total_amount
#
#         total_payed.append(tot_am)
#         total_debt = sum(p.debt for p in purchase)
#         total_deb.append(total_debt)
#     # for k in uniq:
#     #     payments = SupplierPayment.query.filter_by(
#     #         purchase_id=k
#     #     ).all()
#     #
#     #     total_paid = sum(p.amount for p in payments)
#     #     total_payed.append(total_paid)
#     print(sum(total_deb))
#     print(total_deb)
#     print(total_payed)
#     print(sum(total_deb)-sum(total_payed))
#     # do you have any comment i wanted to show the debt wich i own for all supplier comment






class SaleEntryForm(FlaskForm):
    class Meta:
        csrf = False  # CSRF token only needed once, on the parent form

    product_id = SelectField(
        "Select Product",
        coerce=int,
        validators=[DataRequired(message="Please select a product.")]
    )
    customer_id = SelectField(
        "Select Customer",
        coerce=int,
        validators=[DataRequired(message="Please select a customer.")]
    )
    measurement = SelectField(
        "Measurement",
        choices=[
            ("", "Select measurement (optional)"),
            ("piece", "Piece"),
            ("kg", "Kg"),
            ("liter", "Liter"),
            ("package", "Package"),
            ("box", "Box"),
            ("meter", "Meter"),
            ("other", "Other")
        ],
        validators=[Optional()]
    )
    quantity = FloatField(
        "Quantity",
        validators=[DataRequired(message="Quantity is required."), NumberRange(min=0.01, message="Quantity must be greater than 0.")]
    )
    unit_price = FloatField(
        "Selling Price",
        validators=[DataRequired(message="Selling price is required."), NumberRange(min=0.01, message="Price must be greater than 0.")]
    )
    current_payment = FloatField(
        "Current Payment",
        validators=[Optional(), NumberRange(min=0, message="Payment cannot be negative.")],
        default=0
    )


class SaleForm(FlaskForm):
    sales = FieldList(FormField(SaleEntryForm), min_entries=1)
    submit = SubmitField("Sell Product")



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match')]
    )
    submit = SubmitField('Create Account')

class UserEditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    is_verified = BooleanField('Verified')
    submit = SubmitField('Save Changes')


class AddDebtForm(FlaskForm):
    amount = DecimalField(
        'Amount',
        validators=[
            DataRequired(message="Please enter an amount."),
            NumberRange(min=0.01, message="Amount must be greater than zero.")
        ],
        places=2
    )
    description = StringField(
        'Note / Reference (Optional)'
    )
    submit = SubmitField('Save Debt')