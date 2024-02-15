from flask import render_template, Blueprint, url_for, flash, redirect, request
from CeeVee_Online.users.forms import Category, SignUpForm, SignInForm, User, Role, ResetPasswordForm, RequestResetForm
from CeeVee_Online import bcrypt, db
from CeeVee_Online.categories.category_service import CategoryService
from flask_login import current_user, login_user, logout_user
from CeeVee_Online.users.utils import send_reset_email
from sqlalchemy import asc, desc

users = Blueprint("users", __name__)
category_service = CategoryService()


# class cat(db.Model):
#     __tablename__ = 'ceevee_categories'
#     id = db.Column(db.Integer, primary_key=True)
#     Laptop_part = db.Column(db.String(255))
#     Laptop_Accessory = db.Column(db.String(255))
#     Desktop_Part = db.Column(db.String(255))
#     Desktop_Accessory = db.Column(db.String(255))
#     Phone_Part = db.Column(db.String(255))
#     Phone_Accessory = db.Column(db.String(255))
#     Tablet_Part = db.Column(db.String(255))
#     Tablet_Accessory = db.Column(db.String(255))
#     Console_part = db.Column(db.String(255))
#     Console_Accessories = db.Column(db.String(255))
#     Appliance_Home = db.Column(db.String(255))
#     Appliance_Kitchen = db.Column(db.String(255))
#     Server_Networking = db.Column(db.String(255))
#     Sound = db.Column(db.String(255))
#     Video_Pictures = db.Column(db.String(255))
#     Car = db.Column(db.String(255))
#     Car_Part = db.Column(db.String(255))
#     Car_Accessory = db.Column(db.String(255))

#
# def replace_underscores_with_spaces(lst):
#     """
#     Replace underscores with spaces in each string within a list object.
#
#     Args:
#     lst (list): A list object containing strings.
#
#     Returns:
#     list: A new list object with underscores replaced by spaces in each string.
#     """
#     new_lst = []  # Initialize an empty list to store modified strings
#
#     # Iterate over each string in the input list
#     for string in lst:
#         # Replace underscores with spaces in the current string
#         modified_string = string.replace('_', ' ')
#         # Add the modified string to the new list
#         new_lst.append(modified_string)
#
#     return new_lst


@users.route('/')
def index():
    """
    Get the columns of the cat model
    """
    category_service_ = CategoryService()
    for categories_ in category_service_.get_all_categories():
        return render_template('home.html', categories_=categories_)


@users.route("/home")
def home():
    return render_template('backup/home.html')


@users.route("/categories")
def categories():
    return render_template('listings.html', title='Categories')


@users.route("/laptops")
def laptops():
    return render_template('laptops.html', title='Categories')


@users.route("/listings")
def listings():
    return render_template('listings.html', title='Listings')


@users.route("/listing")
def listing():
    return render_template('listing.html', title='Listing')


@users.route("/payment")
def payment():
    return render_template('payment.html', title='Payment')


@users.route("/signup", methods=('GET', 'POST'))
def sign_up():
    """Signup view function. Handles signup form validations
    Return: signup view
    """
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))

    form = SignUpForm();
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data, email=form.email.data,
                    password=hashed_password)
        role_name = Role(name="Admin", role_description="Manage everything")
        user.roles.append(role_name)
        db.session.add(user)
        db.session.commit();
        flash(f'Account created for {form.username.data}! you''re now able to login', 'success')
        return redirect(url_for('users.login'))
    return render_template("signup.html", title='Register', form=form);


@users.route("/login", methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.home'))

        else:
            flash("Login unsuccessful, please check email or password!", 'danger')
    return render_template("login.html", title='Login', form=form)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    """Ask for a reset password request"""
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password", 'info');
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',
                           form=form, title='Reset Password')


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """Reset user's token"""
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))

    user = User.verify_reset_token(token)
    if not user:
        flash('Token invalid or expired', 'warning')
        return redirect(url_for('users.reset_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated! You're now able to login", 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',
                           form=form, title='Reset Token')


@users.route("/logout")
def logout():
    """Logout a logged-in user"""
    logout_user();
    return redirect(url_for('users.login'))
