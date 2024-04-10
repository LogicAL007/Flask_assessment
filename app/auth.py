from flask import Blueprint, render_template, flash, redirect, Flask, request
from .models import Customer
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """
    Registers a new user with email, username, and password.

    Expects a JSON payload with 'email', 'username', 'password1', and 'password2'.
    Validates the input data, checks for existing users with the same email or username,
    and creates a new Customer if validation passes.

    Returns:
        JSON response with a success message or an error message with appropriate HTTP status codes.
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Missing data'}), 400

    email = data.get('email')
    username = data.get('username')
    password1 = data.get('password1')
    password2 = data.get('password2')

    if not all([email, username, password1, password2]):
        return jsonify({'error': 'All fields are required'}), 400

    if password1 != password2:
        return jsonify({'error': 'Passwords do not match'}), 400

    # Check if user already exists
    if Customer.query.filter_by(email=email).first() is not None:
        return jsonify({'error': 'Email already in use'}), 400
    if Customer.query.filter_by(username=username).first() is not None:
        return jsonify({'error': 'Username already taken'}), 400

    new_user = Customer(email=email, username=username, password_hash=generate_password_hash(password1))

    db.session.add(new_user)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({'error': 'Account creation failed'}), 500

    return jsonify({'message': 'Account created successfully'}), 201


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Authenticates a user based on email and password.

    Expects a JSON payload with 'email' and 'password'.
    Validates the input data, checks if the user exists and if the password is correct,
    and logs the user in if validation passes.

    Returns:
        JSON response with a success message or an error message with appropriate HTTP status codes.
    """   
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Missing data'}), 400

    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'error': 'Both email and password are required'}), 400

    user = Customer.query.filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        # Redirect isn't typically used in APIs; instead, return a success message or token
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401


@auth.route('/logout', methods=['GET', 'POST'])
# @login_required
def log_out():
    """
    Logs out the currently logged-in user.

    Ends the user's session and redirects to the home page.
    
    Returns:
        Redirection to the home page.
    """
    logout_user()
    return redirect('/')

@auth.route('/change-password/<int:customer_id>', methods=['GET', 'POST'])
# @login_required
def change_password(user_id):
    """
    Allows a logged-in user to change their password.

    Expects a URL parameter 'user_id' and a JSON payload with 'current_password', 
    'new_password', and 'confirm_new_password'.
    Validates the input data, checks if the current password is correct,
    and updates the user's password if validation passes.

    Parameters:
        user_id (int): The ID of the user attempting to change their password. Expected in the URL.

    Returns:
        JSON response with a success message or an error message with appropriate HTTP status codes.
    """
    # Ensure the current user is the one trying to change their password
    if current_user.id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()

    if not data:
        return jsonify({'error': 'Missing data'}), 400

    current_password = data.get('current_password')
    new_password = data.get('new_password')
    confirm_new_password = data.get('confirm_new_password')

    if not all([current_password, new_password, confirm_new_password]):
        return jsonify({'error': 'All fields are required'}), 400

    if new_password != confirm_new_password:
        return jsonify({'error': 'New passwords do not match'}), 400

    user = Customer.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if check_password_hash(user.password_hash, current_password):
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({'message': 'Password updated successfully'}), 200
    else:
        return jsonify({'error': 'Current password is incorrect'}), 401

