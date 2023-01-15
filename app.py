"""Blogly application."""

"""
Author: Mahad Osman
Date: Jan 11th 2023
Assignment Blogly part 2
"""

from crypt import methods
from operator import methodcaller
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy 
from models import db, connect_db, Users, Posts, PostTag, Tag
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


app.config['SECRET_KEY'] = "secert123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)



connect_db(app)
# db.drop_all()
# db.create_all()

@app.route('/')
def show_users():
    """The root path which will list all users"""
    all_users = Users.query.all()
    # print('*********************')
    # print(all_users)
    # print('*********************')
    # return f"<h1> Weclome to our workking server {all_users}</h1>"
    return render_template('list.html', all_users = all_users)

@app.route('/users/new')
def new_user_form():
    """Returns a form to create a new user"""
    return render_template('new_userform.html')


@app.route('/users/new', methods=["POST"])
def add_new_user():
    """Submits the new user to the database"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    # file_name = secure_filename(image_url.filename)

    new_user = Users(first_name= first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/')

@app.route('/users/<int:user_id>')
def user_profile(user_id):
    """Creates the users unique profile"""
    user = Users.query.get_or_404(user_id)
    #posts = Posts.query.get(user_id)
    posts = Posts.query.filter_by(user_id = user_id).all()
    return render_template('user_profile.html', user = user, posts = posts)


@app.route('/users/<int:user_id>/edit')
def edit_user_profile(user_id):
    """The edit form for a user's profile"""
    user = Users.query.get_or_404(user_id)
    return render_template('edit_user.html', user= user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def submit_edit(user_id):
    """Handles submitting the edit change to our db"""
    user = Users.query.get(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()
    return redirect (f'/users/{user_id}')



@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deletes a user from the database and page."""
    Users.query.filter_by(id = user_id).delete()
    db.session.commit()
    flash(f"Users {user_id} was deleted")
    return redirect (f'/')


"""Post routes"""
@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """New post form"""
    user = Users.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('new_post.html', user = user, tags = tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_new_post(user_id):
    """Handles the submisson of a new post to our db"""
    user = Users.query.get_or_404(user_id)
    title = request.form["title"]
    content = request.form["content"]
    tags = request.form.getlist("tags")

    
    p = Posts(title =title, content =content, user_id=user.id)
    db.session.add(p)
    db.session.commit()

    print('*************************')
    for tag in tags: 
        t = Tag.query.filter(Tag.name == tag).one()
        pt = PostTag(post_id =p.id, tag_id = t.id)
        db.session.add(pt)
        db.session.commit()
        print(t.id)    
    print('*************************')
    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def post_view(post_id):
    """The post view which a user can click to edit or delete"""
    post = Posts.query.get_or_404(post_id)
    
    tags = post.tags # So our tags can be added to our post page
    return render_template("post_view.html", post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit')
def edit_view(post_id):
    """Populates an edit form for the selected post"""
    post = Posts.query.get_or_404(post_id)
    
    tags = Tag.query.all()

    """Also retrieve the related tags"""
    posttags = post.tags
    ''''''
    print('************************')
    for pt in posttags:
        print(pt.name)
    for tag in tags:
        print(tag.name)
    print('************************')

    ''''''
    return render_template("edit_post.html", post = post, tags = tags, posttags=posttags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Handles the submission of an edit for a post"""
    post = Posts.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form['content']
    db.session.add(post)
    db.session.commit()
    return redirect (f"/users/{post.user.id}")




@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Handles the deletion of a users post in our db and front end."""
    post = Posts.query.get_or_404(post_id)
    print("******************************")
    print(post.user.id)
    print("******************************")
    Posts.query.filter_by(id = post_id).delete()    
    db.session.commit()
    return redirect(f"/users/{post.user.id}")


'''Adding the tag routes to our project'''
@app.route('/tags')
def show_tag_list():
    '''Shows a list of our tags'''
    tags = Tag.query.all()
    return render_template('tag_list.html', tags = tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Shows a tags page and the assocaited posts"""
    tag = Tag.query.get(tag_id)
    posts = tag.posts
    return render_template('tag_view.html', tag = tag, posts = posts)

@app.route('/tags/new')
def create_new_tag():
    """Create a new Tag"""
    return render_template('new_tag.html')

@app.route('/tags/new', methods=["POST"])
def submitting_new_tag():
    """Submitting A new tag to the database"""
    name = request.form["tagname"]
    t = Tag(name=name)
    db.session.add(t)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_view(tag_id):
    """Editing an existing tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit_tag.html", tag = tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag_submit(tag_id):
    """Editing an existing tag"""
    name = request.form["tagname"]
    tag = Tag.query.get_or_404(tag_id)
    tag.name = name 

    db.session.add(tag)
    db.session.commit()
    return redirect(f"/tags/{tag.id}")

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Deleting an existing tag"""
    'First need to remove all posttags that are associated'
    PostTag.query.filter_by(tag_id = tag_id).delete()
    Tag.query.filter_by(id = tag_id).delete()
    db.session.commit()
    return redirect("/tags")



