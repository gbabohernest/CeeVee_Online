from flask import render_template, Blueprint, url_for, flash, redirect, request, g
from CeeVee_Online.users.forms import SignUpForm, SignInForm, User, Role, ResetPasswordForm, RequestResetForm
from CeeVee_Online import bcrypt, db
from flask_login import current_user, login_user, logout_user
from CeeVee_Online.users.utils import send_reset_email

users = Blueprint("users", __name__)








class cat(db.Model):
    __tablename__ = 'ceevee_sidebar'
    id = db.Column(db.Integer, primary_key=True)
    Laptop_part = db.Column(db.String(255))
    Laptop_Accessory = db.Column(db.String(255))
    Desktop_Part = db.Column(db.String(255))
    Desktop_Accessory = db.Column(db.String(255))
    Phone_Part = db.Column(db.String(255))
    Phone_Accessory = db.Column(db.String(255))
    Tablet_Part = db.Column(db.String(255))
    Tablet_Accessory = db.Column(db.String(255))
    Console_part = db.Column(db.String(255))
    Console_Accessories = db.Column(db.String(255))
    Appliance_Home = db.Column(db.String(255))
    Appliance_Kitchen = db.Column(db.String(255))
    Server_Networking = db.Column(db.String(255))
    Sound = db.Column(db.String(255))
    Video_Pictures = db.Column(db.String(255))
    Car = db.Column(db.String(255))
    Car_Part = db.Column(db.String(255))
    Car_Accessory = db.Column(db.String(255))


class laptops_listing(db.Model):
    __tablename__ = 'Laptop_listings'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    PRICE = db.Column(db.String(255))
    PRODUCT = db.Column(db.String(255))
    YEAR = db.Column(db.String(255))
    BRAND = db.Column(db.String(255))
    BRAND_MODEL = db.Column(db.String(255))
    SERIAL_NUMBER = db.Column(db.String(255))
    PURPOSE = db.Column(db.String(255))
    OPERATING_SYSTEM = db.Column(db.String(255))
    PROCESSOR_TYPE = db.Column(db.String(255))
    CPU_AMD_MODEL = db.Column(db.String(255))
    CPU_INTEL_MODEL = db.Column(db.String(255))
    CPU_QUALCOMM_MODEL = db.Column(db.String(255))
    GRAPHICS_NUMBER = db.Column(db.String(255))
    GPU_INTEGRATED = db.Column(db.String(255))
    Dedicated_brand = db.Column(db.String(255))
    GPU_DEDICATED = db.Column(db.String(255))
    DRIVE_NUMBER = db.Column(db.String(255))
    DD_NVME_SSD = db.Column(db.String(255))
    DD_SATA_SSD = db.Column(db.String(255))
    DD_HDD = db.Column(db.String(255))
    RAM_CAPACITY = db.Column(db.String(255))
    SCREEN_TYPE = db.Column(db.String(255))
    SCREEN_SIZE = db.Column(db.String(255))
    SCREEN_RESOLUTION = db.Column(db.String(255))
    LAPTOP_CHARGER = db.Column(db.String(255))
    CONDITION_POWER_STATUS = db.Column(db.String(255))
    CONDITION_SCREEN = db.Column(db.String(255))
    CONDITION_KEYBOARD = db.Column(db.String(255))
    CONDITION_LAPTOP_USB = db.Column(db.String(255))
    CONDITION_LAN_PORT = db.Column(db.String(255))
    CONDITION_WIFI = db.Column(db.String(255))
    CONDITION_BLUETOOTH = db.Column(db.String(255))
    CONDITION_AUDIO_JACK = db.Column(db.String(255))
    CONDITION_CARD_READER = db.Column(db.String(255))
    PHOTOS = db.Column(db.String(255))






def get_data_for_templates():
    columns = cat.__table__.columns.keys()
    rows = cat.query.all()

    column_names = {}
    for column in columns:
        column_names[column] = [getattr(row, column) for row in rows]

    cat_name = replace_underscores_with_spaces(column_names)
    Laptop_part = [row.Laptop_part for row in rows]
    Laptop_Accessory = [row.Laptop_Accessory for row in rows]
    Desktop_Part = [row.Desktop_Part for row in rows]

    return {
        'sidebar': ['Laptop', 'Desktop', 'Phone', 'Tablet', 'Console', 'Appliance', 'Professional', 'Cars', 'Parts'],
        'rows': rows,
        'column_names': column_names,
        'cat_name': cat_name,
        'Laptop_part': Laptop_part,
        'Laptop_Accessory': Laptop_Accessory,
        'Desktop_Part': Desktop_Part
    }





def laptop_listings_to_dict():
    """
    Retrieve all data from the 'Laptop_listings' table and transform it into a dictionary.

    Returns:
        A dictionary where keys are column names and values are lists of corresponding column values for each row.
    """
    # Retrieve all rows from the 'Laptop_listings' table
    rows = laptops_listing.query.all()

    # Get the columns of the 'Laptop_listings' table
    columns = laptops_listing.__table__.columns.keys()

    # Initialize an empty dictionary to store the table data
    table_data = {column: [] for column in columns}

    # Populate the dictionary with data from each row
    for row in rows:
        for column in columns:
            # Get the value of the current column for the current row
            value = getattr(row, column)
            # Append the value to the corresponding list in the dictionary
            table_data[column].append(value)

    return table_data




def replace_underscores_with_spaces(lst):
    """
    Replace underscores with spaces in each string within a list object.
    """
    new_lst = []  # Initialize an empty list to store modified strings

    # Iterate over each string in the input list
    for string in lst:
        # Replace underscores with spaces in the current string
        modified_string = string.replace('_', ' ')
        # Add the modified string to the new list
        new_lst.append(modified_string)

    return new_lst



@users.route('/home')
def index():
    template_data = get_data_for_templates()
    laptop_list = laptop_listings_to_dict()


    # Pass the laptop_parts list to the template
    return render_template('home.html', **template_data, laptop_list=laptop_list)



@users.route("/")
def home():
    return render_template('landing.html')


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


@users.route('/about')
def about():
    template_data = get_data_for_templates()
    return render_template('about.html', **template_data)



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
        role_name=Role(name="Admin", role_description="Manage everything")
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