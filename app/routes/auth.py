# from flask import Blueprint, render_template, redirect, url_for, flash
# from flask_login import login_user, logout_user, login_required, current_user
# from ..models.user import User
# from ..forms import LoginForm, SignupForm
# from ..database import db, bcrypt
# from datetime import datetime  # Import datetime

# auth_bp = Blueprint('auth', __name__)

# @auth_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('users.dashboard'))

#     form = LoginForm()
#     if form.validate_on_submit():
#         print(f"Email entered: {form.email.data.strip()}")  # Debugging line
#         user = User.query.filter_by(email=form.email.data.strip()).first()
#         if user:
#             print(f"User found: {user.email}, Role: {user.role}")  # Debugging line
#             if bcrypt.check_password_hash(user.password, form.password.data):
#                 if user.is_active:  # Check if the user account is active
#                     login_user(user)
#                     user.last_login = datetime.utcnow()  # Set last login time
#                     db.session.commit()  # Commit the change to the database
#                     flash('Login successful!', 'success')
#                     if user.role == 'Super Admin':
#                         return redirect(url_for('users.manage_users'))
#                     else:
#                         return redirect(url_for('users.dashboard'))
#                 else:
#                     print("User account is inactive.")
#                     flash('Your account is inactive. Please contact support.', 'danger')
#             else:
#                 print("Password mismatch.")
#                 flash('Login Unsuccessful. Please check email and password', 'danger')
#         else:
#             print("No user found with this email.")
#             flash('Login Unsuccessful. Please check email and password', 'danger')
#     return render_template('login.html', form=form)

# @auth_bp.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if current_user.is_authenticated:  # Redirect if the user is already logged in
#         return redirect(url_for('users.dashboard'))

#     form = SignupForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         new_user = User(
#             email=form.email.data,
#             password=hashed_password,
#             role='Super Admin',  # Default role for new users
#             business_name=form.business_name.data,
#             address=form.address.data,
#             city=form.city.data,
#             phone_number=form.phone_number.data,
#             is_active=True  # Set account to active upon signup
#         )
#         db.session.add(new_user)
#         db.session.commit()
#         flash('Your account has been created! You can now log in', 'success')
#         return redirect(url_for('auth.login'))
#     return render_template('signup.html', form=form)

# @auth_bp.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash('You have been logged out.', 'info')  # Feedback message for logout
#     return redirect(url_for('auth.login'))


from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..models.user import User
from ..forms import LoginForm, SignupForm
from ..database import db, bcrypt
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip()).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            if user.is_active:
                login_user(user)
                user.last_login = datetime.utcnow()
                db.session.commit()
                flash('Login successful!', 'success')
                return redirect(url_for('users.dashboard'))
            else:
                flash('Your account is inactive. Please contact support.', 'danger')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))

    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(
            email=form.email.data,
            password_hash=hashed_password,
            role='Super Admin',  # Default role for new users
            business_name=form.business_name.data,
            address=form.address.data,
            city=form.city.data,
            phone_number=form.phone_number.data,
            is_active=True
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
