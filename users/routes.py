import os
import pathlib

import requests
import google.auth.transport.requests as google
from pip._vendor import cachecontrol
from flask import render_template, Blueprint, abort, \
    session, url_for, flash, redirect, request
from CeeVee_Online.users.forms import Category, SignUpForm, SignInForm, User, ResetPasswordForm, RequestResetForm
from CeeVee_Online import bcrypt, db
from flask_login import current_user, login_user, logout_user
from CeeVee_Online.users.utils import send_reset_email
from CeeVee_Online.categories.category_service import CategoryService
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token

users = Blueprint("users", __name__)
category_service = CategoryService()
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
redirect_uri = os.environ.get('REDIRECT_URI')
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=['https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email', 'openid'],
    redirect_uri=redirect_uri
)


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


# Implementing google login feature
@users.route("/google_login")
def google_login():
    """Google AuthO2 login
    """
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function()

    return wrapper


@users.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(5000)
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/")


@users.route("/")
@login_is_required
def index():
    """
    Get the columns of the cat model
    """
    return redirect(url_for('products.all_products'))


@users.route("/home")
def home():
    return redirect(url_for('products.all_products'))


@users.route("/categories")
@login_is_required
def categories():
    return render_template("index.html",
                           categories=category_service.get_all_categories(),
                           title='Home')


@users.route("/laptops")
@login_is_required
def laptops():
    return render_template('laptops.html', title='Categories')


@users.route("/listings")
@login_is_required
def listings():
    return render_template('listings.html', title='Listings')


@users.route("/listing")
@login_is_required
def listing():
    return render_template('listing.html', title='Listing')


@users.route("/payment")
@login_is_required
def payment():
    return render_template('payment.html', title='Payment')


@users.route("/signup", methods=['GET', 'POST'])
def sign_up():
    """Signup view function. Handles signup form validations
    Return: signup view
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data, email=form.email.data,
                    password=hashed_password, role="customers")

        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=hashed_password)

        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You are now able to login',
              'success')  # Fixed the flash message
        return redirect(url_for('login'))
    return render_template("signup.html", title='Register', form=form)


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
@login_is_required
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
@login_is_required
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
@login_is_required
def logout():
    """Logout a logged-in user"""
    logout_user();
    session.clear()
    return redirect(url_for('users.login'))
