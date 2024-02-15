import os
import secrets
from PIL import Image
from flask_mail import Message
from CeeVee_Online import mail
from flask import current_app, url_for


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
