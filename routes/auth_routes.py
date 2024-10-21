import requests
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from forms import RegistrationForm, LoginForm
from models import User
from database import db

auth_bp = Blueprint('auth', __name__)

# Registration route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # if form.validate_on_submit():
    #     # Send POST request to the /auth/register route with the form data
    #     response = requests.post('http://localhost:5000/auth/register', json={
    #         'username': form.username.data,
    #         'password': form.password.data
    #     })
    #     if response.status_code == 201:
    #         flash('Registration successful! Please log in.', 'success')
    #         return redirect(url_for('auth.login'))
    #     else:
    #         flash('Registration failed.', 'danger')
    
    if form.validate_on_submit():
        username = form.username.data
        password = generate_password_hash(form.password.data)
        role = 'user'  # Default to user role

        user = User(username=username, password=password, role=role)
        db.session.add(user)
        db.session.commit()
        flash("User registered successfully!", "success")
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)

# Login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # if form.validate_on_submit():
        
    #     # Send POST request to the /auth/login route with the form data
    #     response = requests.post('http://localhost:5000/auth/login', json={
    #         'username': form.username.data,
    #         'password': form.password.data
    #     })
    #     if response.status_code == 200:
    #         flash('Login successful!', 'success')
    #         return redirect(url_for('auth.protected'))
    #     else:
    #         flash('Login failed. Check your username and password.', 'danger')
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity={'id': user.id, 'username': user.username, 'role': user.role})
            flash("Login successful!", "success")
            return redirect(url_for('auth.protected'))

        flash("Invalid credentials", "danger")
    
    return render_template('login.html', form=form)

# Protected route
@auth_bp.route('/protected', methods=['GET'])
@jwt_required()  # This requires JWT authentication
def protected():
    current_user = get_jwt_identity()
    return f"This is a protected page. Welcome, {current_user['username']}."
