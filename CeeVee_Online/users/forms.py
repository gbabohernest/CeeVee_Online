from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from CeeVee_Online import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

""" User class"""
user_role = db.Table('users_roles',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id')))


@login_manager.user_loader
def load_user(user_id):
    """Load user details"""
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    photo = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    roles = db.relationship('Role', secondary='users_roles', backref='role', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec);
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id);


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    role_description = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "Role('{}', '{}', '{}')" \
            .format(self.id, self.name, self.role_description)


class SignUpForm(FlaskForm):
    """A signup form to signup for registering
    users on the site
    """
    first_name = StringField('First Name',
                             validators=[DataRequired()])
    last_name = StringField('Last Name',
                            validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    sign_up = SubmitField('Sign Up')


class SignInForm(FlaskForm):
    """A signIn form to log user in on our site"""

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    sign_in = SubmitField('Sign In')


class RequestResetForm(FlaskForm):
    """Reset Form"""
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password_reset = StringField("Request Password Reset")
    submit = SubmitField("Send")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class PostingForm(FlaskForm):
    price = StringField('Price', validators=[DataRequired()])
    brand = StringField('Brand', validators=[DataRequired()])
    brand_model = StringField('Brand Model', validators=[DataRequired()])
    serial_number = StringField('Serial Number', validators=[DataRequired()])
    purpose = StringField('Purpose', validators=[DataRequired()])
    operating_system = StringField('Operating System', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])
    processor_type = StringField('Processor Type', validators=[DataRequired()])
    amd_model = StringField('AMD Model', validators=[DataRequired()])
