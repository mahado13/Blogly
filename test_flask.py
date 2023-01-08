from unittest import TestCase
from urllib import response

from app import app
from models import db, Users

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bloglytest'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UsersViewTestCase(TestCase):
    def setUp(self):
        """Add sample pet."""

        Users.query.delete()

        user = Users(first_name="Test1", last_name="Test1", image_url="https://upload.wikimedia.org/wikipedia/commons/e/e9/Felis_silvestris_silvestris_small_gradual_decrease_of_quality.png")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    
    def test_show_users(self):
       """Testing our home page"""
       with app.test_client() as client:
           res = client.get("/")
           html = res.get_data(as_text = True)

           self.assertEqual(res.status_code, 200)
           self.assertIn('Test1', html)

    def test_user_profile(self):
        """Testing User Profile"""
        with app.test_client() as client:
            res = client.get(f"/users/{self.user_id}")
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Test1 Test1 Profile</h1>', html)

    def test_adding_user(self):
        """Testing adding a User"""
        with app.test_client() as client:
           u = {"first_name":"Test2", "last_name": "Test2", "image_url":"https://upload.wikimedia.org/wikipedia/commons/e/e9/Felis_silvestris_silvestris_small_gradual_decrease_of_quality.png"}
           res = client.post("/users/new", data=u, follow_redirects=True)
           html = res.get_data(as_text=True)

           self.assertEqual(res.status_code, 200)
           self.assertIn('Test2', html)

    def test_deleting_user(self):
        """Testing deleting a User"""
        with app.test_client() as client:
         u = {"first_name":"Test1", "last_name": "Test1", "image_url":"https://upload.wikimedia.org/wikipedia/commons/e/e9/Felis_silvestris_silvestris_small_gradual_decrease_of_quality.png"}
         res = client.post(f"/users/{self.user_id}/delete", data=u, follow_redirects=True)
         html = res.get_data(as_text = True)

         self.assertEqual(res.status_code, 200)
         self.assertNotIn('Test1', html)

    def test_editing_user(self):
        """Testing Editing a user"""
        with app.test_client() as client:
         u = {"first_name":"Test3", "last_name": "Test3", "image_url":"https://upload.wikimedia.org/wikipedia/commons/e/e9/Felis_silvestris_silvestris_small_gradual_decrease_of_quality.png"}
         res = client.post(f"/users/{self.user_id}/edit", data=u, follow_redirects=True)
         html = res.get_data(as_text = True)

         self.assertEqual(res.status_code, 200)
         self.assertNotIn('Test1', html)
         self.assertIn('Test3', html)
