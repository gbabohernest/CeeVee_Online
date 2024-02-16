from sqlalchemy import text

from CeeVee_Online import db
from CeeVee_Online.models.model import Product


def list_by_category(category_id, category_id_match, pageable):
    query = text(
        f"USE ceevee"
        f"SELECT * FROM products as p"
        f" WHERE p.enabled = true"
        f" AND (p.category_id = :{category_id} OR p.category.all_parents_id LIKE CONCAT('-' || :{category_id_match} || '-%', '%'))"
        f" ORDER BY p.name ASC"
    )
    with db.engine.connect() as connection:
        products = connection.execute(query)
        return products


def find_by_alias(alias):
    return Product.query.filter_by(alias=alias).first()


def search(keyword, pageable):
    query = text(
        "USE ceevee; "
        "SELECT * FROM products as p"
        " WHERE p.enabled = true"
        " AND MATCH(p.name, p.short_description, p.full_description) AGAINST(:keyword)"
    )
    with db.engine.connect() as connection:
        # Execute the query
        products = connection.execute(query, keyword=keyword)
        return products  # Or return the products as needed
