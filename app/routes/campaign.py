from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models.campaign import Campaign
from ..models.user import User, Permission  # Import Permission here
from ..forms import CampaignForm  # Assume you have a CampaignForm defined
from ..database import db

campaign_bp = Blueprint('campaigns', __name__)

def is_super_admin():
    return current_user.role == 'Super Admin'

def has_permission(permission_name):
    # Check if the user has the specified permission based on their role
    user_role = current_user.role
    permission = Permission.query.filter_by(role=user_role).first()
    if permission and getattr(permission, permission_name, False):
        return True
    return False

@campaign_bp.route('/manage_campaigns', methods=['GET', 'POST'])
@login_required
def manage_campaigns():
    if not (is_super_admin() or has_permission('manage_campaigns')):
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('users.dashboard'))

    all_campaigns = Campaign.query.all()
    return render_template('manage_campaigns.html', campaigns=all_campaigns)

@campaign_bp.route('/add_campaign', methods=['GET', 'POST'])
@login_required
def add_campaign():
    if not (is_super_admin() or has_permission('manage_campaigns')):
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('users.dashboard'))

    form = CampaignForm()
    if form.validate_on_submit():
        new_campaign = Campaign(
            name=form.title.data,
            description=form.description.data,
            created_by=current_user.user_id,
            assigned_phone_numbers=form.assigned_phone_numbers.data,  # Assuming this field is in the form
            custom_faq=form.custom_faq.data,  # Assuming this field is in the form
            knowledge_base=form.knowledge_base.data,  # Assuming this field is in the form
            data_source_type=form.data_source_type.data,  # Assuming this field is in the form
            data_source_details=form.data_source_details.data,  # Assuming this field is in the form
            status='active'
        )
        db.session.add(new_campaign)
        db.session.commit()
        flash('Campaign has been added!', 'success')
        return redirect(url_for('campaigns.manage_campaigns'))

    return render_template('add_campaign.html', form=form)

@campaign_bp.route('/edit_campaign/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
def edit_campaign(campaign_id):
    if not (is_super_admin() or has_permission('manage_campaigns')):
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('users.dashboard'))

    campaign = Campaign.query.get_or_404(campaign_id)
    form = CampaignForm(obj=campaign)
    if form.validate_on_submit():
        campaign.name = form.title.data
        campaign.description = form.description.data
        campaign.assigned_phone_numbers = form.assigned_phone_numbers.data  # Update phone numbers
        campaign.custom_faq = form.custom_faq.data  # Update custom FAQ
        campaign.knowledge_base = form.knowledge_base.data  # Update knowledge base
        campaign.data_source_type = form.data_source_type.data  # Update data source type
        campaign.data_source_details = form.data_source_details.data  # Update data source details
        db.session.commit()
        flash('Campaign has been updated!', 'success')
        return redirect(url_for('campaigns.manage_campaigns'))

    return render_template('edit_campaign.html', form=form, campaign=campaign)

@campaign_bp.route('/delete_campaign/<int:campaign_id>', methods=['POST'])
@login_required
def delete_campaign(campaign_id):
    if not (is_super_admin() or has_permission('manage_campaigns')):
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('users.dashboard'))

    campaign = Campaign.query.get_or_404(campaign_id)
    db.session.delete(campaign)
    db.session.commit()
    flash('Campaign has been deleted!', 'success')
    return redirect(url_for('campaigns.manage_campaigns'))
