from CeeVee_Online import db
from CeeVee_Online.app import app
from CeeVee_Online.models.CategoryRepository import *
from CeeVee_Online.users.forms import Category
import unittest


class TestCategory(unittest.TestCase):
    """Test all the categories functionalities"""
    category = Category.query.filter_by(id=id)

    def setUp(self):
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_create_category(self):
        """
        Create a category for testing
      """
        category_ = Category(id=1, name="Laptops", alias="PC")
        app.app_context().push()
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
        update_enabled_category(self.category.id, True)  # Update the enabled status of the category
        updated_category = Category.query.get(self.category.id)
        assert updated_category.enabled == True  # Check if the enabled status has been updated


if __name__=='__main__':
    unittest.main()