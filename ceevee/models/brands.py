from ceevee import db
from ceevee.models.categories import Category


class Brand(db.Model):
    """This is the brand model
    We have a One-To-Many relationship between the Brand
    and Categories."""
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    brand_logo = db.Column(db.String(20), nullable=False, default='default.jpg')
    categories = db.relationship('Category', backref=db.backref('brand'), lazy=True)

    def __repr__(self):
        """Official string rep"""
        return "Brand('{}', '{}', '{}', '{}')" \
            .format(self.id, self.name, self.brand_logo,
                    self.categories)