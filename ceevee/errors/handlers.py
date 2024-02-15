from flask import Blueprint, render_template

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(404)
def error_404(error):
    """Page Not found error"""
    return render_template("errors/404.html"), 404;

@errors.app_errorhandler(403)
def error_403(error):
    """Forbidden 403"""
    return render_template('errors/403.html'), 403;

@errors.app_errorhandler(500)
def error_500(error):
    """Internal Server error"""
    return render_template('errors/500.html'), 500;

@errors.app_errorhandler(401)
def error_401(error):
    """UnAuthorized request error"""
    return render_template('errors/401.html'), 401;
