from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models.user import User, Permission , UserPermission
from ..forms import UserForm
from ..database import db, bcrypt

users_bp = Blueprint('users', __name__)

def is_super_admin():
    return current_user.role == 'Super Admin'




def has_permission(permission_name):
    # Fetch the user's role
    user_role = current_user.role
    print(f"User ID: {current_user.user_id}, Role: {user_role}")  # Debugging line
    
    # Fetch the permissions associated with the user's role
    permission = Permission.query.filter_by(role=user_role).first()
    
    if permission:
        # Debug output for all permissions associated with the role
        print(f"Permissions for role '{user_role}':")
        print(f"Manage Users: {permission.manage_users}")
        print(f"Manage Sub Admins: {permission.manage_sub_admins}")
        print(f"Create Campaign: {permission.create_campaign}")
        print(f"Manage Calls: {permission.manage_calls}")
        print(f"View Call Logs: {permission.view_call_logs}")
        print(f"Manage Integrations: {permission.manage_integrations}")
        print(f"Manage Subscriptions: {permission.manage_subscriptions}")
        print(f"Manage Reports: {permission.manage_reports}")

        # Check if the specific permission is granted
        if getattr(permission, permission_name, False):
            return True

    print(f"No permission found for {permission_name} for User ID: {current_user.user_id}")  # Debugging line
    return False



@users_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@users_bp.route('/manage_users', methods=['GET', 'POST'])
@login_required
def manage_users():
    if not (is_super_admin() or has_permission('manage_users')):
        flash('You do not have permission to access this page.', 'danger')
        print(f"Access denied for User ID: {current_user.user_id}")  # Debugging line
        return redirect(url_for('users.dashboard'))

    all_users = User.query.all()
    form = UserForm()  # Instantiate UserForm here
    print(f"User ID: {current_user.user_id} has access to manage users.")  # Debugging line
    return render_template('users.html', users=all_users, form=form)

@users_bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if not (is_super_admin() or has_permission('manage_users')):
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('users.dashboard'))

    form = UserForm()
    if form.validate_on_submit():
        new_user = User(
            email=form.email.data,
            password_hash=bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
            business_name=form.business_name.data,
            address=form.address.data,
            city=form.city.data,
            phone_number=form.phone_number.data,
            is_active=True
        )
        db.session.add(new_user)
        db.session.commit()
        flash('User has been added!', 'success')
        return redirect(url_for('users.manage_users'))

    return render_template('add_user.html', form=form)

@users_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not (is_super_admin() or has_permission('manage_users')):
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('users.dashboard'))

    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.business_name = form.business_name.data
        user.address = form.address.data
        user.city = form.city.data
        user.phone_number = form.phone_number.data
        db.session.commit()
        flash('User has been updated!', 'success')
        return redirect(url_for('users.manage_users'))

    return render_template('edit_user.html', form=form, user=user)

@users_bp.route('/delete_user/<int:user_id>', methods=['POST'])  # Changed to POST for safety
@login_required
def delete_user(user_id):
    if not (is_super_admin() or has_permission('manage_users')):
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('users.dashboard'))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted!', 'success')
    return redirect(url_for('users.manage_users'))

@users_bp.route('/activate_user/<int:user_id>', methods=['POST'])
@login_required
def activate_user(user_id):
    if not (is_super_admin() or has_permission('manage_users')):
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('users.dashboard'))

    user = User.query.get_or_404(user_id)
    user.is_active = True  # Set user as active
    db.session.commit()
    flash(f'User {user.email} has been activated.', 'success')
    return redirect(url_for('users.manage_users'))

@users_bp.route('/deactivate_user/<int:user_id>', methods=['POST'])
@login_required
def deactivate_user(user_id):
    if not (is_super_admin() or has_permission('manage_users')):
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('users.dashboard'))

    user = User.query.get_or_404(user_id)
    user.is_active = False  # Set user as inactive
    db.session.commit()
    flash(f'User {user.email} has been deactivated.', 'success')
    return redirect(url_for('users.manage_users'))
@users_bp.route('/manage_permissions', methods=['GET', 'POST'])
@login_required
def manage_permissions():
    if not is_super_admin():
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('users.dashboard'))

    permissions = Permission.query.all()
    roles = User.query.with_entities(User.role).distinct()  # Get distinct roles from the User model
    form = UserForm()  # Instantiate UserForm for CSRF token

    if request.method == 'POST':
        role = request.form.get('role')
        manage_users = request.form.get('manage_users') == 'on'
        # manage_campaign = request.form.get('manage_campaign') == 'on'  # Capture manage_campaign

        existing_permission = Permission.query.filter_by(role=role).first()

        if existing_permission:
            existing_permission.manage_users = manage_users
            # existing_permission.manage_campaign = manage_campaign  # Update manage_campaign
            db.session.commit()
            flash('Permissions updated successfully!', 'success')
        else:
            new_permission = Permission(role=role, manage_users=manage_users)
            db.session.add(new_permission)
            db.session.commit()
            flash('New permission added successfully!', 'success')

        return redirect(url_for('users.manage_permissions'))

    return render_template('manage_permissions.html', permissions=permissions, roles=roles, form=form)


@users_bp.route('/edit_permission/<int:permission_id>', methods=['GET', 'POST'])
@login_required
def edit_permission(permission_id):
    if not is_super_admin():
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('users.dashboard'))

    permission = Permission.query.get_or_404(permission_id)

    if request.method == 'POST':
        permission.role = request.form.get('role')
        permission.manage_users = request.form.get('manage_users') == 'on'
        # permission.manage_campaign = request.form.get('manage_campaign') == 'on'  # Update manage_campaign
        db.session.commit()
        flash('Permission updated successfully!', 'success')
        return redirect(url_for('users.manage_permissions'))

    return render_template('edit_permission.html', permission=permission)


@users_bp.route('/delete_permission/<int:permission_id>')
@login_required
def delete_permission(permission_id):
    if not is_super_admin():
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('users.dashboard'))

    permission = Permission.query.get_or_404(permission_id)
    db.session.delete(permission)
    db.session.commit()
    flash('Permission deleted successfully!', 'success')
    return redirect(url_for('users.manage_permissions'))
