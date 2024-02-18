from CeeVee_Online.users.forms import Category
from CeeVee_Online.main.category_errors import CategoryNotFoundException
from CeeVee_Online.categories.category_service import CategoryService
from CeeVee_Online.categories.category_page_infor import CategoryPageInfor
from CeeVee_Online.users.utils import save_picture
from CeeVee_Online.categories.brand_service import BrandService
from flask import render_template, request, redirect, url_for, flash, Blueprint
from CeeVee_Online.users.forms import Brand
import os

categories = Blueprint("categories", __name__)
category_service = CategoryService()
brand_service = BrandService()


@categories.route("/categories/all", methods=["GET"])
def list_by_first_page():
    all_categories = category_service.get_all_categories()
    return render_template("index.html", categories=all_categories)


# @categories.route("/categories", methods=["GET"])
# def list_by_first_page():
#     sort_dir = request.args.get("sortDir", default='', type=str)
#     return list_by_page(1, sort_dir, None)


@categories.route("/categories/new", methods=["GET"])
def create_form():
    list_categories = category_service.list_all_categories_in_form()
    category = Category()
    return render_template("categories/category_form.html", category=category, listCategories=list_categories,
                           pageTitle="Create New Category")


@categories.route("/categories/save", methods=["POST"])
def save_category():
    category = request.form.get("category")
    file_image = request.files["fileImage"]

    if file_image.filename is not None:
        save_picture(file_image)
    else:
        category_service.save_category(category)

    flash(f"The Category with the ID: {category.id} has been saved successfully", "success")
    return redirect(url_for("list_by_first_page"))


@categories.route("/categories/edit/<id>", methods=["GET"])
def edit_category(id):
    try:
        category = category_service.get_user_by_id(id)
        list_categories = category_service.list_all_categories_in_form()
        return render_template("categories/category_form.html", category=category, listCategories=list_categories,
                               pageTitle=f"Edit Category With (ID: {id})")
    except CategoryNotFoundException as e:
        flash(e.message, "error")
        return redirect(url_for("list_by_first_page"))


@categories.route("/delete/category/<id>", methods=["GET"])
def delete_category(id):
    try:
        category_service.delete_category(id)
        category_dir = f"../static/images/category-images/{id}"
        if os.path.exists(category_dir):
            os.rmdir(category_dir)
        flash(f"The category with the ID of {id} has been deleted successfully", "success")
    except CategoryNotFoundException as e:
        flash(e.message, "error")

    return redirect(url_for("list_by_first_page"))


@categories.route("/categories/<id>/enabled/<status>", methods=["GET"])
def enabled_update(id, status):
    status_bool = status.lower() == 'true'
    category_service.delete_category(id, status_bool)
    status_msg = "enabled" if status_bool else "disabled"
    flash(f"The Category with the Id of: {id} has been {status_msg}", "success")
    return redirect(url_for("list_by_first_page"))


@categories.route("/categories/page/<int:pageNum>", methods=["GET"])
def list_by_page(pageNum):
    sort_dir = request.args.get("sortDir", default="asc", type=str)
    keyword = request.args.get("keyword", default="", type=str)

    page_info = CategoryPageInfor()
    category_list = category_service.list_by_page(page_info, pageNum, sort_dir, keyword)
    start_count = (pageNum - 1) * CategoryService.ROOT_CATEGORIES_PER_PAGE + 1
    end_count = start_count + CategoryService.ROOT_CATEGORIES_PER_PAGE - 1
    if end_count > page_info.total_elements:
        end_count = page_info.total_elements
    reverse_sort_dir = "desc" if sort_dir == "asc" else "asc"

    return render_template("categories/categories.html", totalPages=page_info.total_pages,
                           totalItems=page_info.total_elements,
                           currentPage=pageNum, sortField="name", sortDir=sort_dir, keyword=keyword,
                           startCount=start_count,
                           endCount=end_count, categoryList=category_list, reverseSortDir=reverse_sort_dir)


@categories.route("/brands", methods=["GET"])
def get_all_brands():
    return list_by_page2(1, "name", "asc", None)


@categories.route("/brands/createNew", methods=["GET"])
def create_new_brand():
    list_categories = category_service.list_all_categories_in_form()
    brand = Brand()
    return render_template("brands/brands_form.html", listCategories=list_categories, brand=brand,
                           pageTitle="Create New Brand")


@categories.route("/brands/update/<id>", methods=["GET"])
def edit_brand(id):
    try:
        brand = brand_service.get_brand_by_id(id)
        list_categories = category_service.listAllCategoriesInForm()
        return render_template("brands/brands_form.html", brand=brand, listCategories=list_categories,
                               pageTitle=f"Edit Brand (ID: {id})")
    except Exception as e:
        flash(e.message, "error")
        return redirect(url_for("get_all_brands"))


@categories.route("/brands/delete/<id>", methods=["GET"])
def delete_brand(id):
    try:
        brand_service.delete_brand(id)
        brand_dir = f"../static/images/brand-logos/{id}"
        if os.path.exists(brand_dir):
            os.rmdir(brand_dir)
        flash(f"The brand with the ID of {id} has been deleted successfully", "success")
    except Exception as e:
        flash(e.message, "error")
    return redirect(url_for("get_all_brands"))


@categories.route("/brands/save", methods=["POST"])
def save_brand():
    brand = Brand(request.form["name"], request.form["logo"])
    file_image = request.files["fileImage"]

    if file_image.filename != "":
        save_brand(file_image)
    else:
        brand_service.save_brand(brand)
    flash("The Brand has been saved successfully", "success")
    return redirect(url_for("get_all_brands"))


@categories.route("/brands/page/<pageNum>", methods=["GET"])
def list_by_page2(pageNum):
    sort_field = request.args.get("sortField", default="name", type=str)
    sort_dir = request.args.get("sortDir", default="asc", type=str)
    keyword = request.args.get("keyword", default="", type=str)
    page_list = brand_service.list_by_page(pageNum, sort_field, sort_dir, keyword)
    total_pages = page_list.total_pages
    start_count = (pageNum - 1) * BrandService.BRAND_PER_PAGE + 1
    end_count = start_count + BrandService.BRAND_PER_PAGE - 1
    if end_count > page_list.total_elements:
        end_count = page_list.total_elements
    reverse_sort_dir = "desc" if sort_dir == "asc" else "asc"
    return render_template("brands/brands.html", currentPage=pageNum, totalPages=total_pages,
                           startCount=start_count, end_count=end_count, totalItems=page_list.total_elements,
                           sortField=sort_field, sortDir=sort_dir, reverseSortSir=reverse_sort_dir,
                           keyword=keyword, listAllBrands=page_list.items)
