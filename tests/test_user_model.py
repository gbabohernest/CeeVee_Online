import unittest
from CeeVee_Online import db, bcrypt
from CeeVee_Online.users.forms import User, Role
from CeeVee_Online.app import app

class TestModel(unittest.TestCase):
    """Test case for User and Role model """

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
                    email="sangary7683@yahoo.com", password=hashed_pass)
        role_name = Role(name="Assistant", role_description="Assist with everything")
        app.app_context().push()
        user.roles.append(role_name)
        db.session.add(user)
        db.session.commit()

        print(f'{user.first_name}, {user.last_name}')
        self.assertEqual(user.password, hashed_pass)



if __name__=='__main__':
    unittest.main()