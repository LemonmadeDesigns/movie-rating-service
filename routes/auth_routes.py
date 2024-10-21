from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
import requests
from forms import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Send POST request to the /auth/register route with the form data
        response = requests.post('http://localhost:5000/auth/register', json={
            'username': form.username.data,
            'password': form.password.data
        })
        if response.status_code == 201:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Registration failed.', 'danger')
    
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Send POST request to the /auth/login route with the form data
        response = requests.post('http://localhost:5000/auth/login', json={
            'username': form.username.data,
            'password': form.password.data
        })
        if response.status_code == 200:
            flash('Login successful!', 'success')
            return redirect(url_for('auth.protected'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    
    return render_template('login.html', form=form)

@auth_bp.route('/protected')
@jwt_required()  # This requires JWT authentication
def protected():
    current_user = get_jwt_identity()
    return f"This is a protected page. Welcome, {current_user['username']}."
