
from datetime import datetime, date
from zoneinfo import ZoneInfo
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from flask import make_response
import io
from decimal import Decimal,InvalidOperation
import os
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO
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
,MultiPurchaseForm,CustomerForm,SupplierForm,SaleForm,LoginForm,RegisterForm,UserEditForm,SupplierEntryForm,StockForm
,CustomerEntryForm,AddDebtForm)
from flask_mail import Mail, Message
from datetime import date, timedelta, datetime







app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','8BYkEfBA6O6donzWlSihBXox7C0sKR6b')
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=365)
app.config['REMEMBER_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_SECURE'] = True
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('shoppingwithkedir@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('nbpe uzrf zxjh dylc')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('shoppingwithkedir@gmail.com')

mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
login_manager=LoginManager()
login_manager.init_app(app)
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'sqlite:///merkato.db'
)

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
    created_at = db.Column(db.DateTime,default=lambda: datetime.now(ZoneInfo("Africa/Addis_Ababa")))
    date = db.Column(db.Date,default=date.today)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("Africa/Addis_Ababa")))
    name = db.Column(db.String(100))
    stock_code = db.Column(db.String(50))
    measurement = db.Column(db.String(20))
    current_quantity = db.Column(db.Float, default=0)
    unit_price = db.Column(db.Float)                       # selling price — unchanged
    purchase_price = db.Column(db.Float, nullable=True)    # NEW — default/cost price, nullable so existing rows are safe
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    purchases = db.relationship('Purchase', backref='product')
    sales = db.relationship('Sale', backref='product')


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("Africa/Addis_Ababa")))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    quantity = db.Column(db.Float)
    unit_price = db.Column(db.Float)
    payment = db.Column(db.Float, default=0)
    debt = db.Column(db.Float, default=0)
    date = db.Column(db.String(20))

    @property
    def total_price(self):
        return self.quantity * self.unit_price


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("Africa/Addis_Ababa")))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    current_payment = db.Column(db.Float, default=0)
    debt = db.Column(db.Float, default=0)
    date = db.Column(db.String(20))


class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )
    created_at = db.Column(db.DateTime,default=lambda: datetime.now(ZoneInfo("Africa/Addis_Ababa")))
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
    created_at = db.Column(db.DateTime,default=lambda: datetime.now(ZoneInfo("Africa/Addis_Ababa")))
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
    created_at = db.Column(db.DateTime,default=lambda: datetime.now(ZoneInfo("Africa/Addis_Ababa")))
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
    created_at = db.Column(db.DateTime,default=lambda: datetime.now(ZoneInfo("Africa/Addis_Ababa")))
    amount = db.Column(db.Float, nullable=False)
    reason = db.Column(db.String(255))
    date = db.Column(db.Date, default=date.today)

class StockAdjustment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    change_type = db.Column(db.String(10))  # 'add' or 'subtract'
    quantity = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product')
    user = db.relationship('User')


class PriceChange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    price_type = db.Column(db.String(10))  # 'selling' or 'purchase'
    old_price = db.Column(db.Float)
    new_price = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product')
    user = db.relationship('User')





with app.app_context():
    db.create_all()




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
        login_user(existing_user,remember=True)
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


@app.route('/new')
@emp_allowed
def new_action():
    return render_template('new_action.html')





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

        for stock in form.stocks.data:

            existing_product = Product.query.filter_by(
                name=stock['stock_name'],
                user_id=current_user.id
            ).first()

            if existing_product:
                flash(f"'{stock['stock_name']}' ቀድሞ ተመዝግቧል።", "danger")
                return redirect(url_for('inventory'))

            new_product = Product(
                name=stock['stock_name'],
                stock_code="",
                measurement="Piece",
                current_quantity=stock['quantity'],
                purchase_price=stock['purchase_price'],   # NEW
                unit_price=stock['unit_price'],
                user_id=current_user.id
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
    form = MultiPurchaseForm()

    product_choices = [(p.id, p.name) for p in Product.query.filter_by(is_deleted=False).all()]
    supplier_choices = [(s.id, s.name) for s in Supplier.query.all()]

    for group in form.groups:
        group.form.supplier.choices = supplier_choices
        for entry in group.form.purchase.entries:
            entry.form.product.choices = product_choices

    if form.validate_on_submit():

        EPSILON = 0.01

        errors_found = False

        for group_index, group in enumerate(form.groups.data, start=1):

            items = group["purchase"]

            if not items:
                continue

            for item in items:

                product = Product.query.get(item["product"])
                product_name = product.name if product else "የተመረጠ ምርት"

                quantity = float(item["quantity"] or 0)
                unit_price = float(item["unit_price"] or 0)

                if quantity <= 0:
                    flash(f"ቡድን #{group_index}: {product_name} - ብዛት ከዜሮ በላይ መሆን አለበት።", "danger")
                    errors_found = True

                if unit_price <= 0:
                    flash(f"ቡድን #{group_index}: {product_name} - ዋጋ ከዜሮ በላይ መሆን አለበት።", "danger")
                    errors_found = True

            overall_payment = float(group["payment"] or 0)

            if overall_payment < 0:
                flash(f"ቡድን #{group_index}: የክፍያ መጠን አሉታዊ ሊሆን አይችልም።", "danger")
                errors_found = True

        if errors_found:
            purchases_list = Purchase.query.all()
            return render_template(
                "purchase.html",
                form=form,
                purchases=purchases_list,
                products=Product.query.all(),   # ADDED
                user_id=current_user.id
            )

        groups_saved = 0

        for group in form.groups.data:

            supplier_id = group["supplier"]
            items = group["purchase"]

            if not items:
                continue

            grand_total = 0.0
            for item in items:
                grand_total += float(item["quantity"]) * float(item["unit_price"])

            overall_payment = float(group["payment"] or 0)

            if overall_payment > grand_total:
                overall_payment = grand_total

            remaining_payment = overall_payment

            for item in items:

                quantity = float(item["quantity"])
                unit_price = float(item["unit_price"])

                total = quantity * unit_price

                item_payment = min(remaining_payment, total)
                item_debt = max(total - item_payment, 0)

                if abs(item_debt) < EPSILON:
                    item_debt = 0.0

                new_purchase = Purchase(
                    product_id=item["product"],
                    supplier_id=supplier_id,
                    quantity=quantity,
                    unit_price=unit_price,
                    payment=item_payment,
                    debt=item_debt,
                    date=date.today().strftime("%m/%d/%Y"),
                    user_id=current_user.id
                )

                db.session.add(new_purchase)

                product = Product.query.get(item["product"])
                if product:
                    product.current_quantity += quantity

                remaining_payment -= item_payment

            groups_saved += 1

        db.session.commit()

        if groups_saved:
            flash(f"{groups_saved} ግዢ(ዎች) በተሳካ ሁኔታ ተመዝግበዋል።", "success")
        else:
            flash("ምንም ትክክለኛ ግዢ አልተመዘገበም። እባክዎ ቢያንስ አንድ ምርት ይምረጡ።", "warning")

        return redirect(url_for("purchases"))

    else:
        print("FORM ERRORS:", form.errors)
        if request.method == "POST":
            flash("እባክዎ ከታች ያሉትን ስህተቶች ያስተካክሉ እና እንደገና ይሞክሩ።", "danger")

    purchases_list = Purchase.query.all()

    return render_template(
        "purchase.html",
        form=form,
        purchases=purchases_list,
        products=Product.query.all(),   # ADDED
        user_id=current_user.id
    )








from decimal import Decimal, InvalidOperation


@app.route("/detail")
@login_required
@emp_allowed
def detail():

    # ---------------------------------------------------------
    # Get all supplier IDs from purchases
    # ---------------------------------------------------------
    purchase_supplier_ids = (
        db.session.query(Purchase.supplier_id)
        .filter(Purchase.supplier_id.isnot(None))
        .distinct()
        .all()
    )

    supplier_ids = {
        row[0]
        for row in purchase_supplier_ids
    }

    # ---------------------------------------------------------
    # Also include suppliers with balance_owed
    # (kept, same as AddDebt is kept for customers)
    # ---------------------------------------------------------
    suppliers = db.session.execute(
        db.select(Supplier)
    ).scalars().all()

    for supplier in suppliers:

        balance_owed = Decimal(
            str(supplier.balance_owed or 0)
        )

        if balance_owed > Decimal("0"):
            supplier_ids.add(supplier.id)

    supplier_details = []

    grand_total_debt = Decimal("0")

    # ---------------------------------------------------------
    # Calculate each supplier — rebuilt from raw purchase totals,
    # same approach as customer_detail, NOT from Purchase.debt
    # ---------------------------------------------------------
    for supplier_id in supplier_ids:

        supplier = db.session.get(
            Supplier,
            supplier_id
        )

        if not supplier:
            continue

        # -----------------------------------------------------
        # TOTAL PURCHASED (purchases) — rebuilt from quantity x
        # unit_price, not from Purchase.debt
        # -----------------------------------------------------
        purchases = Purchase.query.filter_by(
            supplier_id=supplier_id
        ).all()

        total_purchased_via_purchases = sum(
            (
                Decimal(str(p.quantity or 0)) * Decimal(str(p.unit_price or 0))
            )
            for p in purchases
        )

        # Payments already recorded AT the time of purchase
        payments_at_purchase_time = sum(
            (
                Decimal(str(p.payment or 0))
            )
            for p in purchases
        )

        # -----------------------------------------------------
        # ADDITIONAL BALANCE OWED — treated like AddDebt on the
        # customer side: a separate manual debt entry, never
        # itself reduced by SupplierPayment (confirm this holds
        # true in your app before trusting it long-term)
        # -----------------------------------------------------
        balance_owed = Decimal(
            str(supplier.balance_owed or 0)
        )

        if balance_owed < 0:
            balance_owed = Decimal("0")

        # -----------------------------------------------------
        # TOTAL DEBT (everything ever owed, before later payments)
        # -----------------------------------------------------
        total_debt = total_purchased_via_purchases + balance_owed

        # -----------------------------------------------------
        # LATER PAYMENTS (SupplierPayment table — paid after
        # the purchase was recorded)
        # -----------------------------------------------------
        later_payments = SupplierPayment.query.filter_by(
            supplier_id=supplier_id
        ).all()

        total_later_payments = sum(
            (
                Decimal(str(p.amount or 0))
            )
            for p in later_payments
            if (p.amount or 0) > 0
        )

        # -----------------------------------------------------
        # TOTAL PAID = payments made at purchase time + payments
        # made later
        # -----------------------------------------------------
        total_paid = payments_at_purchase_time + total_later_payments

        # -----------------------------------------------------
        # REMAINING DEBT
        # -----------------------------------------------------
        remaining_debt = max(
            total_debt - total_paid,
            Decimal("0")
        )

        # -----------------------------------------------------
        # Only show suppliers who still owe money
        # -----------------------------------------------------
        if remaining_debt > Decimal("0"):

            supplier_details.append({
                "supplier_id": supplier.id,
                "supplier_name": supplier.name or "Unknown",
                "total_debt": total_debt,
                "total_paid": total_paid,
                "remaining_debt": remaining_debt
            })

            grand_total_debt += remaining_debt

    # Highest debt first
    supplier_details.sort(
        key=lambda x: x["remaining_debt"],
        reverse=True
    )

    return render_template(
        "detail.html",
        supplier_details=supplier_details,
        grand_total_debt=grand_total_debt,
        user_id=current_user.id
    )
# =============================================================
# PAY SUPPLIER DEBT
# =============================================================

@app.route("/pay_debt", methods=["POST"])
@login_required
@emp_allowed
def pay_debt():

    supplier_id = request.form.get(
        "supplier_id",
        type=int
    )

    amount_raw = request.form.get("amount")

    # ---------------------------------------------------------
    # Validate supplier ID
    # ---------------------------------------------------------
    if not supplier_id:
        flash(
            "Invalid supplier.",
            "danger"
        )
        return redirect(url_for("detail"))

    # ---------------------------------------------------------
    # Convert payment to Decimal
    # ---------------------------------------------------------
    try:

        amount = Decimal(
            str(amount_raw)
        )

    except (InvalidOperation, TypeError, ValueError):

        flash(
            "Invalid payment amount.",
            "danger"
        )

        return redirect(url_for("detail"))

    # ---------------------------------------------------------
    # Payment must be positive
    # ---------------------------------------------------------
    if amount <= Decimal("0"):

        flash(
            "Payment amount must be greater than zero.",
            "danger"
        )

        return redirect(url_for("detail"))

    # ---------------------------------------------------------
    # Get supplier
    # ---------------------------------------------------------
    supplier = db.session.get(
        Supplier,
        supplier_id
    )

    if not supplier:

        flash(
            "Supplier not found.",
            "danger"
        )

        return redirect(url_for("detail"))

    # ---------------------------------------------------------
    # Calculate purchase debt
    # ---------------------------------------------------------
    purchases = Purchase.query.filter_by(
        supplier_id=supplier_id
    ).all()

    purchase_debt = Decimal("0")

    for purchase in purchases:

        debt = Decimal(
            str(purchase.debt or 0)
        )

        if debt > 0:
            purchase_debt += debt

    # ---------------------------------------------------------
    # Additional supplier balance
    # ---------------------------------------------------------
    balance_owed = Decimal(
        str(supplier.balance_owed or 0)
    )

    if balance_owed < 0:
        balance_owed = Decimal("0")

    # ---------------------------------------------------------
    # Total debt
    # ---------------------------------------------------------
    total_debt = (
        purchase_debt
        + balance_owed
    )

    # ---------------------------------------------------------
    # Existing payments
    # ---------------------------------------------------------
    payments = SupplierPayment.query.filter_by(
        supplier_id=supplier_id
    ).all()

    total_paid = Decimal("0")

    for payment in payments:

        paid = Decimal(
            str(payment.amount or 0)
        )

        if paid > 0:
            total_paid += paid

    # ---------------------------------------------------------
    # Remaining debt
    # ---------------------------------------------------------
    remaining_debt = (
        total_debt
        - total_paid
    )

    if remaining_debt < Decimal("0"):
        remaining_debt = Decimal("0")

    # ---------------------------------------------------------
    # Prevent overpayment
    # ---------------------------------------------------------
    if amount > remaining_debt:

        flash(
            f"Payment cannot be greater than the "
            f"remaining debt "
            f"({remaining_debt:,.2f} ETB).",
            "danger"
        )

        return redirect(
            url_for("detail")
        )

    # ---------------------------------------------------------
    # Create payment
    # ---------------------------------------------------------
    new_payment = SupplierPayment(
        supplier_id=supplier_id,
        amount=amount,
        date=date.today(),
        user_id=current_user.id
    )

    db.session.add(new_payment)

    try:

        db.session.commit()

    except Exception:

        db.session.rollback()

        flash(
            "Payment could not be recorded.",
            "danger"
        )

        return redirect(
            url_for("detail")
        )

    flash(
        "Payment recorded successfully.",
        "success"
    )

    return redirect(
        url_for("detail")
    )

@app.route("/history")
@login_required
@admin_only
def history():

    return render_template(
        "history.html" )





@app.route("/track")
@login_required
def track():
    return render_template("track.html")




@app.route("/suppliers_customers")
@login_required
@emp_allowed
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
        customers=customers,
        user_id=current_user.id
    )


@app.route("/register_customer_and_supplier", methods=["GET", "POST"])
@login_required
@emp_allowed
def Register_customer_and_supplier():
    supplier_form = SupplierForm()
    customer_form = CustomerForm()

    if customer_form.validate_on_submit():
        try:
            for customer in customer_form.customers.data:
                new_customer = Customer(
                    name=customer['name'],
                    phone=customer['phone'],
                    user_id=current_user.id
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
                    user_id=current_user.id
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



from decimal import Decimal

@app.route("/selling", methods=["GET", "POST"])
@login_required
@emp_allowed
def Selling():

    sale_form = SaleForm()

    # Choices MUST be repopulated before validation
    products = Product.query.filter_by(is_deleted=False).all()
    customers = Customer.query.all()

    product_choices = [(p.id, p.name) for p in products]
    customer_choices = [(c.id, c.name) for c in customers]

    for entry in sale_form.sales:
        entry.form.product_id.choices = product_choices
        entry.form.customer_id.choices = customer_choices

    if sale_form.validate_on_submit():
        print("he")

        # ==========================================================
        # PASS 1: Validate the entire batch before changing anything
        # ==========================================================

        errors_found = False
        requested_quantities = {}

        for entry in sale_form.sales.data:

            product = db.session.get(
                Product,
                entry["product_id"]
            )

            if not product:
                flash(
                    "Selected product not found.",
                    "danger"
                )
                errors_found = True
                continue

            quantity = entry["quantity"]

            # Quantity must be positive
            if quantity <= 0:
                flash(
                    f"Quantity for {product.name} must be greater than zero.",
                    "danger"
                )
                errors_found = True
                continue

            if product.id not in requested_quantities:
                requested_quantities[product.id] = 0

            requested_quantities[product.id] += quantity

        # ----------------------------------------------------------
        # Check total requested quantity for every product
        # ----------------------------------------------------------

        for product_id, total_requested in requested_quantities.items():

            product = db.session.get(
                Product,
                product_id
            )

            if not product:
                errors_found = True
                continue

            if total_requested > product.current_quantity:

                flash(
                    f"Insufficient stock for {product.name}. "
                    f"Only {product.current_quantity} available, "
                    f"but {total_requested} requested.",
                    "danger"
                )

                errors_found = True

        # If ANY error exists, save NOTHING
        if errors_found:

            return render_template(
                "selling.html",
                sale_form=sale_form,
                products=products,
                customers=customers
            )

        # ==========================================================
        # PASS 2: Validate payments before creating sales
        # ==========================================================

        for entry in sale_form.sales.data:

            product = db.session.get(
                Product,
                entry["product_id"]
            )

            if not product:
                flash(
                    "Selected product not found.",
                    "danger"
                )

                return render_template(
                    "selling.html",
                    sale_form=sale_form,
                    products=products,
                    customers=customers
                )

            quantity = entry["quantity"]

            # Convert to Decimal for money calculations
            unit_price = Decimal(
                str(entry["unit_price"] or 0)
            )

            payment = Decimal(
                str(entry["current_payment"] or 0)
            )

            # ------------------------------------------------------
            # Validate price
            # ------------------------------------------------------

            if unit_price < Decimal("0"):

                flash(
                    f"Unit price for {product.name} "
                    f"cannot be negative.",
                    "danger"
                )

                return render_template(
                    "selling.html",
                    sale_form=sale_form,
                    products=products,
                    customers=customers
                )

            # ------------------------------------------------------
            # Validate payment
            # ------------------------------------------------------

            if payment < Decimal("0"):

                flash(
                    f"Payment for {product.name} "
                    f"cannot be negative.",
                    "danger"
                )

                return render_template(
                    "selling.html",
                    sale_form=sale_form,
                    products=products,
                    customers=customers
                )

            # ------------------------------------------------------
            # Calculate sale total
            # ------------------------------------------------------

            total_amount = (
                Decimal(str(quantity)) * unit_price
            )

            # ------------------------------------------------------
            # Payment cannot exceed sale total
            # ------------------------------------------------------

            if payment > total_amount:

                flash(
                    f"Payment for {product.name} cannot be greater "
                    f"than the sale total "
                    f"({total_amount:,.2f} ETB).",
                    "danger"
                )

                return render_template(
                    "selling.html",
                    sale_form=sale_form,
                    products=products,
                    customers=customers
                )

        # ==========================================================
        # PASS 3: Everything is valid - create sales
        # ==========================================================

        try:

            for entry in sale_form.sales.data:

                product = db.session.get(
                    Product,
                    entry["product_id"]
                )

                quantity = entry["quantity"]

                unit_price = Decimal(
                    str(entry["unit_price"] or 0)
                )

                payment = Decimal(
                    str(entry["current_payment"] or 0)
                )

                total_amount = (
                    Decimal(str(quantity)) * unit_price
                )

                debt = total_amount - payment

                # Extra safety
                debt = max(
                    debt,
                    Decimal("0")
                )

                new_sale = Sale(
                    product_id=entry["product_id"],
                    customer_id=entry["customer_id"],
                    quantity=quantity,
                    unit_price=unit_price,
                    current_payment=payment,
                    debt=debt,
                    date=date.today().strftime("%m/%d/%Y"),
                    user_id=current_user.id
                )

                db.session.add(new_sale)

                # Deduct stock
                product.current_quantity -= quantity

            # Save everything together
            db.session.commit()

        except Exception:

            db.session.rollback()

            flash(
                "The sale could not be recorded. "
                "Nothing was saved.",
                "danger"
            )

            return render_template(
                "selling.html",
                sale_form=sale_form,
                products=products,
                customers=customers
            )

        flash(
            "Sale(s) recorded successfully.",
            "success"
        )

        return redirect(
            url_for("Selling")
        )

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
        for row in db.session.query(Sale.customer_id)
        .filter(Sale.customer_id.isnot(None))
        .distinct()
    ]

    debt_customer_ids = [
        row[0]
        for row in db.session.query(AddDebt.customer_id)
        .filter(AddDebt.customer_id.isnot(None))
        .distinct()
    ]

    customer_ids = list(
        set(sale_customer_ids) | set(debt_customer_ids)
    )

    customer_details = []

    grand_total_debt = Decimal("0")

    for customer_id in customer_ids:

        # ==========================================================
        # Rebuild total sold and total paid from raw transactions —
        # NOT from Sale.debt, since that field goes stale the
        # moment a later CustomerPayment comes in (confirmed earlier).
        # ==========================================================

        # -------------------------
        # TOTAL SOLD (sales)
        # -------------------------
        sales = Sale.query.filter_by(
            customer_id=customer_id
        ).all()

        total_sold_via_sales = sum(
            (
                Decimal(str(s.quantity or 0)) * Decimal(str(s.unit_price or 0))
            )
            for s in sales
        )

        # Payments already recorded AT the time of sale
        payments_at_sale_time = sum(
            (
                Decimal(str(s.current_payment or 0))
            )
            for s in sales
        )

        # -------------------------
        # ADDITIONAL DEBT
        # -------------------------
        additional_debt_records = AddDebt.query.filter_by(
            customer_id=customer_id
        ).all()

        additional_debt = sum(
            (
                Decimal(str(d.amount or 0))
            )
            for d in additional_debt_records
        )

        # -------------------------
        # TOTAL DEBT (everything ever owed, before any later payment)
        # -------------------------
        total_debt = total_sold_via_sales + additional_debt

        # -------------------------
        # LATER PAYMENTS (CustomerPayment table — paid after the sale)
        # -------------------------
        later_payments = CustomerPayment.query.filter_by(
            customer_id=customer_id
        ).all()

        total_later_payments = sum(
            (
                Decimal(str(p.amount or 0))
            )
            for p in later_payments
        )

        # -------------------------
        # TOTAL PAID = payments made at sale time + payments made later
        # -------------------------
        total_paid = payments_at_sale_time + total_later_payments

        # -------------------------
        # REMAINING DEBT — single source of truth, matches the
        # statement page exactly since both rebuild from raw data
        # -------------------------
        remaining_debt = max(
            total_debt - total_paid,
            Decimal("0")
        )

        # -------------------------
        # CUSTOMER
        # -------------------------
        customer = db.get_or_404(
            Customer,
            customer_id
        )

        customer_details.append({
            "customer_id": customer_id,
            "customer_name": customer.name,
            "total_debt": total_debt,
            "total_paid": total_paid,
            "remaining_debt": remaining_debt
        })

        grand_total_debt += remaining_debt

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

    customer_id = request.form.get(
        "customer_id",
        type=int
    )

    amount = request.form.get(
        "amount",
        type=float
    )

    # -------------------------
    # BASIC VALIDATION
    # -------------------------

    if not customer_id or amount is None or amount <= 0:

        flash(
            "Invalid payment details.",
            "danger"
        )

        return redirect(
            url_for("customer_detail")
        )

    # -------------------------
    # CALCULATE SALES DEBT
    # -------------------------

    sales = Sale.query.filter_by(
        customer_id=customer_id
    ).all()

    sales_debt = sum(
        max(float(s.debt or 0), 0)
        for s in sales
    )

    # -------------------------
    # CALCULATE ADDITIONAL DEBT
    # -------------------------

    additional_debt_records = AddDebt.query.filter_by(
        customer_id=customer_id
    ).all()

    additional_debt = sum(
        max(float(d.amount or 0), 0)
        for d in additional_debt_records
    )

    # -------------------------
    # TOTAL DEBT
    # -------------------------

    total_debt = sales_debt + additional_debt

    # -------------------------
    # PREVIOUS PAYMENTS
    # -------------------------

    payments = CustomerPayment.query.filter_by(
        customer_id=customer_id
    ).all()

    total_paid = sum(
        max(float(p.amount or 0), 0)
        for p in payments
    )

    # -------------------------
    # CURRENT REMAINING DEBT
    # -------------------------

    remaining_debt = max(
        total_debt - total_paid,
        0
    )

    # -------------------------
    # DO NOT ALLOW OVERPAYMENT
    # -------------------------

    if amount > remaining_debt:

        flash(
            f"Payment cannot exceed the remaining debt of "
            f"{remaining_debt:.2f} ETB.",
            "danger"
        )

        return redirect(
            url_for("customer_detail")
        )

    # -------------------------
    # SAVE PAYMENT
    # -------------------------

    new_payment = CustomerPayment(
        customer_id=customer_id,
        amount=amount,
        date=date.today(),
        user_id=current_user.id
    )

    db.session.add(new_payment)
    db.session.commit()

    flash(
        "Payment recorded successfully.",
        "success"
    )

    return redirect(
        url_for("customer_detail")
    )

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


        if form.validate_on_submit():
            customer.name = form.name.data
            customer.phone = form.phone.data


            db.session.commit()

            flash("Customer updated successfully.", "success")
            return redirect(url_for("customers_page"))

        return render_template(
            "edit.html",
            form=form,
            item_type="customer",
            title="Edit Customer",
            user_id=current_user.id
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

        if form.validate_on_submit():
            supplier.name = form.name.data
            supplier.phone = form.phone.data

            db.session.commit()

            flash("Supplier updated successfully.", "success")
            return redirect(url_for("suppliers_page"))

        return render_template(
            "edit.html",
            form=form,
            item_type="supplier",
            title="Edit Supplier",
            user_id=current_user.id
        )

    # --------------------------------
    # --------------------------------
    # PRODUCT
    # --------------------------------
    elif item_type == "product":

        product = db.get_or_404(Product, item_id)
        form = StockForm()

        if request.method == "GET":
            form.stock_name.data = product.name
            form.quantity.data = product.current_quantity
            form.purchase_price.data = product.purchase_price  # NEW
            form.unit_price.data = product.unit_price

        if form.validate_on_submit():
            product.name = form.stock_name.data
            product.current_quantity = form.quantity.data
            product.purchase_price = form.purchase_price.data  # NEW
            product.unit_price = form.unit_price.data

            db.session.commit()

            flash("Product updated successfully.", "success")
            return redirect(url_for("products_page"))

        return render_template(
            "edit.html",
            form=form,
            item_type="product",
            title="Edit Product",
            user_id=current_user.id
        )

# --------------------------------
# INVALID TYPE
# --------------------------------

    flash("Invalid item type.", "danger")
    return redirect(url_for("home"))



@app.route("/delete/<string:item_type>/<int:item_id>", methods=["POST"])
@login_required
@admin_only
def delete(item_type, item_id):

    # ==========================================
    # CUSTOMER
    # ==========================================
    if item_type == "customer":

        customer = Customer.query.filter_by(
            id=item_id
        ).first_or_404()

        # Delete customer's sales
        Sale.query.filter_by(
            customer_id=customer.id
        ).delete()

        # Delete customer's payments
        CustomerPayment.query.filter_by(
            customer_id=customer.id
        ).delete()

        # Delete customer's added debts
        AddDebt.query.filter_by(
            customer_id=customer.id
        ).delete()

        # Delete customer
        db.session.delete(customer)

        db.session.commit()

        flash("ደንበኛው እና ተያያዥ መረጃዎቹ ተሰርዘዋል።", "success")
        return redirect(url_for("customers_page"))


    # ==========================================
    # SUPPLIER
    # ==========================================
    elif item_type == "supplier":

        supplier = Supplier.query.filter_by(
            id=item_id
        ).first_or_404()

        # Delete supplier purchases
        Purchase.query.filter_by(
            supplier_id=supplier.id
        ).delete()

        # Delete supplier payments
        SupplierPayment.query.filter_by(
            supplier_id=supplier.id
        ).delete()

        # Delete supplier
        db.session.delete(supplier)

        db.session.commit()

        flash("አቅራቢው እና ተያያዥ መረጃዎቹ ተሰርዘዋል።", "success")
        return redirect(url_for("suppliers_page"))


    # ==========================================
    # PRODUCT
    # ==========================================
    elif item_type == "product":
        product = Product.query.get_or_404(item_id)
        product.is_deleted = True
        db.session.commit()
        flash('ምርቱ ተሰርዟል', 'success')
        return redirect(url_for('products_page'))


    # ==========================================
    # WRONG TYPE
    # ==========================================
    else:
        flash("ያልታወቀ የመረጃ አይነት ነው።", "danger")


    return redirect(url_for("products_page"))




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
@admin_only
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
@admin_only
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

#
@app.route("/users/delete/<int:user_id>", methods=["POST"])
@login_required
@admin_only
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    # if user.email == 'kedirmuhammed323@gmail.com':
    #     flash("who are you to do that? ","success")
    #         return redirect(url_for("users"))

    if user.id == current_user.id:
        flash("You can't delete your own account while logged in.", "danger")
        return redirect(url_for("users"))

    # Keep business records, but disconnect them from this user
    CustomerPayment.query.filter_by(user_id=user.id).update(
        {"user_id": None}
    )

    Product.query.filter_by(user_id=user.id).update(
        {"user_id": None}
    )

    Purchase.query.filter_by(user_id=user.id).update(
        {"user_id": None}
    )

    Sale.query.filter_by(user_id=user.id).update(
        {"user_id": None}
    )

    Supplier.query.filter_by(user_id=user.id).update(
        {"user_id": None}
    )

    SupplierPayment.query.filter_by(user_id=user.id).update(
        {"user_id": None}
    )

    Customer.query.filter_by(user_id=user.id).update(
        {"user_id": None}
    )

    # ActivityReset cannot have NULL user_id, so remove only this tracking record
    ActivityReset.query.filter_by(user_id=user.id).delete()

    # Now it is safe to delete the user
    db.session.delete(user)
    db.session.commit()

    flash("User deleted successfully.", "success")
    return redirect(url_for("users"))






from sqlalchemy import func

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

    # ================= PROFIT (real, based on actual sales vs. average cost) =================
    # For each product sold today, cost basis = average unit_price paid across ALL of that
    # product's purchases (not just today's), since stock sold today may have been bought earlier.
    sold_product_ids = {s.product_id for s in sales}
    avg_cost_by_product = {}

    for pid in sold_product_ids:
        cost_sum, qty_sum = db.session.query(
            func.sum(Purchase.quantity * Purchase.unit_price),
            func.sum(Purchase.quantity)
        ).filter(Purchase.product_id == pid).first()

        if qty_sum:
            # Real purchase history exists — use it, unchanged
            avg_cost_by_product[pid] = (cost_sum or 0) / qty_sum
        else:
            # Never purchased — use the product's saved default cost instead of 0
            product = db.session.get(Product, pid)
            avg_cost_by_product[pid] = (product.purchase_price or 0) if product else 0


    total_cost_of_goods_sold = 0
    for s in sales:
        avg_cost = avg_cost_by_product.get(s.product_id, 0)
        total_cost_of_goods_sold += (s.quantity or 0) * avg_cost

    total_profit = total_sales_revenue - total_cost_of_goods_sold

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

        total_cost_of_goods_sold=total_cost_of_goods_sold,
        total_profit=total_profit,

        daily_financial_activity=daily_financial_activity
    )


from datetime import datetime, date, timedelta

@app.route("/dashboard")
@login_required
@admin_only
def dashboard():
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
    today = date.today()
    yesterday = today - timedelta(days=1)

    def day_label(dt):
        d = dt.date()
        if d == today:
            return "ዛሬ"
        elif d == yesterday:
            return "ትናንት"
        return dt.strftime("%d %b %Y")

    def time_label(dt, has_real_time):
        if not has_real_time:
            return None
        return dt.strftime("%I:%M%p").lower().lstrip("0")

    # =========================================================
    # PURCHASES
    # =========================================================
    purchases = Purchase.query.order_by(Purchase.id.desc()).all()

    for p in purchases:
        if p.id <= last_purchase_cutoff:
            continue

        try:
            p_date = datetime.strptime(p.date.strip(), "%m/%d/%Y")
        except (ValueError, TypeError, AttributeError):
            continue

        has_time = bool(getattr(p, "created_at", None))
        sort_dt = p.created_at if has_time else p_date

        product = Product.query.get(p.product_id)
        supplier = Supplier.query.get(p.supplier_id)
        user = User.query.get(p.user_id) if p.user_id else None

        activities.append({
            "type": "purchase",
            "icon": "bi-cart-plus",
            "direction": "out",
            "product_name": product.name if product else "ያልታወቀ ምርት",
            "quantity": p.quantity,
            "measurement": product.measurement if product and product.measurement else "",
            "counterparty_role": "አቅራቢ",
            "counterparty_name": supplier.name if supplier else "ያልታወቀ አቅራቢ",
            "money_label": "የተከፈለ",
            "amount": p.payment,
            "user_name": user.name if user else "ያልታወቀ ተጠቃሚ",
            "day_label": day_label(sort_dt),
            "time_label": time_label(sort_dt, has_time),
            "sort_key": sort_dt
        })

    # =========================================================
    # SALES
    # =========================================================
    sales = Sale.query.order_by(Sale.id.desc()).all()

    for s in sales:
        if s.id <= last_sale_cutoff:
            continue

        try:
            s_date = datetime.strptime(s.date.strip(), "%m/%d/%Y")
        except (ValueError, TypeError, AttributeError):
            continue

        has_time = bool(getattr(s, "created_at", None))
        sort_dt = s.created_at if has_time else s_date

        product = Product.query.get(s.product_id)
        customer = Customer.query.get(s.customer_id)
        user = User.query.get(s.user_id) if s.user_id else None

        activities.append({
            "type": "sale",
            "icon": "bi-bag-check",
            "direction": "in",
            "product_name": product.name if product else "ያልታወቀ ምርት",
            "quantity": s.quantity,
            "measurement": product.measurement if product and product.measurement else "",
            "counterparty_role": "ደንበኛ",
            "counterparty_name": customer.name if customer else "ያልታወቀ ደንበኛ",
            "money_label": "የተቀበለ",
            "amount": s.current_payment,
            "user_name": user.name if user else "ያልታወቀ ተጠቃሚ",
            "day_label": day_label(sort_dt),
            "time_label": time_label(sort_dt, has_time),
            "sort_key": sort_dt
        })

    # =========================================================
    # SUPPLIER PAYMENTS
    # =========================================================
    supplier_payments = SupplierPayment.query.order_by(SupplierPayment.id.desc()).all()

    for sp in supplier_payments:
        if sp.id <= last_supplier_payment_cutoff:
            continue

        has_time = bool(getattr(sp, "created_at", None))
        sort_dt = sp.created_at if has_time else datetime.combine(sp.date, datetime.min.time())

        supplier = Supplier.query.get(sp.supplier_id)
        user = User.query.get(sp.user_id) if sp.user_id else None

        activities.append({
            "type": "supplier_payment",
            "icon": "bi-cash-stack",
            "direction": "out",
            "product_name": None,
            "quantity": None,
            "measurement": None,
            "counterparty_role": "አቅራቢ",
            "counterparty_name": supplier.name if supplier else "ያልታወቀ አቅራቢ",
            "money_label": None,
            "amount": sp.amount,
            "user_name": user.name if user else "ያልታወቀ ተጠቃሚ",
            "day_label": day_label(sort_dt),
            "time_label": time_label(sort_dt, has_time),
            "sort_key": sort_dt
        })

    # =========================================================
    # CUSTOMER PAYMENTS
    # =========================================================
    customer_payments = CustomerPayment.query.order_by(CustomerPayment.id.desc()).all()

    for cp in customer_payments:
        if cp.id <= last_customer_payment_cutoff:
            continue

        has_time = bool(getattr(cp, "created_at", None))
        sort_dt = cp.created_at if has_time else datetime.combine(cp.date, datetime.min.time())

        customer = Customer.query.get(cp.customer_id)
        user = User.query.get(cp.user_id) if cp.user_id else None

        activities.append({
            "type": "customer_payment",
            "icon": "bi-wallet2",
            "direction": "in",
            "product_name": None,
            "quantity": None,
            "measurement": None,
            "counterparty_role": "ደንበኛ",
            "counterparty_name": customer.name if customer else "ያልታወቀ ደንበኛ",
            "money_label": None,
            "amount": cp.amount,
            "user_name": user.name if user else "ያልታወቀ ተጠቃሚ",
            "day_label": day_label(sort_dt),
            "time_label": time_label(sort_dt, has_time),
            "sort_key": sort_dt
        })

    # =========================================================
    # SORT + GROUP BY DAY
    # =========================================================
    activities.sort(key=lambda x: x["sort_key"], reverse=True)

    grouped_activities = []
    seen_labels = []
    for act in activities:
        if act["day_label"] not in seen_labels:
            seen_labels.append(act["day_label"])
            grouped_activities.append({"day_label": act["day_label"], "items": [act]})
        else:
            grouped_activities[-1]["items"].append(act)

    return render_template(
        "dashboard.html",
        grouped_activities=grouped_activities,
        recent_activities=activities
    )


@app.route("/reset_activity", methods=["POST"])
@login_required
@admin_only
def reset_activity():
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
        return redirect(url_for('customers_page'))

    return render_template("add_debt.html", form=form, customer=customer)





from io import BytesIO
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont

@app.route("/customer_debt_statement/<int:customer_id>")
@login_required
@admin_only
def customer_debt_statement(customer_id):
    customer = db.get_or_404(Customer, customer_id)

    sales = Sale.query.filter_by(customer_id=customer_id).all()
    additional_debts = AddDebt.query.filter_by(customer_id=customer_id).all()
    payments = CustomerPayment.query.filter_by(customer_id=customer_id).all()

    # ---------- Build unified transaction timeline ----------
    statement_records = []

    for sale in sales:
        statement_records.append({
            "date": sale.date or "",
            "type": "sale",
            "product_name": sale.product.name if sale.product else "Unknown Product",
            "quantity": sale.quantity or 0,
            "unit_price": sale.unit_price or 0,
            "amount": sale.debt or 0,
            "sort_key": str(sale.date or "")
        })

    for debt in additional_debts:
        statement_records.append({
            "date": debt.date.strftime("%m/%d/%Y") if isinstance(debt.date, date) else str(debt.date),
            "type": "additional_debt",
            "reason": debt.reason or "General",
            "amount": debt.amount or 0,
            "sort_key": str(debt.date)
        })

    for payment in payments:
        statement_records.append({
            "date": payment.date.strftime("%m/%d/%Y") if isinstance(payment.date, date) else str(payment.date),
            "type": "payment",
            "amount": -(payment.amount or 0),
            "sort_key": str(payment.date)
        })

    statement_records.sort(key=lambda x: x["sort_key"])

    # ---------- Running balance + paid-in-full detection ----------
    running_balance = 0
    paid_in_full_dates = []

    for rec in statement_records:
        running_balance += rec["amount"]
        if running_balance < 0:
            running_balance = 0
        rec["running_balance"] = running_balance
        if running_balance == 0:
            paid_in_full_dates.append(rec["date"])

    total_debt = sum(r["amount"] for r in statement_records if r["amount"] > 0)
    total_paid = sum(-r["amount"] for r in statement_records if r["amount"] < 0)
    remaining_debt = max(running_balance, 0)

    # ---------- PDF GENERATION ----------
    buffer = BytesIO()
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

    signature_font_name = "Helvetica-Oblique"
    try:
        registerFont(TTFont('SignatureFont', '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf'))
        signature_font_name = "SignatureFont"
    except Exception:
        pass

    business_name_style = ParagraphStyle(
        'BusinessName', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=17, leading=20,
        alignment=TA_CENTER, textColor=NAVY, spaceAfter=2
    )
    doc_title_style = ParagraphStyle(
        'DocTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=13,
        alignment=TA_CENTER, textColor=GOLD
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
    paid_flag_style = ParagraphStyle(
        'PaidFlag', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=6.5, leading=8,
        textColor=RED
    )
    small_note_style = ParagraphStyle(
        'SmallNote', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7.5, leading=10,
        textColor=RED
    )

    # ---------- Logo ----------
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

    header_table = Table([[logo_table, header_text_block]], colWidths=[70, 430])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('LEFTPADDING', (0, 0), (0, 0), 0),
    ]))

    story.append(header_table)
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.4, color=GOLD, spaceAfter=14))

    # ---------- Customer Info ----------
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

    # ---------- Transaction History ----------
    story.append(Paragraph("TRANSACTION HISTORY", section_label_style))

    table_data = [["Date", "Transaction Type", "Amount", "Balance"]]
    row_is_payment = []
    row_is_paid_off = []

    for rec in statement_records:
        is_payment = rec["amount"] < 0
        amt_str = f"({abs(rec['amount']):,.2f} ETB)" if is_payment else f"{rec['amount']:,.2f} ETB"

        if rec["type"] == "sale":
            type_str = f"Product Sale — {rec['product_name']} ({rec['quantity']:g} × {rec['unit_price']:,.2f} ETB)"
        elif rec["type"] == "additional_debt":
            type_str = f"Additional Debt ({rec['reason']})"
        else:
            type_str = "Payment"

        is_paid_off = rec["running_balance"] == 0

        balance_cell = Paragraph(
            f"{rec['running_balance']:,.2f} ETB" + ("<br/><font color='#b91c1c'>✓ PAID IN FULL</font>" if is_paid_off else ""),
            paid_flag_style if is_paid_off else info_value_style
        )

        table_data.append([rec["date"], type_str, amt_str, balance_cell])
        row_is_payment.append(is_payment)
        row_is_paid_off.append(is_paid_off)

    if len(statement_records) == 0:
        table_data.append(["-", "No transactions recorded", "0.00 ETB", "0.00 ETB"])
        row_is_payment.append(False)
        row_is_paid_off.append(False)

    tx_table = Table(table_data, colWidths=[70, 235, 100, 95])
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
        ('ALIGN', (2, 0), (3, -1), 'RIGHT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
    ]
    for i, is_payment in enumerate(row_is_payment, start=1):
        if is_payment:
            tx_style.append(('TEXTCOLOR', (2, i), (2, i), GREEN))
            tx_style.append(('FONTNAME', (2, i), (2, i), 'Helvetica-Bold'))
        else:
            tx_style.append(('TEXTCOLOR', (2, i), (2, i), RED))

    for i, is_paid_off in enumerate(row_is_paid_off, start=1):
        if is_paid_off:
            tx_style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#fef2f2')))

    tx_table.setStyle(TableStyle(tx_style))
    story.append(tx_table)
    story.append(Spacer(1, 8))

    # ---------- Paid-in-full summary note ----------
    if paid_in_full_dates:
        story.append(Paragraph(
            f"<b>Debt Cleared On:</b> {', '.join(paid_in_full_dates)}",
            small_note_style
        ))

    story.append(Spacer(1, 20))

    # ---------- Account Summary ----------
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

    # ---------- Signature ----------
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
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response


@app.route("/share_statement/<int:customer_id>")
@login_required
@admin_only
def customer_debt_statement_share(customer_id):
    customer = db.get_or_404(Customer, customer_id)

    pdf_url = url_for(
        "customer_debt_statement",
        customer_id=customer_id
    )

    return render_template(
        "share_statement.html",
        customer=customer,
        pdf_url=pdf_url
    )

@app.route("/edit_purchase/<int:purchase_id>", methods=["POST"])
@login_required
@admin_only
def edit_purchase(purchase_id):
    purchase = Purchase.query.get_or_404(purchase_id)
    original_supplier_id = purchase.supplier_id

    quantity = request.form.get("quantity", type=float)
    unit_price = request.form.get("unit_price", type=float)
    payment = request.form.get("payment", type=float)
    new_supplier_id = request.form.get("supplier_id", type=int)

    if quantity is None or unit_price is None or payment is None or new_supplier_id is None:
        flash("Invalid data submitted.", "danger")
        return redirect(url_for("supplier_purchase_history", supplier_id=original_supplier_id))

    if quantity <= 0 or unit_price < 0 or payment < 0:
        flash("Values must be valid positive numbers.", "danger")
        return redirect(url_for("supplier_purchase_history", supplier_id=original_supplier_id))

    new_supplier = Supplier.query.get(new_supplier_id)
    if not new_supplier:
        flash("Selected supplier does not exist.", "danger")
        return redirect(url_for("supplier_purchase_history", supplier_id=original_supplier_id))

    old_supplier_id = purchase.supplier_id
    new_total = quantity * unit_price
    new_debt = new_total - payment
    is_moving = old_supplier_id != new_supplier_id

    def supplier_remaining_debt(supplier_id, exclude_purchase_id=None, extra_total=0, extra_payment=0):
        # Rebuild from raw totals, NOT from Purchase.debt (which can go
        # stale — same fix already applied in /detail and customer_detail)
        purchases = Purchase.query.filter(
            Purchase.supplier_id == supplier_id,
            Purchase.id != exclude_purchase_id
        ).all()

        total_purchased = sum(
            (p.quantity or 0) * (p.unit_price or 0) for p in purchases
        )
        total_purchased += max(extra_total, 0)

        payments_at_purchase_time = sum(
            (p.payment or 0) for p in purchases
        )
        payments_at_purchase_time += max(extra_payment, 0)

        supplier = Supplier.query.get(supplier_id)
        balance_owed = 0
        if supplier and supplier.balance_owed and supplier.balance_owed > 0:
            balance_owed = supplier.balance_owed

        total_debt = total_purchased + balance_owed

        later_payments = SupplierPayment.query.filter_by(supplier_id=supplier_id).all()
        total_later_payments = sum(
            (pay.amount or 0) for pay in later_payments if (pay.amount or 0) > 0
        )

        total_paid = payments_at_purchase_time + total_later_payments

        return total_debt - total_paid

    # ---------------------------------------------------------
    # Check ORIGIN supplier
    # ---------------------------------------------------------
    if old_supplier_id:
        origin_extra_total = new_total if not is_moving else 0
        origin_extra_payment = payment if not is_moving else 0

        origin_remaining = supplier_remaining_debt(
            old_supplier_id,
            exclude_purchase_id=purchase.id,
            extra_total=origin_extra_total,
            extra_payment=origin_extra_payment
        )

        if origin_remaining < 0:
            old_supplier = Supplier.query.get(old_supplier_id)
            flash(
                f"Cannot save — this change would make {old_supplier.name if old_supplier else 'the original supplier'}'s "
                f"total remaining debt negative ({origin_remaining:,.2f} ETB).",
                "danger"
            )
            return redirect(url_for("supplier_purchase_history", supplier_id=original_supplier_id))

    # ---------------------------------------------------------
    # Check DESTINATION supplier — only relevant if actually moving
    # ---------------------------------------------------------
    if is_moving:
        destination_remaining = supplier_remaining_debt(
            new_supplier_id,
            exclude_purchase_id=purchase.id,
            extra_total=new_total,
            extra_payment=payment
        )

        if destination_remaining < 0:
            flash(
                f"Cannot move this purchase to {new_supplier.name} — it would make their total remaining debt negative "
                f"({destination_remaining:,.2f} ETB).",
                "danger"
            )
            return redirect(url_for("supplier_purchase_history", supplier_id=original_supplier_id))

    # ---------------------------------------------------------
    # Safe to save — apply changes
    # ---------------------------------------------------------
    product = Product.query.get(purchase.product_id)
    old_quantity = purchase.quantity or 0
    quantity_diff = quantity - old_quantity

    if product:
        product.current_quantity += quantity_diff

    purchase.quantity = quantity
    purchase.unit_price = unit_price
    purchase.payment = payment
    purchase.debt = new_debt
    purchase.supplier_id = new_supplier_id

    db.session.commit()

    if is_moving:
        flash(f"Purchase updated and moved to {new_supplier.name} successfully.", "success")
    else:
        flash("Purchase updated successfully.", "success")

    return redirect(url_for("supplier_purchase_history", supplier_id=new_supplier_id))


@app.route("/edit_sale/<int:sale_id>", methods=["POST"])
@login_required
@admin_only
def edit_sale(sale_id):
    sale = Sale.query.get_or_404(sale_id)
    original_customer_id = sale.customer_id

    quantity = request.form.get("quantity", type=float)
    unit_price = request.form.get("unit_price", type=float)
    current_payment = request.form.get("current_payment", type=float)
    new_customer_id = request.form.get("customer_id", type=int)

    if quantity is None or unit_price is None or current_payment is None or new_customer_id is None:
        flash("Invalid data submitted.", "danger")
        return redirect(url_for("customer_sales_history", customer_id=original_customer_id))

    if quantity <= 0 or unit_price < 0 or current_payment < 0:
        flash("Values must be valid positive numbers.", "danger")
        return redirect(url_for("customer_sales_history", customer_id=original_customer_id))

    new_customer = Customer.query.get(new_customer_id)
    if not new_customer:
        flash("Selected customer does not exist.", "danger")
        return redirect(url_for("customer_sales_history", customer_id=original_customer_id))

    old_customer_id = sale.customer_id
    new_total = quantity * unit_price
    new_debt = new_total - current_payment
    is_moving = old_customer_id != new_customer_id

    def customer_remaining_debt(customer_id, exclude_sale_id=None, extra_total=0, extra_payment=0):
        # Rebuild from raw totals, NOT from Sale.debt (which can go
        # stale — same fix already applied in customer_detail)
        sales = Sale.query.filter(
            Sale.customer_id == customer_id,
            Sale.id != exclude_sale_id
        ).all()

        total_sold = sum(
            (s.quantity or 0) * (s.unit_price or 0) for s in sales
        )
        total_sold += max(extra_total, 0)

        payments_at_sale_time = sum(
            (s.current_payment or 0) for s in sales
        )
        payments_at_sale_time += max(extra_payment, 0)

        additional_debt_records = AddDebt.query.filter_by(customer_id=customer_id).all()
        additional_debt = sum(d.amount or 0 for d in additional_debt_records)

        total_debt = total_sold + additional_debt

        later_payments = CustomerPayment.query.filter_by(customer_id=customer_id).all()
        total_later_payments = sum(
            (p.amount or 0) for p in later_payments if (p.amount or 0) > 0
        )

        total_paid = payments_at_sale_time + total_later_payments

        return total_debt - total_paid

    # ---------------------------------------------------------
    # Check ORIGIN customer
    # ---------------------------------------------------------
    if old_customer_id:
        origin_extra_total = new_total if not is_moving else 0
        origin_extra_payment = current_payment if not is_moving else 0

        origin_remaining = customer_remaining_debt(
            old_customer_id,
            exclude_sale_id=sale.id,
            extra_total=origin_extra_total,
            extra_payment=origin_extra_payment
        )

        if origin_remaining < 0:
            old_customer = Customer.query.get(old_customer_id)
            flash(
                f"Cannot save — this change would make {old_customer.name if old_customer else 'the original customer'}'s "
                f"total remaining debt negative ({origin_remaining:,.2f} ETB).",
                "danger"
            )
            return redirect(url_for("customer_sales_history", customer_id=original_customer_id))

    # ---------------------------------------------------------
    # Check DESTINATION customer — only relevant if actually moving
    # ---------------------------------------------------------
    if is_moving:
        destination_remaining = customer_remaining_debt(
            new_customer_id,
            exclude_sale_id=sale.id,
            extra_total=new_total,
            extra_payment=current_payment
        )

        if destination_remaining < 0:
            flash(
                f"Cannot move this sale to {new_customer.name} — it would make their total remaining debt negative "
                f"({destination_remaining:,.2f} ETB).",
                "danger"
            )
            return redirect(url_for("customer_sales_history", customer_id=original_customer_id))

    # ---------------------------------------------------------
    # Check stock availability if quantity increased
    # ---------------------------------------------------------
    product = Product.query.get(sale.product_id)
    old_quantity = sale.quantity or 0
    quantity_diff = quantity - old_quantity

    if product and quantity_diff > 0:
        if quantity_diff > product.current_quantity:
            flash(
                f"Insufficient stock. Only {product.current_quantity} available.",
                "danger"
            )
            return redirect(url_for("customer_sales_history", customer_id=original_customer_id))

    # ---------------------------------------------------------
    # Safe to save — apply changes
    # ---------------------------------------------------------
    if product:
        product.current_quantity -= quantity_diff

    sale.quantity = quantity
    sale.unit_price = unit_price
    sale.current_payment = current_payment
    sale.debt = new_debt
    sale.customer_id = new_customer_id

    db.session.commit()

    if is_moving:
        flash(f"Sale updated and moved to {new_customer.name} successfully.", "success")
    else:
        flash("Sale updated successfully.", "success")

    return redirect(url_for("customer_sales_history", customer_id=new_customer_id))





@app.route("/customer/<int:customer_id>/sales_history")
@login_required
@admin_only
def customer_sales_history(customer_id):
    customer = db.get_or_404(Customer, customer_id)

    sales = Sale.query.filter_by(customer_id=customer_id).order_by(Sale.id.desc()).all()
    debts = AddDebt.query.filter_by(customer_id=customer_id).order_by(AddDebt.id.desc()).all()
    payments = CustomerPayment.query.filter_by(customer_id=customer_id).all()
    products = {p.id: p for p in Product.query.all()}
    all_customers = Customer.query.order_by(Customer.name).all()

    total_sold = sum(Decimal(str(s.quantity or 0)) * Decimal(str(s.unit_price or 0)) for s in sales)
    sales_debt = sum(max(Decimal(str(s.debt or 0)), Decimal("0")) for s in sales)
    additional_debt = sum(max(Decimal(str(d.amount or 0)), Decimal("0")) for d in debts)
    total_debt = sales_debt + additional_debt
    total_paid = sum(max(Decimal(str(p.amount or 0)), Decimal("0")) for p in payments)
    remaining_debt = max(total_debt - total_paid, Decimal("0"))

    return render_template(
        "customer_sales_history.html",
        customer=customer, sales=sales, debts=debts, products=products,
        all_customers=all_customers,
        total_sold=total_sold, total_paid=total_paid, remaining_debt=remaining_debt
    )






@app.route("/customer/<int:customer_id>/payment_history")
@login_required
@emp_allowed
def customer_payment_history(customer_id):
    customer = db.get_or_404(Customer, customer_id)

    payments = CustomerPayment.query.filter_by(customer_id=customer_id).order_by(CustomerPayment.id.desc()).all()
    sales = Sale.query.filter_by(customer_id=customer_id).all()
    debts = AddDebt.query.filter_by(customer_id=customer_id).all()

    total_sold = sum(Decimal(str(s.quantity or 0)) * Decimal(str(s.unit_price or 0)) for s in sales)
    sales_debt = sum(max(Decimal(str(s.debt or 0)), Decimal("0")) for s in sales)
    additional_debt = sum(max(Decimal(str(d.amount or 0)), Decimal("0")) for d in debts)
    total_debt = sales_debt + additional_debt
    total_paid = sum(max(Decimal(str(p.amount or 0)), Decimal("0")) for p in payments)
    remaining_debt = max(total_debt - total_paid, Decimal("0"))

    return render_template(
        "customer_payment_history.html",
        customer=customer, payments=payments,
        total_sold=total_sold, total_paid=total_paid, remaining_debt=remaining_debt
    )


@app.route("/supplier/<int:supplier_id>/payment_history")
@login_required
@emp_allowed
def supplier_payment_history(supplier_id):
    supplier = db.get_or_404(Supplier, supplier_id)

    payments = SupplierPayment.query.filter_by(supplier_id=supplier_id).order_by(SupplierPayment.id.desc()).all()
    purchases = Purchase.query.filter_by(supplier_id=supplier_id).all()

    total_purchased = sum(Decimal(str(p.total_price or 0)) for p in purchases)
    purchase_debt = sum(max(Decimal(str(p.debt or 0)), Decimal("0")) for p in purchases)

    balance_owed = Decimal(str(supplier.balance_owed or 0))
    if balance_owed < 0:
        balance_owed = Decimal("0")

    total_debt = purchase_debt + balance_owed
    total_paid = sum(max(Decimal(str(p.amount or 0)), Decimal("0")) for p in payments)
    remaining_debt = max(total_debt - total_paid, Decimal("0"))

    return render_template(
        "supplier_payment_history.html",
        supplier=supplier, payments=payments,
        total_purchased=total_purchased, total_paid=total_paid, remaining_debt=remaining_debt
    )



@app.route("/supplier/<int:supplier_id>/purchase_history")
@login_required
@admin_only
def supplier_purchase_history(supplier_id):
    supplier = db.get_or_404(Supplier, supplier_id)

    purchases = Purchase.query.filter_by(supplier_id=supplier_id).order_by(Purchase.id.desc()).all()
    payments = SupplierPayment.query.filter_by(supplier_id=supplier_id).all()
    products = {p.id: p for p in Product.query.all()}
    all_suppliers = Supplier.query.order_by(Supplier.name).all()

    total_purchased = sum(Decimal(str(p.total_price or 0)) for p in purchases)
    purchase_debt = sum(max(Decimal(str(p.debt or 0)), Decimal("0")) for p in purchases)

    balance_owed = Decimal(str(supplier.balance_owed or 0))
    if balance_owed < 0:
        balance_owed = Decimal("0")

    total_debt = purchase_debt + balance_owed
    total_paid = sum(max(Decimal(str(p.amount or 0)), Decimal("0")) for p in payments)
    remaining_debt = max(total_debt - total_paid, Decimal("0"))

    return render_template(
        "supplier_purchase_history.html",
        supplier=supplier, purchases=purchases, products=products,
        all_suppliers=all_suppliers,
        total_purchased=total_purchased, total_paid=total_paid, remaining_debt=remaining_debt
    )

@app.route("/products")
@login_required
@emp_allowed
def products_page():
    products = Product.query.filter_by(is_deleted=False).all()
    return render_template(
        "products.html",
        products=products,
        user_id=current_user.id
    )


@app.route("/customers")
@login_required
@emp_allowed
def customers_page():
    customers = Customer.query.order_by(Customer.id.desc()).all()

    customer_list = []
    for c in customers:
        sales = Sale.query.filter_by(customer_id=c.id).all()
        sales_debt = sum(max(Decimal(str(s.debt or 0)), Decimal("0")) for s in sales)

        debts = AddDebt.query.filter_by(customer_id=c.id).all()
        additional_debt = sum(max(Decimal(str(d.amount or 0)), Decimal("0")) for d in debts)

        payments = CustomerPayment.query.filter_by(customer_id=c.id).all()
        total_paid = sum(max(Decimal(str(p.amount or 0)), Decimal("0")) for p in payments)

        total_debt = sales_debt + additional_debt
        remaining_debt = max(total_debt - total_paid, Decimal("0"))

        c.debt = remaining_debt
        c.paid_amount = total_paid
        customer_list.append(c)

    return render_template(
        "customers.html",
        customers=customer_list,
        user_id=current_user.id
    )


@app.route("/suppliers")
@login_required
@emp_allowed
def suppliers_page():
    suppliers = Supplier.query.order_by(Supplier.id.desc()).all()

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
        "suppliers.html",
        suppliers=supplier_list,
        user_id=current_user.id
    )

from datetime import datetime, date

def prettydate(value):
    if isinstance(value, (datetime, date)):
        return value.strftime('%b %d, %Y')
    if isinstance(value, str):
        for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d'):
            try:
                dt = datetime.strptime(value, fmt)
                return dt.strftime('%b %d, %Y')
            except ValueError:
                continue
    return value

app.jinja_env.filters['prettydate'] = prettydate


@app.route("/history/sales")
@login_required
@admin_only
def sales_history_page():
    sales = Sale.query.order_by(Sale.id.desc()).all()
    customer_payments = CustomerPayment.query.order_by(CustomerPayment.id.desc()).all()
    products = {p.id: p for p in Product.query.all()}
    customers = {c.id: c for c in Customer.query.all()}

    return render_template(
        "sales_history.html",
        sales=sales,
        customer_payments=customer_payments,
        products=products,
        customers=customers
    )


@app.route("/history/purchases")
@login_required
@admin_only
def purchases_history_page():
    purchases = Purchase.query.order_by(Purchase.id.desc()).all()
    payments = SupplierPayment.query.order_by(SupplierPayment.id.desc()).all()
    products = {p.id: p for p in Product.query.all()}
    suppliers = {s.id: s for s in Supplier.query.all()}

    return render_template(
        "purchases_history.html",
        purchases=purchases,
        payments=payments,
        products=products,
        suppliers=suppliers
    )


@app.route("/expenses")
@login_required
@admin_only
def expenses():
    purchases = Purchase.query.filter_by(
        user_id=current_user.id
    ).order_by(Purchase.date.desc()).all()

    grouped = {}
    grand_total = 0

    for p in purchases:
        day = p.date or "Unknown"
        cost = float(p.unit_price or 0) * float(p.quantity or 0)
        grand_total += cost

        if day not in grouped:
            grouped[day] = {"items": [], "total": 0}

        grouped[day]["items"].append({
            "product_name": p.product.name if p.product else "—",
            "supplier_name": p.supplier.name if p.supplier else "—",
            "quantity": p.quantity,
            "unit_price": p.unit_price,
            "total": cost
        })
        grouped[day]["total"] += cost

    grouped = dict(sorted(grouped.items(), reverse=True))

    return render_template(
        "expenses.html",
        grouped=grouped,
        grand_total=grand_total,
        user_id=current_user.id
    )



@app.route('/stock/add', methods=['GET', 'POST'])
@admin_only
def stock_add():
    products = Product.query.filter_by(is_deleted=False).all()
    if request.method == 'POST':
        product = Product.query.get_or_404(int(request.form['product_id']))
        qty = float(request.form['quantity'])
        product.current_quantity += qty

        db.session.add(StockAdjustment(
            product_id=product.id,
            change_type='add',
            quantity=qty,
            user_id=current_user.id if current_user.is_authenticated else None
        ))

        db.session.commit()
        flash(f'{product.name} ላይ {qty} ተጨምሯል።', 'success')
        return redirect(url_for('stock_add'))
    return render_template('stock_add.html', products=products)


@app.route('/stock/subtract', methods=['GET', 'POST'])
@admin_only
def stock_subtract():
    products = Product.query.filter_by(is_deleted=False).all()
    if request.method == 'POST':
        product = Product.query.get_or_404(int(request.form['product_id']))
        qty = float(request.form['quantity'])
        if qty > product.current_quantity:
            flash('የሚቀነሰው መጠን ካለው ክምችት መብለጥ አይችልም።', 'danger')
            return redirect(url_for('stock_subtract'))
        product.current_quantity -= qty

        db.session.add(StockAdjustment(
            product_id=product.id,
            change_type='subtract',
            quantity=qty,
            user_id=current_user.id if current_user.is_authenticated else None
        ))

        db.session.commit()
        flash(f'{product.name} ላይ {qty} ተቀንሷል።', 'success')
        return redirect(url_for('stock_subtract'))
    return render_template('stock_subtract.html', products=products)


@app.route('/change-price', methods=['GET', 'POST'])
@login_required
@emp_allowed
def change_price():
    products = Product.query.filter_by(is_deleted=False).all()

    if request.method == 'POST':

        index = 0
        updates = []
        errors_found = False

        while f'items-{index}-product_id' in request.form:

            product_id = request.form.get(f'items-{index}-product_id')
            new_price_raw = request.form.get(f'items-{index}-new_price')

            product = Product.query.get(product_id) if product_id else None

            if not product:
                flash('የተመረጠ ምርት አልተገኘም።', 'danger')
                errors_found = True
                index += 1
                continue

            try:
                new_price = float(new_price_raw)
            except (TypeError, ValueError):
                new_price = -1

            if new_price <= 0:
                flash(f'{product.name} ላይ ዋጋ ከዜሮ በላይ መሆን አለበት።', 'danger')
                errors_found = True
                index += 1
                continue

            updates.append((product, new_price))
            index += 1

        if errors_found:
            return render_template('change_price.html', products=products)

        for product, new_price in updates:
            old_price = product.unit_price
            product.unit_price = new_price

            db.session.add(PriceChange(
                product_id=product.id,
                price_type='selling',
                old_price=old_price,
                new_price=new_price,
                user_id=current_user.id if current_user.is_authenticated else None
            ))

        db.session.commit()

        flash(f'{len(updates)} ምርት(ቶች) ዋጋ ተቀይሯል።', 'success')
        return redirect(url_for('change_price'))

    return render_template('change_price.html', products=products)


@app.route('/change-purchase-price', methods=['GET', 'POST'])
@login_required
@emp_allowed
def change_purchase_price():
    products = Product.query.filter_by(is_deleted=False).all()

    if request.method == 'POST':

        index = 0
        updates = []
        errors_found = False

        while f'items-{index}-product_id' in request.form:

            product_id = request.form.get(f'items-{index}-product_id')
            new_price_raw = request.form.get(f'items-{index}-new_price')

            product = Product.query.get(product_id) if product_id else None

            if not product:
                flash('የተመረጠ ምርት አልተገኘም።', 'danger')
                errors_found = True
                index += 1
                continue

            try:
                new_price = float(new_price_raw)
            except (TypeError, ValueError):
                new_price = -1

            if new_price <= 0:
                flash(f'{product.name} ላይ ዋጋ ከዜሮ በላይ መሆን አለበት።', 'danger')
                errors_found = True
                index += 1
                continue

            updates.append((product, new_price))
            index += 1

        if errors_found:
            return render_template('change_purchase_price.html', products=products)

        for product, new_price in updates:
            old_price = product.purchase_price
            product.purchase_price = new_price

            db.session.add(PriceChange(
                product_id=product.id,
                price_type='purchase',
                old_price=old_price,
                new_price=new_price,
                user_id=current_user.id if current_user.is_authenticated else None
            ))

        db.session.commit()

        flash(f'{len(updates)} ምርት(ቶች) የግዢ ዋጋ ተቀይሯል።', 'success')
        return redirect(url_for('change_purchase_price'))

    return render_template('change_purchase_price.html', products=products)









@app.route("/edit/sales/select-customer")
@login_required
@emp_allowed
def select_customer_for_sales_edit():
    customers = Customer.query.order_by(Customer.name).all()
    return render_template("select_customer_for_edit.html", customers=customers)


@app.route("/edit/purchases/select-supplier")
@login_required
@admin_only
def select_supplier_for_purchases_edit():
    suppliers = Supplier.query.order_by(Supplier.name).all()
    return render_template("select_supplier_for_edit.html", suppliers=suppliers)



@app.route("/product/<int:product_id>/history")
@login_required
@emp_allowed
def product_history(product_id):
    product = db.get_or_404(Product, product_id)

    sales = Sale.query.filter_by(product_id=product_id).order_by(Sale.id.desc()).all()
    purchases = Purchase.query.filter_by(product_id=product_id).order_by(Purchase.id.desc()).all()
    adjustments = StockAdjustment.query.filter_by(product_id=product_id).order_by(StockAdjustment.id.desc()).all()
    price_changes = PriceChange.query.filter_by(product_id=product_id).order_by(PriceChange.id.desc()).all()

    timeline = []

    for s in sales:
        customer = Customer.query.get(s.customer_id)
        timeline.append({
            "type": "sale",
            "text": f"{s.quantity} pc ለ {customer.name if customer else 'ያልታወቀ ደንበኛ'} ተሸጠ",
            "detail": f"በ {s.unit_price:,.2f} ETB",
            "date": s.date,
            "sort_key": getattr(s, "created_at", None) or s.date
        })

    for p in purchases:
        supplier = Supplier.query.get(p.supplier_id)
        timeline.append({
            "type": "purchase",
            "text": f"{p.quantity} pc ከ {supplier.name if supplier else 'ያልታወቀ አቅራቢ'} ተገዛ",
            "detail": f"በ {p.unit_price:,.2f} ETB",
            "date": p.date,
            "sort_key": getattr(p, "created_at", None) or p.date
        })

    for a in adjustments:
        timeline.append({
            "type": "stock_add" if a.change_type == "add" else "stock_subtract",
            "text": f"{a.quantity} pc {'ተጨመረ' if a.change_type == 'add' else 'ተቀነሰ'}",
            "detail": f"በ {a.user.name if a.user else 'ያልታወቀ'} ተመዘገበ",
            "date": a.created_at.strftime("%m/%d/%Y") if a.created_at else "",
            "sort_key": a.created_at
        })

    for pc in price_changes:
        label = "የመሸጫ ዋጋ" if pc.price_type == "selling" else "የግዢ ዋጋ"
        timeline.append({
            "type": "price_change",
            "text": f"{label} ከ {pc.old_price:,.2f} ወደ {pc.new_price:,.2f} ETB ተቀይሯል",
            "detail": f"በ {pc.user.name if pc.user else 'ያልታወቀ'} ተመዘገበ",
            "date": pc.created_at.strftime("%m/%d/%Y") if pc.created_at else "",
            "sort_key": pc.created_at
        })

    timeline = [t for t in timeline if t["sort_key"]]
    timeline.sort(key=lambda x: str(x["sort_key"]), reverse=True)

    return render_template("product_history.html", product=product, timeline=timeline)


@app.route("/reports/settings-history")
@login_required
@admin_only
def settings_history():
    adjustments = StockAdjustment.query.order_by(StockAdjustment.id.desc()).all()
    price_changes = PriceChange.query.order_by(PriceChange.id.desc()).all()

    records = []

    for a in adjustments:
        product = Product.query.get(a.product_id)
        records.append({
            "type": "stock_add" if a.change_type == "add" else "stock_subtract",
            "product_name": product.name if product else "ያልታወቀ ምርት",
            "detail": f"{a.quantity} pc {'ተጨመረ' if a.change_type == 'add' else 'ተቀነሰ'}",
            "user_name": a.user.name if a.user else "ያልታወቀ",
            "date": a.created_at,
            "sort_key": a.created_at
        })

    for pc in price_changes:
        product = Product.query.get(pc.product_id)
        label = "የመሸጫ ዋጋ" if pc.price_type == "selling" else "የግዢ ዋጋ"
        records.append({
            "type": "price_change",
            "product_name": product.name if product else "ያልታወቀ ምርት",
            "detail": f"{label}: {pc.old_price:,.2f} → {pc.new_price:,.2f} ETB",
            "user_name": pc.user.name if pc.user else "ያልታወቀ",
            "date": pc.created_at,
            "sort_key": pc.created_at
        })

    records = [r for r in records if r["sort_key"]]
    records.sort(key=lambda x: x["sort_key"], reverse=True)

    return render_template("settings_history.html", records=records)











if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    # app.run(debug=True, port=5005)