from flask_sqlalchemy import SQLAlchemy 
from models import db, connect_db, Users, Posts, Tag, PostTag
from app import app

"""
Author: Mahad Osman
Date: Jan 11th 2023
Assignment Blogly part 2
"""

#Create all tables 
db.drop_all()
db.create_all()


#
u1 = Users(first_name= "Mahad", last_name = "Osman", image_url = "https://images.unsplash.com/photo-1661956602868-6ae368943878?ixlib=rb-4.0.3&ixid=MnwxMjA3fDF8MHxlZGl0b3JpYWwtZmVlZHw3MXx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=60")
u2 = Users(first_name= "Hadi", last_name = "Makki", image_url = "https://plus.unsplash.com/premium_photo-1663054425353-d181e7ea137f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxlZGl0b3JpYWwtZmVlZHw0OXx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=60")
u3 = Users(first_name= "Emily", last_name = "Lefebvre", image_url ="https://images.unsplash.com/photo-1673268724551-60203522ccea?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxlZGl0b3JpYWwtZmVlZHw0N3x8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=60")


#posts
p1 = Posts(title ="bwah bwah", content = "its me your pal yoshi", user_id="2")
p2 = Posts(title ="Zote!", content = "SAVE HIM?!", user_id="3")
p3 = Posts(title ="The Nail Master", content = "Give hime eternal peace", user_id="3")
p4 = Posts(title ="SpiderMan Is A MENACE!", content = "JJJ Bringing you the news", user_id="1")
p5 = Posts(title ="BlackSuited Spidey", content = "Is he really venom?!", user_id="1")



#Tags
t1 = Tag(name = "funny")
t2 = Tag(name = "Zote")
t3 = Tag(name = "Superhero")
t4 = Tag(name = "Videogame")


#PostTag
pt1 = PostTag(post_id=1, tag_id=1)
pt2 = PostTag(post_id=2, tag_id=1)
pt3 = PostTag(post_id=2, tag_id=2)
pt4 = PostTag(post_id=4, tag_id=3)





#Users
db.session.add_all([u1,u2,u3])
db.session.commit()

#Posts
db.session.add_all([p1,p2,p3,p4,p5])
db.session.commit()


#Tags
db.session.add_all([t1,t2,t3,t4])
db.session.commit()

#PostTags
db.session.add_all([pt1,pt2,pt3,pt4])
db.session.commit()



