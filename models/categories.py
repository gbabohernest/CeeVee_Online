from models import db


class Category(db.Model):
    """
    This is the category model.
    """
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    brand_id = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(50), nullable=False)
    alias = db.Column(db.String(50), nullable=False)

