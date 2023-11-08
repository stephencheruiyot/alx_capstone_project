# Import necessary modules and classes
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like  # Import models from your application
from . import db  # Import the database instance

# Create a Blueprint for this set of views
views = Blueprint("views", __name__)

# Route for the home page
@views.route("/")
@views.route("/home")
@login_required  # Ensure the user is logged in to access this page
def home():
    # Query all posts from the database
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)

# Route for creating a new post
@views.route("/create-post", methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in to create a post
def create_post():
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            # Create a new post and add it to the database
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_post.html', user=current_user)

# Route for deleting a post
@views.route("/delete-post/<id>")
@login_required  # Ensure the user is logged in to delete a post
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.id:
        flash('You do not have permission to delete this post.', category='error')
    else:
        # Delete the post from the database
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.home'))

# Route for viewing posts by a specific user
@views.route("/posts/<username>")
@login_required  # Ensure the user is logged in to view posts
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=username)

# Route for creating a comment on a post
@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required  # Ensure the user is logged in to create a comment
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            # Create a new comment and add it to the database
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.home'))

# Route for deleting a comment
@views.route("/delete-comment/<comment_id>")
@login_required  # Ensure the user is logged in to delete a comment
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        # Delete the comment from the database
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))

# Route for liking/unliking a post
@views.route("/like-post/<post_id>", methods=['POST'])
@login_required  # Ensure the user is logged in to like/unlike a post
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        # User already liked the post, so unlike it
        db.session.delete(like)
        db.session.commit()
    else:
        # User is liking the post
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    # Return JSON response with the number of likes and whether the user has liked the post
    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})

# Route for changing the user's password
@views.route('/change_password', methods=['GET'])
@login_required
def change_password():
    user = current_user
    return render_template('change_password.html',user=user)
