from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from CeeVee_Online import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from sqlalchemy import UniqueConstraint
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

""" User class"""
user_role = db.Table('users_roles',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id')))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



""" class User(db.Model, UserMixin):
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
        return User.query.get(user_id); """


class User(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Changed column name
    is_active = db.Column(db.Boolean, default=True)

    __table_args__ = (
        UniqueConstraint('email', name='unique_email'),
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.id




class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    role_description = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "Role('{}', '{}', '{}')" \
            .format(self.id, self.name, self.role_description)


""" class SignUpForm(FlaskForm):
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

    sign_up = SubmitField('Sign Up') """




class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


""" class SignInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    sign_in = SubmitField('Sign In')
 """


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')





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
    PRODUCT = StringField('Product', validators=[DataRequired()])
    YEAR = StringField('Year', validators=[DataRequired()])
    PRICE = StringField('Price', validators=[DataRequired()])
    SERIAL_NUMBER = StringField('Serial number', validators=[DataRequired()])
    SCREEN_TYPE = StringField('Display technology', validators=[DataRequired()])
    SCREEN_SIZE = StringField('input screen size in inches', validators=[DataRequired()])
    BRAND = StringField('Price', validators=[DataRequired()])
    BRAND_MODEL = StringField('Brand model', validators=[DataRequired()])
    PURPOSE = StringField('Purpose', validators=[DataRequired()])
    OPERATING_SYSTEM = StringField('Operating system', validators=[DataRequired()])
    CPU_BRAND = StringField('Cpu brand', validators=[DataRequired()])
    CPU_AMD_MODEL = StringField('AMD CPU model')
    CPU_INTEL_MODEL = StringField('Intel CPU model')
    CPU_QUALCOMM_MODEL = StringField('Qualcomm CPU model')
    GPU_NUMBER = StringField('Number of GPUs', validators=[DataRequired()])
    GPU_INTEGRATED_BRAND = StringField('Integrated GPU brand', validators=[DataRequired()])
    GPU_INTEL_INTEGRATED = StringField('Intel Integrated GPU')
    GPU_AMD_INTEGRATED = StringField('AMD integrated GPU')
    GPU_DEDICATED_BRAND = StringField('Dedicated GPU brand')
    GPU_INTEL_DEDICATED = StringField('Intel Dedicated GPU ')
    GPU_AMD_DEDICATED = StringField('AMD Dedicated GPU')
    GPU_NVIDIA_DEDICATED = StringField('Nvidia Dedicated GPU')
    DRIVE_NUMBER = StringField('Number of Drives', validators=[DataRequired()])
    DRIVE_TYPE = StringField('Drive Type', validators=[DataRequired()])
    DRIVE_CAPACITY = StringField('Drive Capacity', validators=[DataRequired()])
    DRIVE2_TYPE = StringField('Drive 2 Type')
    DRIVE2_CAPACITY = StringField('Drive 2 Capacity')
    DRIVE3_TYPE = StringField('Drive 3 Type')
    DRIVE3_CAPACITY = StringField('Drive 3 Capacity')
    RAM_NUMBER = StringField('Number of RAM modules', validators=[DataRequired()])
    RAM_TYPE = StringField('RAM Type', validators=[DataRequired()])
    RAM_CAPACITY = StringField('Total RAM Capcity', validators=[DataRequired()])
    SCREEN_RESOLUTION = StringField('Screen Resolution', validators=[DataRequired()])
    SCREEN_CONDITION = StringField('Screen Condition', validators=[DataRequired()])
    KEYBOARD_LAYOUT = StringField('Keyboard Layout', validators=[DataRequired()])
    KEYBOARD_CONDITION = StringField('Keyboard Condition', validators=[DataRequired()])
    LAPTOP_POWER_STATUS = StringField('Laptop Power status', validators=[DataRequired()])
    LAPTOP_CHARGER = StringField('Is the charger included', validators=[DataRequired()])
    LAPTOP_USB = StringField('Laptop USB status', validators=[DataRequired()])
    LAN_PORT = StringField('Laptop LAN port status', validators=[DataRequired()])
    WIFI_CONDITION = StringField('WIFI status', validators=[DataRequired()])
    BLUETOOTH_CONDITION = StringField('Bluetooth Condition', validators=[DataRequired()])
