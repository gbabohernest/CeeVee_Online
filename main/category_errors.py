from flask import jsonify, Blueprint
from werkzeug.exceptions import HTTPException

errors = Blueprint("errors", __name__)


class CategoryNotFoundException(HTTPException):
    code = 404
    message = 'Category not found'


class ProductNotFoundException(HTTPException):
    code = 404
    message = 'Product not found'


@errors.errorhandler(CategoryNotFoundException)
def handle_category_not_found_error(e):
    response = jsonify({'error': e.description})
    response.status_code = e.code
    return response


@errors.errorhandler(ProductNotFoundException)
def handle_product_not_found_error(e):
    response = jsonify({'error': e.description})
    response.status_code = e.code
    return response
