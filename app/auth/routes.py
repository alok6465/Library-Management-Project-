from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.extensions import db
from app.auth import bp
from app.auth.forms import LoginForm, ProfileForm, RegisterForm
from app.models import User

@bp.route('/login')
def login():
    return redirect(url_for('auth.student_login'))

@bp.route('/student-login', methods=['GET', 'POST'])
def student_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        print(f"Form submitted with PRN: {form.prn_number.data}")
        user = User.query.filter_by(prn_number=form.prn_number.data).first()
        print(f"User found: {user}")
        if user and user.check_password(form.password.data):
            print(f"Password correct, user role: {user.role}")
            if user.role != 'student':
                flash('This is Student Login. Please use Admin Login for admin access.', 'warning')
                return render_template('auth/student_login.html', title='Student Login', form=form)
            login_user(user)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        print("Invalid credentials")
        flash('Invalid PRN number or password', 'danger')
    else:
        print(f"Form validation failed: {form.errors}")
    
    return render_template('auth/student_login.html', title='Student Login', form=form)

@bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(prn_number=form.prn_number.data).first()
        if user and user.check_password(form.password.data):
            if user.role != 'admin':
                flash('This is Admin Login. Please use Student Login for student access.', 'warning')
                return render_template('auth/admin_login.html', title='Admin Login', form=form)
            login_user(user)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        flash('Invalid PRN number or password', 'danger')
    
    return render_template('auth/admin_login.html', title='Admin Login', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(prn_number=form.prn_number.data).first():
            flash('PRN number already exists', 'danger')
            return render_template('auth/register.html', title='Register', form=form)
        
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists', 'danger')
            return render_template('auth/register.html', title='Register', form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'danger')
            return render_template('auth/register.html', title='Register', form=form)
        
        user = User(
            prn_number=form.prn_number.data,
            username=form.username.data, 
            name=form.name.data,
            email=form.email.data, 
            mother_name=form.mother_name.data,
            dob=form.dob.data,
            phone=form.phone.data,
            address=form.address.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    
    return render_template('auth/profile.html', title='Profile', form=form)