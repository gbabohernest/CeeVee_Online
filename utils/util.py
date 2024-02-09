from flask import url_for
from flask_mail import Message
from app import mail


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
