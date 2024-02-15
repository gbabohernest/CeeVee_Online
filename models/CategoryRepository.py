from CeeVee_Online import db
from CeeVee_Online.users.forms import Category


def find_root(sort):
    """
           Find root categories sorted by the specified criteria.

           Args:
           sort: The sorting criteria.

           Returns:
           A list of root categories.
           """
    return Category.query.filter_by(parent_id=None).order_by(sort).all()


def find_root_categories_paginated(pageable):
    """
           Find root categories with pagination.

           Args:
           pageable: Pagination information.

           Returns:
           A paginated list of root categories.
           """
    return Category.query.filter_by(parent_id=None).paginate(
        page=pageable.page, per_page=pageable.per_page)


def search(keyword, pageable):
    """
            Search for categories based on the provided keyword with pagination.

            Args:
            keyword: The keyword to search for.
            pageable: Pagination information.

            Returns:
            A paginated list of categories matching the search keyword.
            """
    return Category.query.filter(Category.name.ilike(f"%{keyword}%")) \
        .paginate(page=pageable.page, per_page=pageable.per_page)


def count_by_id(id):
    """
            Count the number of categories with the specified ID.

            Args:
            id: The ID of the category.

            Returns:
            The count of categories with the specified ID.
            """
    return Category.query.filter_by(id=id).count()


def find_by_name(name):
    """
           Find a category by name.

           Args:
           name: The name of the category.

           Returns:
           The category with the specified name.
           """
    return Category.query.filter_by(name=name).first()


def find_by_alias(alias):
    """
           Find a category by alias.

           Args:
           alias: The alias of the category.

           Returns:
           The category with the specified alias.
           """
    return Category.query.filter_by(alias=alias).first()


def update_enabled_category(id, enabled):
    """
           Update the enabled status of a category.

           Args:
           id: The ID of the category.
           enabled: The new enabled status.

           Returns:
           None
           """
    category = Category.query.get(id)
    if category:
        category.enabled = enabled
        db.session.commit()
