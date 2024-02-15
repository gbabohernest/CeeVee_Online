from flask import Blueprint, render_template,current_app, url_for, flash, redirect, request
from flask_mail import Message
from ceevee import mail, bcrypt
from ceevee.models.user import User
from ceevee.models.forms import SignUpForm, SignInForm
from flask_login import current_user, logout_user
from PIL import Image
import secrets
import os


utils = Blueprint("utils", __name__)

def send_reset_email(user):
    """Send a reset email request"""
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, please visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}
    If you didn't make this request, kindly ignore this email with no change. Thank you!!
    '''
    mail.send(msg)


@utils.route("/")
@utils.route("/home")
def home():
    return render_template('index.html', title="Home Page")


@utils.route("/categories")
def categories():
    return render_template('listings.html', title='Categories')


@utils.route("/laptops")
def laptops():
    return render_template("laptop.html", title="Laptops")


@utils.route("/listings")
def listings():
    return render_template("listings.html", title="Listing")


@utils.route("/listing")
def listing():
    return render_template("listing.html", title="Listing")

@utils.route("/logout", methods=['GET', 'POST', 'PUT'])
def logout():
    """Logout a logged-in user"""
    logout_user();
    return redirect(url_for('home'))


@utils.route("/reset_password", methods=['GET', 'POST'])
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


@utils.route("/reset_password/<token>", methods=['GET', 'POST'])
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


def save_picture(user_picture):
    """Save user pictures"""
    random_hex = secrets.token_hex(8);
    _, f_extention = os.path.splitext(user_picture.filename);
    picture_fn = random_hex + f_extention
    pic_path = os.path.join(current_app.root_path, '../static/images', picture_fn)
    output_size = (125, 125);
    image = Image.open(user_picture)
    image.thumbnail(output_size)
    image.save(pic_path)

    return picture_fn;