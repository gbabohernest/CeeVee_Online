from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FileField, TextAreaField, \
    PasswordField, SubmitField, BooleanField, SelectMultipleField
from wtforms.validators import InputRequired, URL, DataRequired, Length, Email, EqualTo, ValidationError
from ceevee.models.role import Role
from ceevee.models.user import User


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
    sign_up = SubmitField('Sign Up')


class SignInForm(FlaskForm):
    """A signIn form to log user in on our site"""

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    sign_in = SubmitField('Sign In')


class SellingForm(FlaskForm):
    category = StringField('Category', validators=[InputRequired()])
    location = SelectField('Location', choices=[('location1', 'Location 1'), ('location2', 'Location 2'), ('location3', 'Location 3')], validators=[InputRequired()])
    photo1 = FileField('Photo 1', validators=[InputRequired()])
    photo2 = FileField('Photo 2')
    photo3 = FileField('Photo 3')
    photo4 = FileField('Photo 4')
    description = TextAreaField('Description')
    youtube_link = StringField('Link to Youtube video', validators=[URL()])
