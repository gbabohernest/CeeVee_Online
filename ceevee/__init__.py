from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_mail import Mail
from ceevee.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    """Create the application"""
    app = Flask(__name__)
    with app.app_context():
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ousmane2022&&!@localhost/ceevee'
        app.config.from_object(Config)

        db.init_app(app)
        bcrypt.init_app(app)
        mail.init_app(app)
        login_manager.init_app(app)

        from ceevee.utils.util import utils
        from ceevee.errors.handlers import errors
        from ceevee.utils.categories import categories

        app.register_blueprint(utils)
        app.register_blueprint(errors)
        app.register_blueprint(categories)

    return app
