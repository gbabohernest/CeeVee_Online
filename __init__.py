from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from CeeVee_Online.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    """Main entrypoint of the application"""
    app = Flask(__name__)

    with app.app_context():
        app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ousmane2022&&!@localhost/ceevee'
        app.config.from_object(Config)

        db.init_app(app)
        bcrypt.init_app(app)
        mail.init_app(app)
        login_manager.init_app(app)

        from CeeVee_Online.users.routes import users
        from CeeVee_Online.main.category_errors import errors
        from CeeVee_Online.categories.routes import categories
        from CeeVee_Online.products.routes import products

        app.register_blueprint(users)
        app.register_blueprint(errors)
        app.register_blueprint(categories)
        app.register_blueprint(products)
    return app


