from ceevee import db


class Category(db.Model):
    """
    This is the category model.
    """
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    brand_id = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(50), nullable=False)
    alias = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Official string rep of this module"""
        return "Category ('{}', '{}', '{}', '{}')" \
            .format(self.id, self.alias, self.brand_id,
                    self.image)
