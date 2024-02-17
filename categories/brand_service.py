from CeeVee_Online import db


class BrandService:
    BRAND_PER_PAGE = 4

    def __init__(self):
        self.brand_repository = db.session

    def list_all_brands(self):
        return self.brand_repository.query.all()

    def list_by_page(self, page_num, sort_field, sort_dir, keyword):
        sort = sort_field if sort_dir == "asc" else f"{sort_field} DESC"
        # Perform the query using the sort and keyword, limit, and pagination
        results = self.brand_repository.query.filter(self.brand_repository.name.like(f"%{keyword}%"))\
            .order_by(sort).paginate(page_num, per_page=self.BRAND_PER_PAGE)
        return results

    def get_brand_by_id(self, id):
        """Get a brand by ID"""
        return self.brand_repository.query.get_or_404(id)

    def delete_brand(self, id):
        """Delete a brand from the DB"""
        brand = self.get_brand_by_id(id)
        db.session.delete(brand)
        db.session.commit()

    def save_brand(self, brand):
        """Save Brand"""
        db.session.add(brand)
        db.session.commit()

    def check_unique_brand(self, id, name):
        is_creating_new = (id is None or id == 0)
        if is_creating_new:
            existing_brand = self.brand_repository.query.filter_by(name=name).first()
            return "Duplicate" if existing_brand else "OK"
        else:
            existing_brand = self.brand_repository.query.filter(self.brand_repository.id != id, self.brand_repository.name == name).first()
            return "Duplicate" if existing_brand else "OK"

