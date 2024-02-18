from CeeVee_Online.models.CategoryRepository import *
from CeeVee_Online.main.category_errors import CategoryNotFoundException
from sqlalchemy import asc, desc


class CategoryService:
    ROOT_CATEGORIES_PER_PAGE = 4

    @staticmethod
    def list_by_page(category_info, page_number, sort_dir, keyword):
        sort = asc(Category.name) if sort_dir == 'asc' else desc(Category.name)

        if keyword:
            page_categories = Category.query.filter(Category.name.ilike(f"%{keyword}%")) \
                .paginate(page=page_number, per_page=CategoryService.ROOT_CATEGORIES_PER_PAGE)
        else:
            page_categories = Category.query.filter_by(parent=None).order_by(sort) \
                .paginate(page=page_number, per_page=CategoryService.ROOT_CATEGORIES_PER_PAGE)
        root_categories = page_categories.items
        category_info['total_elements'] = page_categories.total
        category_info['total_pages'] = page_categories.pages

        if keyword:
            search_result = page_categories.items
            for category in search_result:
                category.set_has_children(len(search_result) > 0)
            return search_result
        else:
            return category_info.list_hierarchical_categories(root_categories, sort_dir)

    @staticmethod
    def list_all_categories_in_form():

        categories_inform = []
        categories_in_db = Category.query.filter_by(parent=None).order_by(asc(Category.name)).all()

        for category in categories_in_db:
            if category.parent is None:
                categories_inform.append(Category.copy_id_name(category))
                children = CategoryService.sort_sub_categories(category.children)
                for sub_category in children:
                    format_ = "--" + sub_category.name
                    categories_inform.append(Category.copy_id_name(sub_category.id, format_))
                    CategoryService.list_sub_categories_used_in_form(categories_inform, sub_category, 1)

        return categories_inform

    @staticmethod
    def save_category(category):
        parent = category.parent
        if parent:
            all_parent_ids = parent.all_parent_ids or "-"
            all_parent_ids += str(parent.id) + "-"
            category.all_parent_ids = all_parent_ids
        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def get_category_by_id(category_id):
        category = Category.query.get(category_id)
        if not category:
            raise Exception(f"Sorry! Couldn't find any category with the ID of: {category_id}")
        return category

    @staticmethod
    def delete_category(category_id):
        category = Category.query.get(category_id)
        if not category:
            raise Exception(f"Sorry! Couldn't find any category with the ID of: {category_id}")
        db.session.delete(category)
        db.session.commit()

    @staticmethod
    def check_unique_category(category_id, name, alias):
        is_creating_new = not category_id
        category_by_name = Category.query.filter_by(name=name).first()
        category_by_alias = Category.query.filter_by(alias=alias).first()

        if is_creating_new:
            if category_by_name:
                return "DuplicateName"
            elif category_by_alias:
                return "DuplicateAlias"
        else:
            if category_by_name and category_by_name.id != category_id:
                return "DuplicateName"
            elif category_by_alias and category_by_alias.id != category_id:
                return "DuplicateAlias"
        return "OK"

    @staticmethod
    def sort_sub_categories(children):
        return sorted(children, key=lambda x: x.name)

    @staticmethod
    def list_hierarchical_categories(root_categories, sort_dir):
        hierarchical_categories = []

        for root_category in root_categories:
            hierarchical_categories.append(root_category)
            children = CategoryService.sort_sub_categories(root_category.children)

            for sub_category in children:
                name = "--" + sub_category.name
                hierarchical_categories.append(Category.copy_full(sub_category, name))
                CategoryService.list_sub_categories_used_in_form(hierarchical_categories, sub_category, 1, sort_dir)

        return hierarchical_categories

    @staticmethod
    def list_sub_categories_used_in_form(categories_inform, parent, sub_level):
        children = CategoryService.sort_sub_categories(parent.children)

        for sub_category in children:
            name = "-" * (sub_level * 2) + sub_category.name
            categories_inform.append(Category.copy_id_and_name2(sub_category.id, name))
            CategoryService.list_sub_categories_used_in_form(categories_inform, sub_category, sub_level + 1)

    @staticmethod
    def get_all_categories():
        return Category.query.all()

    @staticmethod
    def get_category_by_name(name):
        return Category.query.filter_by(name=name).first()

    @staticmethod
    def get_category(alias):
        category = find_by_alias(alias)
        if category is None:
            raise CategoryNotFoundException(
                f"Couldn't find any category with alias {alias}"
            )
        return category

    @staticmethod
    def list_not_children_categories(self):
        list_not_children = []
        list_enabled_categories = find_all_enabled()

        for category in list_enabled_categories:
            if not category.children:
                list_not_children.append(category)

        return list_not_children

    @staticmethod
    def get_category_parents(child):
        list_parents = []
        parent = child.parent

        while parent is not None:
            list_parents.insert(0, parent)
            parent = parent.parent

        list_parents.append(child)
        return list_parents
