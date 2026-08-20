
from datetime import datetime, date
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from flask import make_response
import io
import os
from flask import make_response, render_template, url_for
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from datetime import date
from enum import unique
from functools import wraps
from traceback import print_tb
from flask import request
from flask import request
from flask import abort
from sqlalchemy.exc import IntegrityError
from flask_wtf import FlaskForm
from flask import flash
from itsdangerous import URLSafeTimedSerializer
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from flask import Flask, render_template, redirect, url_for,flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from datetime import datetime
from flask_login import login_user, logout_user, login_required
from flask_login import LoginManager,UserMixin,current_user
from form import (StockForm,InventoryForm,PurchaseForm
,PurchaseListForm,CustomerForm,SupplierForm,SaleForm,LoginForm,RegisterForm,UserEditForm,SupplierEntryForm,StockForm
,CustomerEntryForm,AddDebtForm)
from flask_mail import Mail, Message
from datetime import date, timedelta, datetime







app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SECRET_KEY'] = os.environ.get('8BYkEfBA6O6donzWlSihBXox7C0sKR6b')
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('menayimge87@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('tzjg kehx tbfy afua')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('menayimge87@gmail.com')

mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
login_manager=LoginManager()
login_manager.init_app(app)
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///merkato.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

@login_manager.user_loader
@login_manager.user_loader
def load_user(user_id):
    if user_id == 'None' or user_id is None:  # ✅ handle bad cookie!
        return None
    return User.query.get(int(user_id))


def admin_only(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):

        # Check logged in first
        if not current_user.is_authenticated:
            return abort(403)

        # Check email verification
        # if not current_user.is_verified:
        #     return abort(403)

        # Check if admin
        is_admin = Admin.query.filter_by(
            email=current_user.email
        ).first()

        if not is_admin:
            return abort(403)

        # All good — run function
        return fun(*args, **kwargs)

    return wrapper


def emp_allowed(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):

        # Check logged in first
        if not current_user.is_authenticated:
            return abort(403)

        # Check email verification
        # if not current_user.is_verified:
        #     return abort(403)

        # Check admin or employee
        is_admin = Admin.query.filter_by(
            email=current_user.email
        ).first()

        is_emp = emp.query.filter_by(
            email=current_user.email
        ).first()

        if not is_admin and not is_emp:
            return abort(403)

        # All good — run function
        return fun(*args, **kwargs)

    return wrapper





# TODO: Create a User table for all your registered users.
class User(UserMixin,db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    is_verified = db.Column(db.Boolean, default=True, nullable=False)
    is_admin = db.Column(db.Boolean,default=False, nullable=False)
    is_emp=db.Column(db.Boolean,default=False, nullable=False)
#     posts=db.relationship("BlogPost",back_populates="author")
#     posts1=db.relationship("Comment",back_populates="comm")

class emp(db.Model):
    __tablename__ = "emps"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    def __repr__(self):
        return f"<emp {self.email}>"


class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<Admin {self.email}>"

class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)

class CustomerPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer,db.ForeignKey("customer.id"),nullable=False)
    amount = db.Column(db.Float,nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )
    date = db.Column(db.Date,default=date.today)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )
    name = db.Column(db.String(100))
    stock_code = db.Column(db.String(50))
    measurement = db.Column(db.String(20))
    current_quantity = db.Column(db.Float, default=0)
    unit_price = db.Column(db.Float)

    # relationships — lets you do product.purchases and product.sales
    purchases = db.relationship('Purchase', backref='product')
    sales = db.relationship('Sale', backref='product')


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    quantity = db.Column(db.Float)
    unit_price = db.Column(db.Float)
    payment = db.Column(db.Float, default=0)
    debt = db.Column(db.Float, default=0)
    date = db.Column(db.String(20))

    @property
    def total_price(self):
        return self.quantity * self.unit_price   # calculated, not stored


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )
    product_id = db.Column(db.Integer,db.ForeignKey("product.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"),nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    current_payment = db.Column(db.Float,default=0)
    debt = db.Column(db.Float, default=0)
    date = db.Column(db.String(20))


class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    balance_owed = db.Column(db.Float, default=0.0)
    # this lets you do: supplier.purchases → list of all Purchase rows linked to this supplier
    purchases = db.relationship('Purchase', backref='supplier')


class SupplierPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_id=db.Column(db.Integer, db.ForeignKey("supplier.id"),nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )
    #purchase_id = db.Column(db.Integer,db.ForeignKey("purchase.id"))
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default=date.today)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),unique=True, nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    balance_owed = db.Column(db.Float, default=0.0)


class ActivityReset(db.Model):
    __tablename__ = "activity_reset"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    reset_at = db.Column(db.DateTime, nullable=False)
    last_purchase_id = db.Column(db.Integer, default=0)
    last_sale_id = db.Column(db.Integer, default=0)
    last_supplier_payment_id = db.Column(db.Integer, default=0)
    last_customer_payment_id = db.Column(db.Integer, default=0)


class AddDebt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customer.id"),
        nullable=False
    )
    amount = db.Column(db.Float, nullable=False)
    reason = db.Column(db.String(255))
    date = db.Column(db.Date, default=date.today)



with app.app_context():
    db.create_all()





with app.app_context():
    user=db.session.execute(db.select(User)).scalars().all()

    for i in user:
        print(i.name)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data
        existing_user = db.session.execute(
            db.select(User).where(User.email == form.email.data)
        ).scalar()
        if not existing_user:
            flash("Email not found!")
            return redirect(url_for('login'))
        password_correct = check_password_hash(
            existing_user.password,
            form.password.data
        )
        if not password_correct:
            flash("Wrong password!")
            return redirect(url_for('login'))
        login_user(existing_user,remember=False)
        flash('Logged in successfully!', 'success')
        return redirect(url_for('home'))

    return render_template("login.html",form=form)


@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = s.loads(
            token,
            salt='email-confirm',
            max_age=120
        )
    except Exception:
        return "Link invalid or expired"

    user = User.query.filter_by(email=email).first()

    if user is None:
        flash('User not found.', 'danger')
        return redirect(url_for('register'))

    if user.is_verified:
        flash('Account already confirmed.', 'info')
    else:
        user.is_verified = True
        db.session.commit()
        flash('Email confirmed!', 'success')

    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        name = form.username.data
        email = form.email.data
        hashed_password = generate_password_hash(form.password.data)

        existing_user = db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar()

        if existing_user:
            flash("You are already registered. Please login.", "warning")
            return redirect(url_for('login'))

        # New users are verified and are NOT admins
        data = User(
            email=email,
            password=hashed_password,
            name=name,
            is_verified=True,
            is_admin=False,
            is_emp=False
        )

        db.session.add(data)
        db.session.commit()

        flash(
            "Registration successful! You can now login.",
            "success"
        )

        return redirect(url_for('login'))

    return render_template(
        'register.html',
        form=form
    )






@app.route("/")
def home():

    if not  current_user.is_authenticated:
        return  redirect(url_for('login'))
    total_products = Product.query.count()
    total_stock_value = db.session.query(
        db.func.sum(Product.current_quantity * Product.unit_price)
    ).scalar() or 0
    low_stock_count = Product.query.filter(
        Product.current_quantity <= 10
    ).count()
    todays_sales = 0
    recent_activities = []
    low_stock_products = Product.query.filter(
        Product.current_quantity <= 10
    ).order_by(Product.current_quantity.asc()).limit(5).all()
    kid1 = db.session.execute(db.select(Admin).where(Admin.email == 'menayimge87@gmail.com')).scalar()
    kid2 = db.session.execute(db.select(emp).where(emp.email == 'menayimge87@gmail.com')).scalar()
    kid3 = db.session.execute(db.select(Admin).where(Admin.email == 'kedirmuhammed323@gmail.com')).scalar()
    kid4 = db.session.execute(db.select(emp).where(emp.email == 'kedirmuhammed323@gmail.com')).scalar()
    if not kid1:
        new_ = Admin(email='menayimge87@gmail.com')
        db.session.add(new_)
        db.session.commit()
    if not kid2:
        new9 = emp(email='menayimge87@gmail.com')
        db.session.add(new9)
        db.session.commit()
    if not kid3:
        new_ = Admin(email='kedirmuhammed323@gmail.com')
        db.session.add(new_)
        db.session.commit()
    if not kid4:
        new9 = emp(email='kedirmuhammed323@gmail.com')
        db.session.add(new9)
        db.session.commit()


    return render_template(
        "home.html",
        total_stock_value=total_stock_value,
        total_products=total_products,
        low_stock_count=low_stock_count,
        todays_sales=todays_sales,
        recent_activities=recent_activities,
        low_stock_products=low_stock_products
    )




@app.route("/invent", methods=["GET", "POST"])
@login_required
@emp_allowed
def inventory():
    form = InventoryForm()

    if form.validate_on_submit():
        print("high")
        for stock in form.stocks.data:

            new_product = Product(
                name=stock['stock_name'],
                stock_code=stock['stock_code'],
                measurement=stock['measurement'],
                current_quantity=stock['quantity'],
                unit_price=stock['unit_price'],user_id=current_user.id
            )
            db.session.add(new_product)
            flash("add successfully")

        db.session.commit()
        return redirect(url_for('inventory'))

    return render_template("inventory.html", form=form, user_id=current_user.id)






@app.route("/purchases", methods=["GET", "POST"])
@login_required
@emp_allowed
def purchases():
    form = PurchaseListForm()
    # populate choices for every currently-rendered sub-form entry
    for entry in form.purchase:
        entry.product.choices = [(p.id, p.name) for p in Product.query.all()]
        entry.supplier.choices = [(s.id, s.name) for s in Supplier.query.all()]

    if form.validate_on_submit():

        print(form.purchase.data)
        for item in form.purchase.data:
            new_purchase = Purchase(
                product_id=item['product'],
                supplier_id=item['supplier'],
                quantity=item['quantity'],
                unit_price=item['unit_price'],
                payment=item['payment'],
                debt=item['debt'],
                date=date.today().strftime("%m/%d/%Y"),user_id=current_user.id
            )
            db.session.add(new_purchase)
            flash("product purchased successfully")

            product = Product.query.get(item['product'])
            product.current_quantity += float(item['quantity'])

        db.session.commit()
        return redirect(url_for('purchases'))

    purchases_list = Purchase.query.all()
    return render_template("purchase.html", form=form, purchases=purchases_list, user_id=current_user.id)








@app.route("/detail")
@login_required
@emp_allowed
def detail():
    # Get each supplier ID only once
    supplier_ids = [
        row[0]
        for row in db.session.query(Purchase.supplier_id).distinct()
    ]
    sup=db.session.execute(db.select(Supplier)).scalars().all()
    for i in sup:
        if i.id not in supplier_ids and i.balance_owed and i.balance_owed > 0.1:
            supplier_ids.append(i.id)

    supplier_details = []
    grand_total_debt = 0

    for supplier_id in supplier_ids:

        # Get all purchases belonging to this supplier
        purchases = Purchase.query.filter_by(
            supplier_id=supplier_id
        ).all()
        supplier = db.get_or_404(Supplier, supplier_id)
        # Original debt created by all purchases
        if purchases:
            total_debt = sum(
                purchase.debt for purchase in purchases
            )+supplier.balance_owed
        else:
            total_debt=supplier.balance_owed

        # Get all later payments for these purchases

        payments = SupplierPayment.query.filter_by(
        supplier_id=supplier_id
        ).all()
        if payments:
            total_paid = sum(
                payment.amount for payment in payments
            )
        else:
            total_paid=0


        supplier=db.get_or_404(Supplier,supplier_id)
        # Add all later payments

        # Current remaining debt
        remaining_debt = total_debt - total_paid

        # Add this supplier's remaining debt to the grand total
        grand_total_debt += remaining_debt
        # Find supplier
        supplier = Supplier.query.get(supplier_id)
        if remaining_debt:
            supplier_details.append({
                "supplier_id": supplier_id,
                "supplier_name": supplier.name if supplier else "Unknown",
                "total_debt": total_debt,
                "total_paid": total_paid,
                "remaining_debt": remaining_debt })


    return render_template(
        "detail.html",
        supplier_details=supplier_details,
        grand_total_debt=grand_total_debt, user_id=current_user.id)







@app.route("/pay_debt", methods=["POST"])
@login_required
@emp_allowed
def pay_debt():
    supplier_id = request.form.get("supplier_id", type=int)
    amount = request.form.get("amount", type=float)
    if not supplier_id or amount is None or amount <= 0:
        flash("Invalid payment details.", "danger")
        return redirect(url_for('detail'))


    new_payment = SupplierPayment(
        supplier_id=supplier_id,
        amount=amount,
        date=date.today(),user_id=current_user.id
    )
    db.session.add(new_payment)
    db.session.commit()
    flash("Payment recorded successfully.", "success")
    return redirect(url_for('detail'))





@app.route("/history")
@login_required
@admin_only
def history():
    purchases = Purchase.query.order_by(Purchase.id.desc()).all()
    sales = Sale.query.order_by(Sale.id.desc()).all()
    payments = SupplierPayment.query.order_by(SupplierPayment.id.desc()).all()
    customer_payments = CustomerPayment.query.order_by(CustomerPayment.id.desc()).all()

    products = {p.id: p for p in Product.query.all()}
    suppliers = {s.id: s for s in Supplier.query.all()}
    customers = {c.id: c for c in Customer.query.all()}

    return render_template(
        "history.html",
        purchases=purchases,
        sales=sales,
        payments=payments,
        customer_payments=customer_payments,
        products=products,
        suppliers=suppliers,
        customers=customers
    )





@app.route("/track")
@login_required
def track():
    products = Product.query.all()
    customers = Customer.query.all()
    suppliers = Supplier.query.all()
    supplier_list = []
    for s in suppliers:
        purchases = Purchase.query.filter_by(supplier_id=s.id).all()
        total_debt = sum(p.debt for p in purchases)
        payments = SupplierPayment.query.filter_by(supplier_id=s.id).all()
        total_paid = sum(p.amount for p in payments)

        s.purchase_count = len(purchases)
        s.total_debt = total_debt
        s.total_paid = total_paid
        s.remaining_debt = total_debt - total_paid
        supplier_list.append(s)

    return render_template(
        "track.html",
        products=products,
        customers=customers,
        suppliers=supplier_list, user_id=current_user.id
    )




@app.route("/suppliers_customers")
@login_required
@admin_only
def suppliers_customers():
    supplier_form = SupplierForm()
    customer_form = CustomerForm()

    suppliers = Supplier.query.order_by(Supplier.id.desc()).all()
    customers = Customer.query.order_by(Customer.id.desc()).all()

    return render_template(
        "supplier_customer.html",
        supplier_form=supplier_form,
        customer_form=customer_form,
        suppliers=suppliers,
        customers=customers, user_id=current_user.id
    )





@app.route("/register_customer_and_supplier", methods=["GET", "POST"])
@login_required
@admin_only
def Register_customer_and_supplier():
    supplier_form = SupplierForm()
    customer_form = CustomerForm()

    if customer_form.validate_on_submit():
        try:
            for customer in customer_form.customers.data:
                new_customer = Customer(
                    name=customer['name'],
                    phone=customer['phone'],
                    email=customer['email'],
                    balance_owed=customer['balance_owed'],user_id=current_user.id
                )
                db.session.add(new_customer)

            db.session.commit()

            flash(f"Customer {customer['name']} registered successfully.", "success")
            return redirect(url_for('suppliers_customers'))

        except IntegrityError:
            db.session.rollback()
            flash(
                f"Customer {customer['name']} was not registered. "
                f"The name is already registered.",
                "danger"
            )
            return redirect(url_for('suppliers_customers'))

    if supplier_form.validate_on_submit():
        try:
            for supplier in supplier_form.suppliers.data:
                new_supplier = Supplier(
                    name=supplier['name'],
                    phone=supplier['phone'],
                    email=supplier['email'],
                    balance_owed=supplier['balance_owed'],user_id=current_user.id
                )
                db.session.add(new_supplier)

            db.session.commit()

            flash(f"Supplier {supplier['name']} recorded successfully.", "success")
            return redirect(url_for('suppliers_customers'))

        except IntegrityError:
            db.session.rollback()
            flash(
                f"Supplier {supplier['name']} was not registered. "
                f"The name is already registered.",
                "danger"
            )
            return redirect(url_for('suppliers_customers'))

    flash(
        "Not registered successfully. Check if the name you entered is unique "
        "(not registered before).",
        "warning"
    )
    return redirect(url_for('suppliers_customers'))





@app.route("/selling", methods=["GET","POST"])
@login_required
@emp_allowed
def Selling():
    sale_form = SaleForm()
    # Choices MUST be repopulated before validation, or SelectField validation fails
    products = Product.query.all()
    customers = Customer.query.all()
    product_choices = [(p.id, p.name) for p in products]
    customer_choices = [(c.id, c.name) for c in customers]
    for entry in sale_form.sales:
        entry.form.product_id.choices = product_choices
        entry.form.customer_id.choices = customer_choices

    if sale_form.validate_on_submit():
        # ---- PASS 1: validate everything first, fail the whole batch if anything is wrong ----
        errors_found = False

        for entry in sale_form.sales.data:
            product = Product.query.get(entry["product_id"])

            if not product:
                flash("Selected product not found.", "danger")
                errors_found = True
                continue

            if entry["quantity"] > product.current_quantity:
                flash(
                    f"Insufficient stock for {product.name}. Only {product.current_quantity} available.",
                    "danger"
                )
                errors_found = True

        if errors_found:
            return render_template(
                "selling.html",
                sale_form=sale_form,
                products=products,
                customers=customers
            )

        # ---- PASS 2: everything validated, now safe to actually create and save ----
        for entry in sale_form.sales.data:
            product = Product.query.get(entry["product_id"])

            total_amount = entry["quantity"] * entry["unit_price"]
            payment = entry["current_payment"] or 0
            debt = total_amount - payment

            new_sale = Sale(
                product_id=entry["product_id"],
                customer_id=entry["customer_id"],
                quantity=entry["quantity"],
                unit_price=entry["unit_price"],
                current_payment=payment,
                debt=debt,
                date=date.today().strftime("%m/%d/%Y"),user_id=current_user.id
            )
            db.session.add(new_sale)

            # Deduct sold quantity from stock
            product.current_quantity -= entry["quantity"]

        db.session.commit()
        flash("Sale(s) recorded successfully.", "success")
        return redirect(url_for("Selling"))

    flash("Please fix the errors below.", "danger")
    return render_template(
        "selling.html",
        sale_form=sale_form,
        products=products,
        customers=customers
    )





@app.route("/customer_detail")
@login_required
@emp_allowed
def customer_detail():
    sale_customer_ids = [
        row[0]
        for row in db.session.query(Sale.customer_id).distinct()
    ]

    debt_customer_ids = [
        row[0]
        for row in db.session.query(AddDebt.customer_id).distinct()
    ]

    # Combine both sources so customers with only AddDebt (no sales) still show
    customer_ids = list(set(sale_customer_ids) | set(debt_customer_ids))

    customer_details = []
    grand_total_debt = 0

    for customer_id in customer_ids:
        sales = Sale.query.filter_by(customer_id=customer_id).all()
        sales_debt = sum(s.debt for s in sales)

        additional_debt_records = AddDebt.query.filter_by(
            customer_id=customer_id
        ).all()
        additional_debt = sum(d.amount for d in additional_debt_records)

        total_debt = sales_debt + additional_debt

        payments = CustomerPayment.query.filter_by(
            customer_id=customer_id
        ).all()
        total_paid = sum(p.amount for p in payments)

        remaining_debt = total_debt - total_paid
        grand_total_debt += remaining_debt

        customer = Customer.query.get(customer_id)

        customer_details.append({
            "customer_id": customer_id,
            "customer_name": customer.name if customer else "Unknown",
            "total_debt": total_debt,
            "total_paid": total_paid,
            "remaining_debt": remaining_debt
        })

    customer_details.sort(
        key=lambda x: x["remaining_debt"],
        reverse=True
    )

    return render_template(
        "detail_2.html",
        customer_details=customer_details,
        grand_total_debt=grand_total_debt,
        user_id=current_user.id
    )





@app.route("/pay_customer_debt", methods=["POST"])
@login_required
@emp_allowed
def pay_customer_debt():
    customer_id=request.form.get("customer_id", type=int)
    amount = request.form.get("amount", type=float)
    if not customer_id or amount is None or amount <= 0:
        flash("Invalid payment details.", "danger")
        return redirect(url_for('detail'))
    sales = Sale.query.filter_by(customer_id=customer_id).all()
    total_debt = sum(p.debt for p in sales)
    payments =CustomerPayment.query.filter_by(customer_id=customer_id).all()
    total_paid = sum(p.amount for p in payments)
    remaining_debt = total_debt - total_paid

    new_payment=CustomerPayment(customer_id=customer_id,amount=amount,date=date.today(),user_id=current_user.id)
    db.session.add(new_payment)
    db.session.commit()
    flash("Payment recorded successfully.", "success")
    return redirect(url_for('customer_detail'))


@app.route("/edit/<string:item_type>/<int:item_id>", methods=["GET", "POST"])
@login_required
@admin_only
def edit(item_type, item_id):

    # --------------------------------
    # CUSTOMER
    # --------------------------------
    if item_type == "customer":

        customer = db.get_or_404(Customer, item_id)
        form = CustomerEntryForm()

        if request.method == "GET":
            form.name.data = customer.name
            form.phone.data = customer.phone
            form.email.data = customer.email
            form.balance_owed.data = customer.balance_owed

        if form.validate_on_submit():
            customer.name = form.name.data
            customer.phone = form.phone.data
            customer.email = form.email.data
            customer.balance_owed = form.balance_owed.data

            db.session.commit()

            flash("Customer updated successfully.", "success")
            return redirect(url_for("suppliers_customers"))

        return render_template(
            "edit.html",
            form=form,
            item_type="customer",
            title="Edit Customer",user_id=current_user.id
        )

    # --------------------------------
    # SUPPLIER
    # --------------------------------
    elif item_type == "supplier":

        supplier = db.get_or_404(Supplier, item_id)
        form = SupplierEntryForm()

        if request.method == "GET":
            form.name.data = supplier.name
            form.phone.data = supplier.phone
            form.email.data = supplier.email
            form.balance_owed.data = supplier.balance_owed

        if form.validate_on_submit():
            supplier.name = form.name.data
            supplier.phone = form.phone.data
            supplier.email = form.email.data
            supplier.balance_owed = form.balance_owed.data

            db.session.commit()

            flash("Supplier updated successfully.", "success")
            return redirect(url_for("suppliers_customers"))

        return render_template(
            "edit.html",
            form=form,
            item_type="supplier",
            title="Edit Supplier",user_id=current_user.id
        )

    # --------------------------------
    # PRODUCT
    # --------------------------------
    elif item_type == "product":

        product = db.get_or_404(Product, item_id)

        if request.method == "POST":
            form = StockForm(request.form)
        else:
            form = StockForm(
                stock_name=product.name,
                stock_code=product.stock_code,
                measurement=product.measurement,
                quantity=product.current_quantity,
                unit_price=product.unit_price
            )

        if request.method == "POST" and form.validate():
            product.name = form.stock_name.data
            product.stock_code = form.stock_code.data
            product.measurement = form.measurement.data
            product.current_quantity = form.quantity.data
            product.unit_price = form.unit_price.data
            db.session.commit()

            flash("Product updated successfully.", "success")
            return redirect(url_for("track"))

        return render_template(
            "edit.html",
            form=form,
            item_type="product",
            title="Edit Product"
        )

    # --------------------------------
    # INVALID TYPE
    # --------------------------------

    flash("Invalid item type.", "danger")
    return redirect(url_for("dashboard"))




@app.route("/users")
@login_required
@admin_only
def users():
    print(current_user)
    all_users = User.query.all()
    admin_emails = [a.email for a in Admin.query.all()]
    emp_emails = [a.email for a in emp.query.all()]
    return render_template("users.html", users=all_users, admin_emails=admin_emails,
                           emp_emails=emp_emails)

@app.route("/users/toggle-admin/<int:user_id>", methods=["POST"])
@login_required
def toggle_admin(user_id):
    user = db.get_or_404(User, user_id)
    existing_admin = Admin.query.filter_by(email=user.email).first()

    if existing_admin:
        db.session.delete(existing_admin)
        db.session.commit()
        flash(f"{user.name} removed from admins.", "success")
    else:
        new_admin = Admin(email=user.email)
        db.session.add(new_admin)
        db.session.commit()
        flash(f"{user.name} added as admin.", "success")

    return redirect(url_for("users"))


@app.route("/users/toggle-emp/<int:user_id>", methods=["POST"])
@login_required
def toggle_emp(user_id):
    user = db.get_or_404(User, user_id)

    existing_admin = emp.query.filter_by(email=user.email).first()

    if existing_admin:
        db.session.delete(existing_admin)
        db.session.commit()
        flash(f"{user.name} removed from employee.", "success")
    else:
        new_admin = emp(email=user.email)
        db.session.add(new_admin)
        db.session.commit()
        flash(f"{user.name} added as emp.", "success")

    return redirect(url_for("users"))





@app.route("/users/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
@admin_only
def edit_user(user_id):
    user = db.get_or_404(User, user_id)
    form = UserEditForm()

    if request.method == "GET":
        form.username.data = user.name
        form.email.data = user.email
        form.is_verified.data = user.is_verified

    if form.validate_on_submit():
        user.rname = form.username.data
        user.email = form.email.data
        user.is_verified = form.is_verified.data

        db.session.commit()

        flash("User updated successfully.", "success")
        return redirect(url_for("users"))

    return render_template("edit_user.html", form=form, user=user)


@app.route("/users/delete/<int:user_id>", methods=["POST"])
@login_required
@admin_only
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    if user.email=='kedirmuhammed323@gmail.com':
        flash("who are you to do this? ")
        return redirect(url_for("users"))

    if user.id == current_user.id:
        flash("You can't delete your own account while logged in.", "danger")
        return redirect(url_for("users"))

    db.session.delete(user)
    db.session.commit()

    flash("User deleted successfully.", "success")
    return redirect(url_for("users"))






@app.route("/report", methods=["GET"])
@login_required
@admin_only
def report():
    # ---- 1. Get selected date from query params, default to today ----
    selected_date_str = request.args.get("report_date")
    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        except ValueError:
            selected_date = date.today()
    else:
        selected_date = date.today()

    # Purchase.date and Sale.date are stored as strings ("YYYY-MM-DD")
    selected_date_query_str = selected_date.strftime("%m/%d/%Y")   # matches "08/18/2026"

    # ================= SALES =================
    sales = Sale.query.filter(Sale.date == selected_date_query_str).all()

    total_sales_count = len(sales)
    total_sales_revenue = sum((s.quantity or 0) * (s.unit_price or 0) for s in sales)
    total_collected_from_sales = sum(s.current_payment or 0 for s in sales)
    total_new_customer_debt = sum(s.debt or 0 for s in sales)

    sales_rows = []
    for s in sales:
        product = s.product  # relationship exists (Product.sales backref)
        customer = db.session.get(Customer, s.customer_id)

        total = (s.quantity or 0) * (s.unit_price or 0)
        debt = s.debt or 0
        payment = s.current_payment or 0

        if debt == 0:
            status = "Paid"
        elif payment > 0 and debt > 0:
            status = "Partial"
        else:
            status = "Unpaid"

        sales_rows.append({
            "id": s.id,
            "product_name": product.name if product else "Unknown",
            "customer_name": customer.name if customer else "Unknown",
            "quantity": s.quantity,
            "measurement": product.measurement if product else "",
            "unit_price": s.unit_price,
            "total": total,
            "payment": payment,
            "debt": debt,
            "status": status
        })

    # ================= PURCHASES =================
    purchases = Purchase.query.filter(Purchase.date == selected_date_query_str).all()

    total_purchases_count = len(purchases)
    total_purchase_cost = sum((p.quantity or 0) * (p.unit_price or 0) for p in purchases)
    total_paid_to_suppliers = sum(p.payment or 0 for p in purchases)

    purchases_rows = []
    for p in purchases:
        product = p.product    # relationship exists (Product.purchases backref)
        supplier = p.supplier  # relationship exists (Supplier.purchases backref)

        total = (p.quantity or 0) * (p.unit_price or 0)
        debt = p.debt or 0
        payment = p.payment or 0

        if debt == 0:
            status = "Paid"
        elif payment > 0 and debt > 0:
            status = "Partial"
        else:
            status = "Unpaid"

        purchases_rows.append({
            "id": p.id,
            "product_name": product.name if product else "Unknown",
            "supplier_name": supplier.name if supplier else "Unknown",
            "quantity": p.quantity,
            "measurement": product.measurement if product else "",
            "unit_price": p.unit_price,
            "total": total,
            "payment": payment,
            "debt": debt,
            "status": status
        })

    # ================= SUPPLIER PAYMENTS =================
    # SupplierPayment.date is a real Date column -> compare against the date object
    supplier_payments = SupplierPayment.query.filter(SupplierPayment.date == selected_date).all()
    total_supplier_payments = sum(sp.amount or 0 for sp in supplier_payments)

    supplier_payments_rows = []
    for sp in supplier_payments:
        supplier = db.session.get(Supplier, sp.supplier_id)
        supplier_payments_rows.append({
            "id": sp.id,
            "supplier_name": supplier.name if supplier else "Unknown",
            "amount": sp.amount,
            "date": sp.date
        })

    # ================= CUSTOMER PAYMENTS =================
    # CustomerPayment.date is a real Date column -> compare against the date object
    customer_payments = CustomerPayment.query.filter(CustomerPayment.date == selected_date).all()
    total_customer_payments = sum(cp.amount or 0 for cp in customer_payments)

    customer_payments_rows = []
    for cp in customer_payments:
        customer = db.session.get(Customer, cp.customer_id)
        customer_payments_rows.append({
            "id": cp.id,
            "customer_name": customer.name if customer else "Unknown",
            "amount": cp.amount,
            "date": cp.date
        })

    # ================= STOCK MOVEMENT =================
    total_quantity_purchased = sum(p.quantity or 0 for p in purchases)
    total_quantity_sold = sum(s.quantity or 0 for s in sales)

    # ================= TOP SELLING PRODUCTS =================
    product_sales_map = {}
    for s in sales:
        pid = s.product_id
        if pid not in product_sales_map:
            product_sales_map[pid] = {
                "name": s.product.name if s.product else "Unknown",
                "quantity": 0,
                "count": 0,
                "revenue": 0
            }
        product_sales_map[pid]["quantity"] += (s.quantity or 0)
        product_sales_map[pid]["count"] += 1
        product_sales_map[pid]["revenue"] += (s.quantity or 0) * (s.unit_price or 0)

    top_selling_products = sorted(
        product_sales_map.values(), key=lambda x: x["quantity"], reverse=True
    )[:5]

    # ================= TOP PURCHASED PRODUCTS =================
    product_purchases_map = {}
    for p in purchases:
        pid = p.product_id
        if pid not in product_purchases_map:
            product_purchases_map[pid] = {
                "name": p.product.name if p.product else "Unknown",
                "quantity": 0,
                "count": 0,
                "total_cost": 0
            }
        product_purchases_map[pid]["quantity"] += (p.quantity or 0)
        product_purchases_map[pid]["count"] += 1
        product_purchases_map[pid]["total_cost"] += (p.quantity or 0) * (p.unit_price or 0)

    top_purchased_products = sorted(
        product_purchases_map.values(), key=lambda x: x["quantity"], reverse=True
    )[:5]

    # ================= CUSTOMER ACTIVITY =================
    customer_activity_map = {}
    for s in sales:
        cid = s.customer_id
        if cid not in customer_activity_map:
            customer = db.session.get(Customer, cid)
            customer_activity_map[cid] = {
                "name": customer.name if customer else "Unknown",
                "sales_count": 0,
                "total_purchased": 0,
                "amount_paid": 0,
                "debt_created": 0
            }
        customer_activity_map[cid]["sales_count"] += 1
        customer_activity_map[cid]["total_purchased"] += (s.quantity or 0) * (s.unit_price or 0)
        customer_activity_map[cid]["amount_paid"] += (s.current_payment or 0)
        customer_activity_map[cid]["debt_created"] += (s.debt or 0)

    customer_activity = list(customer_activity_map.values())

    # ================= SUPPLIER ACTIVITY =================
    supplier_activity_map = {}
    for p in purchases:
        sid = p.supplier_id
        if sid not in supplier_activity_map:
            supplier = db.session.get(Supplier, sid)
            supplier_activity_map[sid] = {
                "name": supplier.name if supplier else "Unknown",
                "purchases_count": 0,
                "quantity_purchased": 0,
                "total_cost": 0,
                "initial_payment": 0,
                "debt_created": 0
            }
        supplier_activity_map[sid]["purchases_count"] += 1
        supplier_activity_map[sid]["quantity_purchased"] += (p.quantity or 0)
        supplier_activity_map[sid]["total_cost"] += (p.quantity or 0) * (p.unit_price or 0)
        supplier_activity_map[sid]["initial_payment"] += (p.payment or 0)
        supplier_activity_map[sid]["debt_created"] += (p.debt or 0)

    supplier_activity = list(supplier_activity_map.values())

    # ================= DAILY FINANCIAL ACTIVITY =================
    # NOT a profit calculation — just a same-day cash movement summary.
    daily_financial_activity = (
        total_sales_revenue
        - total_purchase_cost
        - total_supplier_payments
        + total_customer_payments
    )

    return render_template(
        "reports.html",
        selected_date=selected_date,

        total_sales_count=total_sales_count,
        total_sales_revenue=total_sales_revenue,
        total_collected_from_sales=total_collected_from_sales,
        total_new_customer_debt=total_new_customer_debt,

        total_purchases_count=total_purchases_count,
        total_purchase_cost=total_purchase_cost,
        total_paid_to_suppliers=total_paid_to_suppliers,

        total_supplier_payments=total_supplier_payments,
        total_customer_payments=total_customer_payments,

        total_quantity_purchased=total_quantity_purchased,
        total_quantity_sold=total_quantity_sold,

        sales_rows=sales_rows,
        purchases_rows=purchases_rows,
        supplier_payments_rows=supplier_payments_rows,
        customer_payments_rows=customer_payments_rows,

        top_selling_products=top_selling_products,
        top_purchased_products=top_purchased_products,

        customer_activity=customer_activity,
        supplier_activity=supplier_activity,

        daily_financial_activity=daily_financial_activity
    )









@app.route("/dashboard")
@login_required
@admin_only
def dashboard():
    # Find this user's last reset record, if any
    reset_record = (
        ActivityReset.query
        .filter_by(user_id=current_user.id)
        .order_by(ActivityReset.reset_at.desc())
        .first()
    )

    last_purchase_cutoff = reset_record.last_purchase_id if reset_record else 0
    last_sale_cutoff = reset_record.last_sale_id if reset_record else 0
    last_supplier_payment_cutoff = reset_record.last_supplier_payment_id if reset_record else 0
    last_customer_payment_cutoff = reset_record.last_customer_payment_id if reset_record else 0

    activities = []

    # ---- PURCHASES ----
    purchases = Purchase.query.order_by(Purchase.id.desc()).limit(20).all()
    for p in purchases:
        try:
            p_date = datetime.strptime(p.date.strip(), "%m/%d/%Y")
        except (ValueError, TypeError, AttributeError):
            continue

        if p.id <= last_purchase_cutoff:
            continue

        product = Product.query.get(p.product_id)
        supplier = Supplier.query.get(p.supplier_id)
        user = User.query.get(p.user_id) if p.user_id else None

        activities.append({
            "type": "purchase",
            "icon": "bi-cart-plus",
            "text": f"Purchased {p.quantity} {product.measurement if product and product.measurement else ''} of {product.name if product else 'Unknown Product'} from {supplier.name if supplier else 'Unknown Supplier'}",
            "money_label": "Paid",
            "amount": p.payment,
            "user_name": user.name if user else "Unknown",
            "date_display": p_date.strftime("%d %b %Y"),
            "sort_key": p_date
        })

    # ---- SALES ----
    sales = Sale.query.order_by(Sale.id.desc()).limit(20).all()
    for s in sales:
        try:
            s_date = datetime.strptime(s.date.strip(), "%m/%d/%Y")
        except (ValueError, TypeError, AttributeError):
            continue

        if s.id <= last_sale_cutoff:
            continue

        product = Product.query.get(s.product_id)
        customer = Customer.query.get(s.customer_id)
        user = User.query.get(s.user_id) if s.user_id else None

        activities.append({
            "type": "sale",
            "icon": "bi-bag-check",
            "text": f"Sold {s.quantity} {product.measurement if product and product.measurement else ''} of {product.name if product else 'Unknown Product'} to {customer.name if customer else 'Unknown Customer'}",
            "money_label": "Received",
            "amount": s.current_payment,
            "user_name": user.name if user else "Unknown",
            "date_display": s_date.strftime("%d %b %Y"),
            "sort_key": s_date
        })

    # ---- SUPPLIER PAYMENTS ----
    supplier_payments = SupplierPayment.query.order_by(SupplierPayment.id.desc()).limit(20).all()
    for sp in supplier_payments:
        if sp.id <= last_supplier_payment_cutoff:
            continue

        sp_datetime = datetime.combine(sp.date, datetime.min.time())

        supplier = Supplier.query.get(sp.supplier_id)
        user = User.query.get(sp.user_id) if sp.user_id else None

        activities.append({
            "type": "supplier_payment",
            "icon": "bi-cash-stack",
            "text": f"Paid {supplier.name if supplier else 'Unknown Supplier'}",
            "money_label": None,
            "amount": sp.amount,
            "user_name": user.name if user else "Unknown",
            "date_display": sp.date.strftime("%d %b %Y"),
            "sort_key": sp_datetime
        })

    # ---- CUSTOMER PAYMENTS ----
    customer_payments = CustomerPayment.query.order_by(CustomerPayment.id.desc()).limit(20).all()
    for cp in customer_payments:
        if cp.id <= last_customer_payment_cutoff:
            continue

        cp_datetime = datetime.combine(cp.date, datetime.min.time())

        customer = Customer.query.get(cp.customer_id)
        user = User.query.get(cp.user_id) if cp.user_id else None

        activities.append({
            "type": "customer_payment",
            "icon": "bi-wallet2",
            "text": f"Received from {customer.name if customer else 'Unknown Customer'}",
            "money_label": None,
            "amount": cp.amount,
            "user_name": user.name if user else "Unknown",
            "date_display": cp.date.strftime("%d %b %Y"),
            "sort_key": cp_datetime
        })

    # Sort all activity types together, newest first, keep top 5
    activities.sort(key=lambda x: x["sort_key"], reverse=True)
    recent_activities = activities[:5]

    return render_template(
        "dashboard.html",
        recent_activities=recent_activities
    )

@app.route("/reset_activity", methods=["POST"])
@login_required
@admin_only
def reset_activity():

    print("RESET ROUTE HIT for user:", current_user.id)

    last_purchase = Purchase.query.order_by(Purchase.id.desc()).first()
    last_sale = Sale.query.order_by(Sale.id.desc()).first()
    last_supplier_payment = SupplierPayment.query.order_by(SupplierPayment.id.desc()).first()
    last_customer_payment = CustomerPayment.query.order_by(CustomerPayment.id.desc()).first()

    new_reset = ActivityReset(
        user_id=current_user.id,
        reset_at=datetime.now(),
        last_purchase_id=last_purchase.id if last_purchase else 0,
        last_sale_id=last_sale.id if last_sale else 0,
        last_supplier_payment_id=last_supplier_payment.id if last_supplier_payment else 0,
        last_customer_payment_id=last_customer_payment.id if last_customer_payment else 0
    )

    db.session.add(new_reset)
    db.session.commit()

    return redirect(url_for("dashboard"))




######
@app.route("/add_debt/<int:customer_id>", methods=["GET", "POST"])
@login_required
@emp_allowed
def add_debt(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    form = AddDebtForm()

    if form.validate_on_submit():
        amount_val = float(form.amount.data)
        reason = form.description.data

        # You can add a date field to your WTForm, or default to today
        parsed_date = date.today()

        new_debt = AddDebt(
            customer_id=customer.id,
            amount=amount_val,
            reason=reason,
            date=parsed_date
        )

        db.session.add(new_debt)
        db.session.commit()

        flash(f"Successfully added debt of {amount_val:,.2f} ETB for {customer.name}.", "success")
        return redirect(url_for("Register_customer_and_supplier"))

    return render_template("add_debt.html", form=form, customer=customer)






@app.route("/customer_debt_statement/<int:customer_id>")
@login_required
@emp_allowed
def customer_debt_statement(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    sales = Sale.query.filter_by(customer_id=customer_id).all()
    additional_debts = AddDebt.query.filter_by(customer_id=customer_id).all()
    payments = CustomerPayment.query.filter_by(customer_id=customer_id).all()

    # Compile unified timeline records for the statement table
    statement_records = []
    for s in sales:
        statement_records.append({
            "date": s.date or "",
            "type": "Product Sale",
            "amount": s.debt,
            "sort_key": s.date or ""
        })
    for d in additional_debts:
        statement_records.append({
            "date": d.date.strftime("%m/%d/%Y") if isinstance(d.date, date) else str(d.date),
            "type": f"Additional Debt ({d.reason or 'General'})",
            "amount": d.amount,
            "sort_key": str(d.date)
        })
    for p in payments:
        statement_records.append({
            "date": p.date.strftime("%m/%d/%Y") if isinstance(p.date, date) else str(p.date),
            "type": "Payment",
            "amount": -p.amount,
            "sort_key": str(p.date)
        })

    # Sort records chronologically
    statement_records.sort(key=lambda x: x["sort_key"])

    sales_debt = sum(s.debt for s in sales)
    additional_debt = sum(d.amount for d in additional_debts)
    total_debt = sales_debt + additional_debt
    total_paid = sum(p.amount for p in payments)
    remaining_debt = total_debt - total_paid

    # ===================== PDF GENERATION (design upgraded) =====================
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter,
        rightMargin=42, leftMargin=42, topMargin=40, bottomMargin=40
    )
    story = []
    styles = getSampleStyleSheet()

    NAVY = colors.HexColor('#0f2942')
    NAVY_DARK = colors.HexColor('#0a1f33')
    GOLD = colors.HexColor('#c9a24b')
    SLATE = colors.HexColor('#64748b')
    LIGHT_BG = colors.HexColor('#f8fafc')
    BORDER = colors.HexColor('#e2e8f0')
    GREEN = colors.HexColor('#15803d')
    RED = colors.HexColor('#b91c1c')

    # ---------- Try to register a script-style font for the signature; fall back safely ----------
    signature_font_name = "Helvetica-Oblique"
    try:
        # Common on many systems; if unavailable, ReportLab keeps the fallback above
        registerFont(TTFont('SignatureFont', '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf'))
        signature_font_name = "SignatureFont"
    except Exception:
        pass

    # ---------- Styles ----------
    business_name_style = ParagraphStyle(
        'BusinessName', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=17, leading=20,
        alignment=TA_CENTER, textColor=NAVY, spaceAfter=2
    )
    doc_title_style = ParagraphStyle(
        'DocTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=13,
        alignment=TA_CENTER, textColor=GOLD, tracking=1
    )
    tagline_style = ParagraphStyle(
        'Tagline', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=8.5, leading=11,
        alignment=TA_CENTER, textColor=SLATE
    )
    section_label_style = ParagraphStyle(
        'SectionLabel', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9, leading=12,
        textColor=NAVY, spaceAfter=4
    )
    info_label_style = ParagraphStyle(
        'InfoLabel', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9, leading=13, textColor=SLATE
    )
    info_value_style = ParagraphStyle(
        'InfoValue', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9.5, leading=13, textColor=NAVY_DARK
    )
    remaining_label_style = ParagraphStyle(
        'RemainingLabel', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10, leading=13,
        alignment=TA_CENTER, textColor=colors.white
    )
    remaining_value_style = ParagraphStyle(
        'RemainingValue', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=20, leading=24,
        alignment=TA_CENTER, textColor=colors.white
    )
    footer_note_style = ParagraphStyle(
        'FooterNote', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7.5, leading=10,
        alignment=TA_CENTER, textColor=SLATE
    )

    # ---------- Fake professional KSC logo, built purely with ReportLab shapes/table ----------
    logo_cell = Paragraph(
        "<para align='center'><font name='Helvetica-Bold' size='15' color='white'>K</font>"
        "<font name='Helvetica-Bold' size='15' color='#c9a24b'>S</font>"
        "<font name='Helvetica-Bold' size='15' color='white'>C</font></para>",
        styles['Normal']
    )
    logo_table = Table([[logo_cell]], colWidths=[52], rowHeights=[52])
    logo_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NAVY),
        ('BOX', (0, 0), (-1, -1), 1.4, GOLD),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    header_text_block = [
        Paragraph("KIYA SHOPPING CENTER", business_name_style),
        Paragraph("• CUSTOMER DEBT STATEMENT •", doc_title_style),
        Paragraph("Quality products, trusted service", tagline_style),
    ]

    header_table = Table(
        [[logo_table, header_text_block]],
        colWidths=[70, 430]
    )
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('LEFTPADDING', (0, 0), (0, 0), 0),
    ]))

    story.append(header_table)
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.4, color=GOLD, spaceAfter=14))

    # ---------- Customer Info Block ----------
    story.append(Paragraph("CUSTOMER INFORMATION", section_label_style))
    info_data = [
        [Paragraph("Customer Name", info_label_style), Paragraph(customer.name, info_value_style),
         Paragraph("Statement Date", info_label_style), Paragraph(date.today().strftime('%m/%d/%Y'), info_value_style)],
        [Paragraph("Phone", info_label_style), Paragraph(customer.phone or 'N/A', info_value_style),
         Paragraph("Email", info_label_style), Paragraph(customer.email or 'N/A', info_value_style)],
    ]
    info_table = Table(info_data, colWidths=[85, 155, 85, 175])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 0.75, BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 18))

    # ---------- Transactions Table ----------
    story.append(Paragraph("TRANSACTION HISTORY", section_label_style))

    table_data = [["Date", "Transaction Type", "Amount"]]
    row_styles = []  # track which rows are payments vs debts for coloring
    for idx, rec in enumerate(statement_records, start=1):
        is_payment = rec['amount'] < 0
        amt_str = f"({abs(rec['amount']):,.2f} ETB)" if is_payment else f"{rec['amount']:,.2f} ETB"
        label = rec['type']
        table_data.append([rec['date'], label, amt_str])
        row_styles.append(is_payment)

    if len(statement_records) == 0:
        table_data.append(["-", "No transactions recorded", "0.00 ETB"])
        row_styles.append(False)

    tx_table = Table(table_data, colWidths=[85, 275, 140])
    tx_style = [
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
    ]
    # Color payment rows green, debt rows dark red/navy, for visual distinction only (no logic change)
    for i, is_payment in enumerate(row_styles, start=1):
        if is_payment:
            tx_style.append(('TEXTCOLOR', (2, i), (2, i), GREEN))
            tx_style.append(('FONTNAME', (2, i), (2, i), 'Helvetica-Bold'))
        else:
            tx_style.append(('TEXTCOLOR', (2, i), (2, i), RED))

    tx_table.setStyle(TableStyle(tx_style))
    story.append(tx_table)
    story.append(Spacer(1, 20))

    # ---------- Summary Totals ----------
    story.append(Paragraph("ACCOUNT SUMMARY", section_label_style))
    summary_rows = Table(
        [
            [Paragraph("Total Debt", info_label_style), Paragraph(f"{total_debt:,.2f} ETB", info_value_style)],
            [Paragraph("Total Paid", info_label_style), Paragraph(f"{total_paid:,.2f} ETB", info_value_style)],
        ],
        colWidths=[300, 200]
    )
    summary_rows.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, BORDER),
    ]))
    story.append(summary_rows)
    story.append(Spacer(1, 10))

    # Remaining Debt — most visually prominent
    remaining_box = Table(
        [[Paragraph("REMAINING DEBT", remaining_label_style)],
         [Paragraph(f"{remaining_debt:,.2f} ETB", remaining_value_style)]],
        colWidths=[500]
    )
    remaining_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NAVY),
        ('BOX', (0, 0), (-1, -1), 1.2, GOLD),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 2),
        ('TOPPADDING', (0, 1), (-1, 1), 2),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 12),
    ]))
    story.append(remaining_box)
    story.append(Spacer(1, 36))

    # ---------- Signature Block ----------
    sig_style_script = ParagraphStyle(
        'SigScript', parent=styles['Normal'],
        fontName=signature_font_name, fontSize=16, leading=20,
        textColor=NAVY
    )
    sig_data = [
        [Paragraph("Authorized by:", info_label_style), Paragraph("Signature:", info_label_style)],
        [Paragraph("Owner<br/>KIYA SHOPPING CENTER", info_value_style),
         Paragraph("Kiya S.", sig_style_script)],
        ["", Paragraph("_________________________", info_value_style)],
    ]
    sig_table = Table(sig_data, colWidths=[270, 230])
    sig_table.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(sig_table)
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.75, color=BORDER, spaceAfter=6))
    story.append(Paragraph(
        "This statement is a computer-generated record of account activity and reflects transactions as of the date above.",
        footer_note_style
    ))

    doc.build(story)
    buffer.seek(0)

    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=customer_statement_{customer_id}.pdf'
    return response

@app.route("/customer_debt_statement/<int:customer_id>/share")
@login_required
@emp_allowed
def customer_debt_statement_share(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    pdf_url = url_for('customer_debt_statement', customer_id=customer_id, _external=True)
    return render_template("share_statement.html", customer=customer, pdf_url=pdf_url)





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    # app.run(debug=True, port=5005)