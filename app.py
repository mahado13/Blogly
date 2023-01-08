"""Blogly application."""

"""
Author: Mahad Osman
Date: Jan 8th 2023
Assignment Blogly part 1
"""

from crypt import methods
from operator import methodcaller
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy 
from models import db, connect_db, Users
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
    all_users = Users.query.all()
    # print('*********************')
    # print(all_users)
    # print('*********************')
    # return f"<h1> Weclome to our workking server {all_users}</h1>"
    return render_template('list.html', all_users = all_users)

@app.route('/users/new')
def new_user_form():
    return render_template('new_userform.html')


@app.route('/users/new', methods=["POST"])
def add_new_user():
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
    user = Users.query.get_or_404(user_id)
    return render_template('user_profile.html', user = user)


@app.route('/users/<int:user_id>/edit')
def edit_user_profile(user_id):
    user = Users.query.get_or_404(user_id)
    return render_template('edit_user.html', user= user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def submit_edit(user_id):
    user = Users.query.get(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()
    return redirect (f'/users/{user_id}')



@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    Users.query.filter_by(id = user_id).delete()
    db.session.commit()
    flash(f"Users {user_id} was deleted")
    return redirect (f'/')



