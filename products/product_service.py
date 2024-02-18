from CeeVee_Online.models.product_repository import *
from CeeVee_Online.models.model import Product
from CeeVee_Online.main.category_errors import ProductNotFoundException


class ProductService:
    PRODUCTS_PER_PAGE = 10
    SEARCH_RESULT_PER_PAGE = 10

    def list_by_category(self, page_num, cat_id):
        pagination = Product.query.paginate(page=page_num, per_page=self.PRODUCTS_PER_PAGE)
        match = f"-{cat_id}-"
        return list_by_category(page_num, match, pagination)

    def list_by_cat(self, cat_alias):
        product = Product.query.filter(Product.category.has(alias=cat_alias)).all()
        return product

    def get_product_by_alias(self, alias):
        product = find_by_alias(alias)
        if product is None:
            raise ProductNotFoundException(f"Couldn't find any product with alias: {alias}")
        return product

    def search(self, keyword, page_num):
        pagination = Product.query.paginate(page_num - 1, per_page=self.SEARCH_RESULT_PER_PAGE)
        return search(keyword, pagination)
