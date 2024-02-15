from ceevee import db
from flask import abort
import functools
from flask_login import current_user


class Role(db.Model):
    """ Module for users roles"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    role_description = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "User('{}', '{}', '{}')" \
            .format(self.id, self.name, self.role_description)


def role_required(*role_names):
    """Custom role permission for users"""

    def decorator(func):
        @functools.wraps(func)
        def decorated_function(*args, **kwargs):
            if current_user_is_admin_or_in_roles(role_names):
                return func(*args, **kwargs)
            else:
                abort(403)  # Or redirect to a different page, or display an error message

        return decorated_function

    return decorator


def current_user_is_admin_or_in_roles(role_names):
    if current_user.is_admin:
        return True
    else:
        for role in current_user.roles:
            if role.name in role_names:
                return True
        return False
