from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Create a Flask Blueprint for authentication-related routes
auth = Blueprint("auth", __name__)

# User login route
@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if the user exists in the database
        user = User.query.filter_by(email=email).first()
        if user:
            # If the user exists, verify the provided password
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)  # Log the user in
                return redirect(url_for('views.home'))  # Redirect to the home page
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

# User registration route
@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # Check if email and username already exist in the database
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif password1 != password2:
            flash('Password don\'t match!', category='error')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        elif len(password1) < 6:
            flash('Password is too short.', category='error')
        elif len(email) < 4:
            flash("Email is invalid.", category='error')
        else:
            # Create a new user in the database with a hashed password
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)  # Log the new user in
            flash('User created!')
            return redirect(url_for('views.home'))  # Redirect to the home page

    return render_template("signup.html", user=current_user)

# User logout route
@auth.route("/logout")
@login_required
def logout():
    logout_user()  # Log the user out
    return redirect(url_for("views.home"))  # Redirect to the home page

# Route to change the user's password
@auth.route('/change_password', methods=['POST'])
@login_required
def change_password_post():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    user = User.query.get(current_user.id)

    # Check if the current password matches the one in the database
    if not check_password_hash(user.password, current_password):
        flash('Current password is incorrect.', 'error')
        return redirect(url_for('auth.change_password'))

    # Check if the new password and confirmation password match
    if new_password != confirm_password:
        flash('New password and confirm password do not match.', 'error')
        return redirect(url_for('auth.change_password'))

    # Update the user's password with the new hashed password
    user.password = generate_password_hash(new_password)
    db.session.commit()

    flash('Password changed successfully.', 'success')
    return redirect(url_for('views.home'))
