from unittest import TestCase
from urllib import response

from app import app
from models import db, Users, Posts

"""
Author: Mahad Osman
Date: Jan 11th 2023
Assignment Blogly part 2
"""

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

        Posts.query.delete()
        Users.query.delete()

        """Setting this in part two to make our tests shorter"""
        self.client = app.test_client()

        user = Users(first_name="Test1", last_name="Test1", image_url="https://upload.wikimedia.org/wikipedia/commons/e/e9/Felis_silvestris_silvestris_small_gradual_decrease_of_quality.png")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        """Adding for our post tests"""
        post = Posts(title ="SPIDER-MAN!", content ="JJJ UNVEILS ALL!", user_id=user.id)
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id


    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
    
    def test_show_users(self):
       """Testing our home page"""
       with self.client:
           res = self.client.get("/")
           html = res.get_data(as_text = True)

        #    print('**************')
        #    print(self.post_id)
        #    print(Posts.query.get(self.post_id))
        #    print('**************')


           self.assertEqual(res.status_code, 200)
           self.assertIn('Test1', html)


    def test_user_profile(self):
        """Testing User Profile"""
        with self.client:
            res = self.client.get(f"/users/{self.user_id}")
            html = res.get_data(as_text = True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1>Test1 Test1 Profile</h1>', html)

    def test_adding_user(self):
        """Testing adding a User"""
        with self.client:
           u = {"first_name":"Test2", "last_name": "Test2", "image_url":"https://upload.wikimedia.org/wikipedia/commons/e/e9/Felis_silvestris_silvestris_small_gradual_decrease_of_quality.png"}
           res = self.client.post("/users/new", data=u, follow_redirects=True)
           html = res.get_data(as_text=True)

           self.assertEqual(res.status_code, 200)
           self.assertIn('Test2', html)

    def test_deleting_user(self):
        """Testing deleting a User"""
        with self.client:
         u = {"first_name":"Test1", "last_name": "Test1", "image_url":"https://upload.wikimedia.org/wikipedia/commons/e/e9/Felis_silvestris_silvestris_small_gradual_decrease_of_quality.png"}
         Posts.query.delete()
         res = self.client.post(f"/users/{self.user_id}/delete", data=u, follow_redirects=True)
         html = res.get_data(as_text = True)

         self.assertEqual(res.status_code, 200)
         self.assertNotIn('Test1', html)

    def test_editing_user(self):
        """Testing Editing a user"""
        with self.client:
         u = {"first_name":"Test3", "last_name": "Test3", "image_url":"https://upload.wikimedia.org/wikipedia/commons/e/e9/Felis_silvestris_silvestris_small_gradual_decrease_of_quality.png"}
         res = self.client.post(f"/users/{self.user_id}/edit", data=u, follow_redirects=True)
         html = res.get_data(as_text = True)

         self.assertEqual(res.status_code, 200)
         self.assertNotIn('Test1', html)
         self.assertIn('Test3', html)
    
    def test_post_showing(self):
        """Test to see if the postings show up on a users page"""
        with self.client:
            resp = self.client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text = True)
            self.assertIn("SPIDER-MAN!", html)
    
    def test_add_new_post(self):
        """Testing the add a new post functionality"""
        with self.client:
            post = {"title":"BATMAN!", "content":"IS HE BRUCE WAYNE!?", "user_id":self.user_id}
            resp = self.client.post(f"/users/{self.user_id}/posts/new", data=post, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn("BATMAN!", html)

    def test_view_post(self):
        """Viewing an post itself """
        with self.client:
              post = Posts.query.get(self.post_id)
              res =self.client.get(f"/posts/{post.id}")
              html = res.get_data(as_text=True)
              self.assertIn("<p><i>By Test1 Test1</i></p>", html)

    
    def test_delete_post(self):
        """Testing the ability to delete a post"""
        with self.client:
            post = Posts.query.get(self.post_id)
            p = {"title":post.title, "content":post.content, "user_id":self.user_id}
            res = self.client.post(f"/posts/{post.id}/delete", data= p, follow_redirects = True)
            html = res.get_data(as_text=True)
            self.assertNotIn("SPIDER-MAN",html)

    
    def test_post_edit(self):
        """Testing the ability to edit a post"""
        with self.client:
            post = Posts.query.get(self.post_id)
            p ={"title":"GREEN GOBLIN STRIKES!", "content":"HA HA HA I'VE TAKEN OVER SPIDEY", "user_id":self.user_id}
            res = self.client.post(f"/posts/{post.id}/edit", data = p, follow_redirects = True)
            html = res.get_data(as_text = True)

            self.assertNotIn("SPIDER-MAN", html)
            self.assertIn("GREEN GOBLIN STRIKES!", html)



   
        

