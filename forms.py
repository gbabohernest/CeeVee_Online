from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from models.role import Role
from models import db, app

class SignUpForm(FlaskForm):
    """A signup form to signup for registering
    users on the site
    """
    first_name = StringField('First Name',
                             validators=[DataRequired()])
    last_name = StringField('Last Name',
                            validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    roles = SelectMultipleField("Roles", coerce=int, validators=[DataRequired()],
                                choices=[(role.id, role.name) for role in Role.query.all()])
    sign_up = SubmitField('Sign Up')

    def validate_email(self, email):
        """Validate users email"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Please try another email")


class SignInForm(FlaskForm):
    """A signIn form to log user in on our site"""

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    sign_in = SubmitField('Sign In')
