from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Define the User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the User table
    email = db.Column(db.String(150), unique=True)  # User's email address
    username = db.Column(db.String(150), unique=True)  # User's username
    password = db.Column(db.String(150))  # Hashed password
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())  # User's registration date
    # Define relationships with other models: User has many Posts, Comments, and Likes
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)

# Define the Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the Post table
    text = db.Column(db.Text, nullable=False)  # Content of the post
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())  # Post creation date
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    # Define relationships with other models: Post has many Comments and Likes
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='post', passive_deletes=True)

# Define the Comment model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the Comment table
    text = db.Column(db.String(200), nullable=False)  # Content of the comment
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())  # Comment creation date
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)
    # Comments are associated with a User and a Post

# Define the Like model
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the Like table
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())  # Like creation date
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)
    # Likes are associated with a User and a Post
