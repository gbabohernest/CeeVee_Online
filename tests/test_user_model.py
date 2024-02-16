import unittest
from CeeVee_Online import db, bcrypt
from CeeVee_Online.users.forms import User, Category
from CeeVee_Online.app import app
from CeeVee_Online.models.model import Product, ProductImage, ProductDetail

class TestModel(unittest.TestCase):
    """Test case for User and Role model """

    def test_create_schema(self):
        """Create all table in the database"""
        app.app_context().push()
        db.create_all()
        db.session.commit()
        db.session.commit()

    def test_create_category(self):
        """
        Create a category for testing
      """
        category = Category.query.filter_by(id=1)

        category_ = Category(id=1, name="Laptops", alias="PC")
        db.session.add(category_)
        db.session.commit()
        print(category_)
        self.assertEqual(category_.name, "Laptops")

    def test_root_categories(self):
        """Test the root or parent categories"""
        root_categories = find_root('name')  # Assuming 'name' as the sort parameter
        counter = 0
        for category in root_categories:
            print("{}".format(category))
            counter += 1
        self.assertEqual(root_categories, counter)

    def test_count_category(self):
        """Count categories"""
        # Test count_by_id method
        category = Category.query.filter_by(id=1)

        count = count_by_id(self.category.id)  # Count the number of categories with the test category's ID
        self.assertTrue(count == 1)  # Check if the count is 1 for the test category's ID

    def test_category_by_alias(self):
        """
        Test find_by_alias method
        """
        retrieved_category_by_alias = find_by_alias("PC")
        assert retrieved_category_by_alias == self.category  # Check if the retrieved category matches the created category

    def test_update_category(self):
        """
        Test update_enabled_category method
        """
        category = Category.query.filter_by(id=1)

        update_enabled_category(self.category.id, True)  # Update the enabled status of the category
        updated_category = Category.query.get(self.category.id)
        assert updated_category.enabled == True  # Check if the enabled status has been updated

    def test_password(self):
        """Test bcrypt password"""
        password = "Ousmane"
        hashed_pass = bcrypt.generate_password_hash(password).decode("utf")
        print(hashed_pass)
        self.assertTrue(bcrypt.check_password_hash(hashed_pass, password))

    def test_user_model(self):
        """Create user"""
        password = "jalloh"
        hashed_pass = bcrypt.generate_password_hash(password).decode("utf")
        user = User(first_name="Francis", last_name="George",
                    email="sangary7683@yahoo.com", password=hashed_pass, role="Admin")
        app.app_context().push()
        db.session.add(user)
        db.session.commit()
        print(f'{user.first_name}, {user.last_name}')
        self.assertEqual(user.password, hashed_pass)


if __name__ == '__main__':
    unittest.main()
