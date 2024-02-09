from flask import Flask, render_template, url_for, flash, redirect, request
from forms import SignUpForm, SignInForm
from models import app, db
from flask_bcrypt import Bcrypt
from flask_login import current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from models.user import User
from models.role import Role
from utils.util import send_reset_email

#
# app = Flask(__name__)
#
# app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ousmane2022&&!@localhost/ceevee'
# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'
# app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
# app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
# mail = Mail(app)



@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/categories")
def categories():
    return render_template('listings.html', title='Categories')


@app.route("/laptops")
def laptops():
    return render_template("laptop.html", title="Laptops")


@app.route("/listings")
def listings():
    return render_template("listings.html", title="Listing")


@app.route("/listing")
def listing():
    return render_template("listing.html", title="Listing")


@app.route("/signup", methods=('GET', 'POST'))
def sign_up():
    """Signup view function. Handles signup form validations
    Return: signup view
    """
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = SignUpForm()

    if form.validate_on_submit():
        # checks if all fields are validated when submitted
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data,
                    email=form.email.data, password=hashed_password)
        user.roles.append(form.roles.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account has been created successfully', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='SignUp', form=form)


@app.route("/login", methods=('GET', 'POST'))
def login():
    form = SignInForm()

    # checks if all fields are validated when submitted
    if form.validate_on_submit():
        """Temp data to stimulate login success, change later with actual data from db
         """
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login unsuccessful, please check email or password!", 'danger')
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    """Logout a logged-in user"""
    logout_user();
    return redirect(url_for('home'))


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    """Ask for a reset password request"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password", 'info');
        return redirect(url_for('login'))
    return render_template('reset_request.html',
                           form=form, title='Reset Password')


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    """Reset user's token"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = User.verify_reset_token(token)
    if not user:
        flash('Token invalid or expired', 'warning')
        return redirect(url_for('reset_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated! You're now able to login", 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html',
                           form=form, title='Reset Token')

# with app.app_context():
#     db.create_all()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
