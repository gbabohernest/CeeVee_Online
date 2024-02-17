
# from project import app, db
# app.app_context().push()
# db.create_all()
# db.session.commit()
# User.query.all()
# User.query.filter_by(username='Ousmane').all()
# User.query.filter_by(username='Ousmane')
# db.drop_all()
# db.create_all()
from CeeVee_Online import db
from CeeVee_Online.users.forms import Category, Brand
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    alias = db.Column(db.String(256), unique=True, nullable=False)
    short_description = db.Column(db.String(4000), nullable=False)
    full_description = db.Column(db.String(4095), nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    updated_time = db.Column(db.DateTime, onupdate=datetime.utcnow)
    enabled = db.Column(db.Boolean, default=True)
    in_stock = db.Column(db.Boolean, default=True)
    price = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    discount_percent = db.Column(db.Float, default=0)
    length = db.Column(db.Float, nullable=False)
    width = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    main_image = db.Column(db.String(256), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)

    category = db.relationship('Category', backref='products', lazy=True)
    brand = db.relationship('Brand', backref='products', lazy=True)

    def add_extra_image(self, image):
        img = ProductImage(image=image, product=self)
        self.images.append(img)

    def add_product_details(self, name, value):
        detail = ProductDetail(name=name, value=value, product=self)
        self.product_details.append(detail)

    def add_product_details_with_id(self, id, name, value):
        detail = ProductDetail(id=id, name=name, value=value, product=self)
        self.product_details.append(detail)

    @property
    def main_image_path(self):
        if not self.id or not self.main_image:
            return "../static/images/image-thumbnail.png"
        return f"../static/images/product-images/{self.id}/{self.main_image}"

    def contains_image_name(self, image_name):
        return any(image.name == image_name for image in self.images)

    @property
    def short_name(self):
        return self.name[:70] + '..' if len(self.name) > 70 else self.name

    @property
    def discount_price(self):
        return round(self.price * ((100 - self.discount_percent) / 100)) if self.discount_percent > 0 else self.price


class ProductImage(db.Model):
    __tablename__ = 'product_images'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product', backref='images')

    def __init__(self, name, product):
        self.name = name
        self.product = product

    @property
    def image_path(self):
        return f"../static/images/product-images/{self.product_id}/extras/{self.name}"


class ProductDetail(db.Model):
    __tablename__ = 'product_details'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    value = db.Column(db.String(200), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product = db.relationship('Product', backref='product_details')

    def __init__(self, name, value, product):
        self.name = name
        self.value = value
        self.product = product

    def __init__(self, id, name, value, product):
        self.id = id
        self.name = name
        self.value = value
        self.product = product

