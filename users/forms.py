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

brands_categories = db.Table('brands_categories',
                             db.Column('brand_id', db.Integer, db.ForeignKey('brands.id'), primary_key=True),
                             db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
                             )


@login_manager.user_loader
def load_user(user_id):
    """Load user details"""
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    photo = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    role = db.Column(db.String(60), nullable=False, default='customer')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
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


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    alias = db.Column(db.String(64), nullable=False)
    image = db.Column(db.String(128), nullable=False)
    enabled = db.Column(db.Boolean, default=True)

    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    parent = db.relationship('Category', remote_side=[id], backref='children')

    all_parents_id = db.Column(db.String(256))

    def __init__(self, name):
        self.image = "default.png"
        self.alias = name
        self.name = name

    def __init__(self, name, parent):
        self.__init__(name)
        self.parent = parent

    def __init__(self, id, name, alias):
        self.id = id
        self.name = name
        self.alias = alias

    @property
    def has_children(self):
        return len(self.children) > 0

    @property
    def image_path(self):
        if self.id is None:
            return "../static/images/image-thumbnail.png"
        return f"../static/images/categories-images/{self.id}/{self.image}"

    def __repr__(self):
        return "<Category(name='%s', alias='%s')>" % (self.name, self.alias)

    @classmethod
    def copy_id_and_name(cls, category):
        category1 = cls()
        category1.id = category.id
        category1.name = category.name
        return category1

    @classmethod
    def copy_id_and_name2(cls, id, name):
        category = cls()
        category.id = id
        category.name = name
        return category

    @classmethod
    def copy_full(cls, category, name=None):
        category1 = cls()
        category1.id = category.id
        category1.name = category.name
        category1.image = category.image
        category1.alias = category.alias
        category1.enabled = category.enabled
        category1.hasChildren = bool(category.children)
        if name:
            category1.name = name
        return category1


class Brand(db.Model):
    """This is the brand model
    We have a One-To-Many relationship between the Brand
    and Categories."""
    __tablename__ = 'brands'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    logo = db.Column(db.String(20), nullable=False, default='default.jpg')
    categories = db.relationship('Category', secondary=brands_categories, backref=db.backref('brands', lazy=True))

    def __init__(self, name, logo="brand-logo.png"):
        self.name = name
        self.logo = logo

    def get_logo_path(self):
        if self.id is None:
            return "../static/images/image-thumbnail.png"
        return f"../static/images/brand-logos/{self.id}/{self.logo}"


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

    def validate_username(self, username):
        """Validate fields - username"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken, please choose another one")

    def validate_email(self, email):
        """Validate fields - password"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken, please choose another one")


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
