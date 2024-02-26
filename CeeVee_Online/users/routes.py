from flask import render_template, Blueprint, url_for, flash, redirect, request, g, jsonify
from CeeVee_Online.users.forms import SignUpForm, LoginForm, User, Role, ResetPasswordForm, RequestResetForm, PostingForm
from CeeVee_Online import bcrypt, db
from flask_login import current_user, login_user, logout_user, login_required, current_user
from CeeVee_Online.users.utils import send_reset_email
import uuid
from sqlalchemy.exc import IntegrityError
from flask import session
from flask_login import LoginManager
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from sqlalchemy import func

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
    post_id = db.Column(db.String)
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
    DEDICATED_BRAND = db.Column(db.String(255))
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




class laptops_data(db.Model):
    __tablename__ = 'Laptop_data'
    id = db.Column(db.Integer, primary_key=True)
    BRAND = db.Column(db.String(255))
    PURPOSE = db.Column(db.String(255))
    OPERATING_SYSTEM = db.Column(db.String(255))
    YEAR = db.Column(db.String(255))
    CPU_BRAND = db.Column(db.String(255))
    CPU_AMD_MODEL = db.Column(db.String(255))
    CPU_INTEL_MODEL = db.Column(db.String(255))
    CPU_QUALCOMM_MODEL = db.Column(db.String(255))
    GPU_NUMBER = db.Column(db.Integer)
    GPU_INTEGRATED_BRAND = db.Column(db.String(255))
    GPU_INTEL_INTEGRATED = db.Column(db.String(255))
    GPU_AMD_INTEGRATED = db.Column(db.String(255))
    GPU_DEDICATED_BRAND = db.Column(db.String(255))
    GPU_INTEL_DEDICATED = db.Column(db.String(255))
    GPU_AMD_DEDICATED = db.Column(db.String(255))
    GPU_NVIDIA_DEDICATED = db.Column(db.String(255))
    DRIVE_NUMBER = db.Column(db.Integer)
    DRIVE_TYPE = db.Column(db.String(255))
    DRIVE_CAPACITY = db.Column(db.String(255))
    RAM_NUMBER = db.Column(db.Integer)
    RAM_TYPE = db.Column(db.String(255))
    RAM_CAPACITY = db.Column(db.String(255))
    SCREEN_TYPE = db.Column(db.String(255))
    SCREEN_RESOLUTION = db.Column(db.String(255))
    SCREEN_CONDITION = db.Column(db.String(255))
    KEYBOARD_LAYOUT = db.Column(db.String(255))
    KEYBOARD_CONDITION = db.Column(db.String(255))
    LAPTOP_POWER_STATUS = db.Column(db.String(255))
    LAPTOP_CHARGER = db.Column(db.String(255))
    LAPTOP_USB = db.Column(db.String(255))
    LAN_PORT = db.Column(db.String(255))
    WIFI_CONDITION = db.Column(db.String(255))
    BLUETOOTH_CONDITION = db.Column(db.String(255))









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






def table_to_dict(database_name):
    # Retrieve all rows from the 'Laptop_listings' table
    rows = database_name.query.all()

    # Get the columns of the 'Laptop_listings' table
    columns = database_name.__table__.columns.keys()

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
    laptop_list = table_to_dict(laptops_listing)
    full_name= None
    if current_user.is_authenticated:
        full_name = current_user.first_name + ' ' + current_user.last_name
    # Pass the laptop_parts list to the template
    return render_template('home.html', **template_data, laptop_list=laptop_list, full_name=full_name)



@users.route("/")
def home():
    return render_template('landing.html')



@users.route('/product/<int:listing_id>')
def product(listing_id):
    template_data = get_data_for_templates()
    laptop_list = table_to_dict(laptops_listing)
    full_name= None
    if current_user.is_authenticated:
        full_name = current_user.first_name + ' ' + current_user.last_name

    # Pass the laptop_parts list to the template
    return render_template('product.html', **template_data, laptop_list=laptop_list, listing_id=listing_id, full_name=full_name)


@users.route("/categories")
def categories():
    return render_template('listings.html', title='Categories')


@users.route("/laptops")
def laptops():
    template_data = get_data_for_templates()
    laptop_list = table_to_dict(laptops_listing)
    full_name= None
    if current_user.is_authenticated:
        full_name = current_user.first_name + ' ' + current_user.last_name


    return render_template('laptops.html', **template_data, laptop_list=laptop_list, title='Categories', full_name=full_name)


@users.route("/posting")
def posting():
    form = PostingForm()
    template_data = get_data_for_templates()
    laptop_list = table_to_dict(laptops_listing)
    laptop_data = table_to_dict(laptops_data)
    full_name= None
    if current_user.is_authenticated:
        full_name = current_user.first_name + ' ' + current_user.last_name
    return render_template('posting.html', **template_data, laptop_data=laptop_data, laptop_list=laptop_list, form=form, title='posting', full_name=full_name)


@users.route("/postings")
def postings():
    template_data = get_data_for_templates()
    laptop_list = table_to_dict(laptops_listing)
    full_name= None
    if current_user.is_authenticated:
        full_name = current_user.first_name + ' ' + current_user.last_name
    return render_template('postings.html', **template_data, laptop_list=laptop_list, title='Categories', full_name=full_name)



@users.route("/listings")
def listings():
    template_data = get_data_for_templates()
    laptop_list = table_to_dict(laptops_listing)
    full_name= None
    user_id= None
    if current_user.is_authenticated:
        full_name = current_user.first_name + ' ' + current_user.last_name
        user_id = current_user.id
    return render_template('listings.html', **template_data, laptop_list=laptop_list, title='Listings', full_name=full_name, user_id=user_id)


@users.route("/listing")
def listing():
    return render_template('listing.html', title='Listing')


@users.route("/payment")
def payment():
    template_data = get_data_for_templates()
    full_name= None
    if current_user.is_authenticated:
        full_name = current_user.first_name + ' ' + current_user.last_name
    return render_template('payment.html', **template_data, laptop_list=laptop_list, title='Payment', full_name=full_name)


@users.route('/about')
def about():
    template_data = get_data_for_templates()
    full_name= None
    if current_user.is_authenticated:
        full_name = current_user.first_name + ' ' + current_user.last_name
    return render_template('about.html', **template_data, full_name=full_name)



""" @users.route("/signup", methods=('GET', 'POST'))
def sign_up():

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
    return render_template("signup.html", title='Register', form=form); """



@users.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        # Check if the email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already exists', 'danger')
        else:
            # Proceed with creating a new user if the email doesn't exist
            user_id = str(uuid.uuid4())
            # Hash the password before storing it
            hashed_password = generate_password_hash(form.password.data)
            new_user = User(id=user_id,
                            email=form.email.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=hashed_password)  # Store the hashed password
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Account created successfully!', 'success')
                return redirect(url_for('users.login'))
            except IntegrityError:
                db.session.rollback()
                flash('An error occurred while creating your account. Please try again.', 'danger')
    return render_template('signup.html', form=form)



""" @users.route("/login", methods=('GET', 'POST'))
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
    return render_template("login.html", title='Login', form=form) """


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # Populate the user object with additional attributes
            user_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
            # Add user data to the session
            session['user'] = user_data
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('users.home'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')
    return render_template('login.html', form=form)





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

@users.route('/settings')
@login_required
def settings():
    user = current_user
    return render_template('settings.html', user=user)


@users.route("/logout")
def logout():
    """Logout a logged-in user"""
    logout_user()
    session.clear()  # Clear session data
    return redirect(url_for('users.login'))



@users.route('/submit_laptop', methods=['POST'])
def submit_laptop():
    full_name= None
    user_id= None
    if current_user.is_authenticated:
        user_id = current_user.id
        full_name = current_user.first_name + ' ' + current_user.last_name
    # Extract form data

    PRICE = request.form['PRICE']
    PRODUCT = request.form['PRODUCT']
    YEAR = request.form['YEAR']
    BRAND = request.form['BRAND']
    BRAND_MODEL = request.form['BRAND_MODEL']
    SERIAL_NUMBER = request.form['SERIAL_NUMBER']
    PURPOSE = request.form['PURPOSE']
    OPERATING_SYSTEM = request.form['OPERATING_SYSTEM']

    CPU_BRAND = request.form['CPU_BRAND']
    CPU_AMD_MODEL = request.form['CPU_AMD_MODEL']
    CPU_INTEL_MODEL = request.form['CPU_INTEL_MODEL']
    CPU_QUALCOMM_MODEL = request.form['CPU_QUALCOMM_MODEL']

    GPU_NUMBER = request.form['GPU_NUMBER']
    GPU_INTEGRATED_BRAND = request.form['GPU_INTEGRATED_BRAND']
    GPU_INTEL_INTEGRATED = request.form['GPU_INTEL_INTEGRATED']
    GPU_AMD_INTEGRATED = request.form['GPU_AMD_INTEGRATED']

    GPU_INTEGRATED = ''

    # Concatenate the fields only if they are not empty
    if GPU_INTEGRATED_BRAND:
        GPU_INTEGRATED += GPU_INTEGRATED_BRAND
    if GPU_INTEL_INTEGRATED:
        GPU_INTEGRATED += GPU_INTEL_INTEGRATED
    if GPU_AMD_INTEGRATED:
        GPU_INTEGRATED += GPU_AMD_INTEGRATED

    GPU_DEDICATED_BRAND = request.form['GPU_DEDICATED_BRAND']
    GPU_INTEL_DEDICATED = request.form['GPU_INTEL_DEDICATED']
    GPU_AMD_DEDICATED = request.form['GPU_AMD_DEDICATED']
    GPU_NVIDIA_DEDICATED = request.form['GPU_NVIDIA_DEDICATED']

    GPU_DEDICATED = ''

    # Concatenate the fields only if they are not empty
    if GPU_INTEGRATED_BRAND:
        GPU_INTEGRATED += GPU_DEDICATED_BRAND
    if GPU_INTEL_INTEGRATED:
        GPU_INTEGRATED += GPU_INTEL_DEDICATED
    if GPU_AMD_INTEGRATED:
        GPU_INTEGRATED += GPU_AMD_DEDICATED
    if GPU_AMD_INTEGRATED:
        GPU_INTEGRATED += GPU_NVIDIA_DEDICATED

    DRIVE_NUMBER = request.form['DRIVE_NUMBER']
    DRIVE_TYPE = request.form['DRIVE_TYPE']
    DRIVE_CAPACITY = request.form['DRIVE_CAPACITY']
    DRIVE1 = DRIVE_CAPACITY + '.' + DRIVE_TYPE

    DRIVE2_TYPE = request.form['DRIVE2_TYPE']
    DRIVE2_CAPACITY = request.form['DRIVE2_CAPACITY']
    DRIVE2 = DRIVE2_CAPACITY + '.' + DRIVE2_TYPE

    DRIVE3_TYPE = request.form['DRIVE3_TYPE']
    DRIVE3_CAPACITY = request.form['DRIVE3_CAPACITY']
    DRIVE3 = DRIVE3_CAPACITY + '.' + DRIVE3_TYPE

    # Initialize variables
    NVME_DRIVE = ""
    SATA_DRIVE = ""
    HDD_DRIVE = ""

    # Concatenate values based on text presence
    if "NVME" in DRIVE1:
        NVME_DRIVE += DRIVE1
    if "SATA" in DRIVE1:
        SATA_DRIVE += DRIVE1
    if "hdd" in DRIVE1.lower():
        HDD_DRIVE += DRIVE1

    if "NVME" in DRIVE2:
        NVME_DRIVE += DRIVE2
    if "SATA" in DRIVE2:
        SATA_DRIVE += DRIVE2
    if "hdd" in DRIVE2.lower():
        HDD_DRIVE += DRIVE2

    if "NVME" in DRIVE3:
        NVME_DRIVE += DRIVE3
    if "SATA" in DRIVE3:
        SATA_DRIVE += DRIVE3
    if "hdd" in DRIVE3.lower():
        HDD_DRIVE += DRIVE3





    RAM_NUMBER = request.form['RAM_NUMBER']
    RAM_TYPE = request.form['RAM_TYPE']
    RAM_CAPACITY = request.form['RAM_CAPACITY']

    RAM = RAM_CAPACITY + '.' + RAM_TYPE

    SCREEN_TYPE = request.form['SCREEN_TYPE']
    SCREEN_SIZE = request.form['SCREEN_SIZE']
    SCREEN_RESOLUTION = request.form['SCREEN_RESOLUTION']
    SCREEN_CONDITION = request.form['SCREEN_CONDITION']
    KEYBOARD_LAYOUT = request.form['KEYBOARD_LAYOUT']
    KEYBOARD_CONDITION = request.form['KEYBOARD_CONDITION']
    LAPTOP_POWER_STATUS = request.form['LAPTOP_POWER_STATUS']
    LAPTOP_CHARGER = request.form['LAPTOP_CHARGER']
    LAPTOP_USB = request.form['LAPTOP_USB']
    LAN_PORT = request.form['LAN_PORT']
    WIFI_CONDITION = request.form['WIFI_CONDITION']
    BLUETOOTH_CONDITION = request.form['BLUETOOTH_CONDITION']

    max_id = db.session.query(func.max(laptops_listing.id)).scalar()

    # Increment the max_id by 1 (or start from 1 if table is empty)
    new_id = (int(max_id or 0)) + 1

    new_listing = laptops_listing(
        id=new_id,
        post_id=user_id,
        PRICE=PRICE,
        PRODUCT=PRODUCT,
        YEAR=YEAR,
        BRAND=BRAND,
        BRAND_MODEL=BRAND_MODEL,
        SERIAL_NUMBER=SERIAL_NUMBER,
        PURPOSE=PURPOSE,
        OPERATING_SYSTEM=OPERATING_SYSTEM,
        PROCESSOR_TYPE=CPU_BRAND,
        CPU_AMD_MODEL=CPU_AMD_MODEL,
        CPU_INTEL_MODEL=CPU_INTEL_MODEL,
        CPU_QUALCOMM_MODEL=CPU_QUALCOMM_MODEL,
        GRAPHICS_NUMBER=GPU_NUMBER,
        GPU_INTEGRATED=GPU_INTEGRATED,
        DEDICATED_BRAND=GPU_DEDICATED_BRAND,
        GPU_DEDICATED=GPU_DEDICATED,
        DRIVE_NUMBER=DRIVE_NUMBER,
        DD_NVME_SSD=NVME_DRIVE,
        DD_SATA_SSD=SATA_DRIVE,
        DD_HDD=HDD_DRIVE,
        RAM_CAPACITY=RAM,
        SCREEN_TYPE=SCREEN_TYPE,
        SCREEN_SIZE=SCREEN_SIZE,
        SCREEN_RESOLUTION=SCREEN_RESOLUTION,
        LAPTOP_CHARGER=LAPTOP_CHARGER,
        CONDITION_POWER_STATUS=LAPTOP_POWER_STATUS,
        CONDITION_SCREEN=SCREEN_CONDITION,
        CONDITION_KEYBOARD=KEYBOARD_CONDITION,
        CONDITION_LAPTOP_USB=LAPTOP_USB,
        CONDITION_LAN_PORT=LAN_PORT,
        CONDITION_WIFI=WIFI_CONDITION,
        CONDITION_BLUETOOTH=BLUETOOTH_CONDITION
)
    db.session.add(new_listing)
    db.session.commit()

    # Redirect to a success page or another appropriate page
    return 'Form submitted successfully'


@users.route('/delete_listing', methods=['POST'])
def delete_listing():
    try:
        # Get the id from the request data
        data = request.get_json()
        post_id = data.get('id')

        # Return a confirmation message to the client
        return jsonify({'confirm': 'Are you sure you want to delete this post?'}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to initiate deletion: {}'.format(str(e))}), 500


@users.route('/confirm_delete_listing', methods=['POST'])
def confirm_delete_listing():
    try:
        # Get the id from the request data
        data = request.get_json()
        post_id = data.get('id')

        # Perform deletion logic
        laptops_listing.query.filter_by(id=post_id).delete()
        db.session.commit()

        # return success response
        return jsonify({'message': 'Post deleted successfully'}), 200
    except Exception as e:
        # Rollback the transaction in case of error
        db.session.rollback()

        # Return error response
        return jsonify({'error': 'Deletion failed: {}'.format(str(e))}), 500
