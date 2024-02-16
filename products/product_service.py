from CeeVee_Online.models.product_repository import *
from CeeVee_Online.models.model import Product
from CeeVee_Online.main.category_errors import ProductNotFoundException


class ProductService:
    PRODUCTS_PER_PAGE = 10
    SEARCH_RESULT_PER_PAGE = 10

    def list_by_category(self, page_num, category_id):
        pagination = Product.query.paginate(page=page_num, per_page=self.PRODUCTS_PER_PAGE)
        match = f"-{category_id}-"
        return list_by_category(category_id, match, pagination)

    def get_product_by_alias(self, alias):
        product = find_by_alias(alias)
        if product is None:
            raise ProductNotFoundException(f"Couldn't find any product with alias: {alias}")
        return product

    def search(self, keyword, page_num):
        pagination = Product.query.paginate(page_num - 1, per_page=self.SEARCH_RESULT_PER_PAGE)
        return search(keyword, pagination)
