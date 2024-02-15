from flask import Blueprint, render_template, url_for, flash, redirect
from ceevee.utils.util import save_picture
from ceevee import db
from ceevee.models.categories import Category

categories = Blueprint("categories", __name__)


@categories.route("/categories", methods=['GET', 'POST', 'PUT'])
def categories_():
    """Add a category"""
    all_categories = Category.query.all()
    if all_categories:
        return render_template("categories.html",
                               all_categories=all_categories, title='Categories')


@categories.route("/categories/<int:cat_id>", methods=['GET', 'POST', 'PUT'])
def category(cat_id):
    """Get a category"""
    cat = Category.query.get_or_404(cat_id)
    return render_template("cat.html", cat=cat)


@categories.route("/categories/<int:cat_id>/delete",
                  methods=['GET', 'POST', 'PUT', 'DELETE'])
def delete_category(cat_id):
    """Delete a category"""
    cat = Category.query.get_or_404(cat_id)
    db.session.delete(cat);
    db.session.commit();
    flash('The category has been deleted!', 'success')
    return redirect(url_for('utils.home'));
