from flask import render_template, request, Blueprint
from CeeVee_Online.categories.category_service import CategoryService
from CeeVee_Online.products.product_service import ProductService
from CeeVee_Online.main.category_errors import ProductNotFoundException

products = Blueprint("products", __name__)

category_service = CategoryService()
product_service = ProductService()


@products.route("/c/<category_alias>")
@products.route("/c/<category_alias>/page/<int:page_num>")
def view_category(category_alias, page_num=1):
    try:
        category = category_service.get_category(category_alias)
        list_category_parents = category_service.get_category_parents(category)
        page_products = product_service.list_by_category(page_num, category.id)

        start_count = (page_num - 1) * ProductService.PRODUCTS_PER_PAGE + 1
        end_count = min(start_count + ProductService.PRODUCTS_PER_PAGE - 1, page_products.total)

        return render_template("products/products_by_category.html",
                               currentPage=page_num,
                               totalPages=page_products.pages,
                               startCount=start_count,
                               endCount=end_count,
                               totalItems=page_products.total,
                               pageTitle=category.name,
                               listCategoryParents=list_category_parents,
                               listProducts=page_products.items,
                               category=category)
    except ProductNotFoundException as e:
        return render_template("errors/404.html", errors=e.description)


@products.route("/p/<product_alias>")
def view_product_details(product_alias):
    try:
        product = product_service.get_product_by_alias(product_alias)
        list_category_parents = category_service.get_category_parents(product.category)

        return render_template("products/product_detail.html",
                               listCategoryParents=list_category_parents,
                               product=product,
                               category=product.category,
                               pageTitle=product.short_name)
    except ProductNotFoundException as e:
        return render_template("errors/404.html", errors=e.description)


@products.route("/search")
@products.route("/search/page/<int:page_num>")
def search_by_page(page_num=1):
    keyword = request.args.get('keyword', '')
    page_products = product_service.search(keyword, page_num)

    start_count = (page_num - 1) * ProductService.SEARCH_RESULT_PER_PAGE + 1
    end_count = min(start_count + ProductService.SEARCH_RESULT_PER_PAGE - 1, page_products.total)

    return render_template("products/search_result.html",
                           currentPage=page_num,
                           totalPages=page_products.pages,
                           startCount=start_count,
                           endCount=end_count,
                           totalItems=page_products.total,
                           pageTitle=keyword + " - Search Result",
                           listResult=page_products.items,
                           keyword=keyword)
