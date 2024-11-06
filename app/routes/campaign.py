from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models.campaign import Campaign, ScheduledCall, KnowledgeBase, Agent , CampaignAgent
from ..database import db
from ..forms import CampaignForm

campaign_bp = Blueprint('campaigns', __name__)

@campaign_bp.route('/manage_campaigns', methods=['GET'])
@login_required
def manage_campaigns():
    campaigns = Campaign.query.all()
    delete_form = CampaignForm()  # Create an instance of the CampaignForm for CSRF token
    return render_template('manage_campaigns.html', campaigns=campaigns, form=delete_form)


@campaign_bp.route('/create_campaign', methods=['GET', 'POST'])
@login_required
def create_campaign():
    form = CampaignForm()  # Create an instance of CampaignForm
    if form.validate_on_submit():
        # Create the campaign
        new_campaign = Campaign(
            campaign_name=form.campaign_name.data,
            user_id=current_user.user_id,
            greeting=form.greeting.data,
            prompt=form.prompt.data,
            call_numbers=form.call_numbers.data,
            routing_group=form.routing_group.data,
            campaign_type=form.campaign_type.data
        )
        db.session.add(new_campaign)
        db.session.commit()  # Commit to get the campaign ID

        # Add Knowledge Base Entries
        for kb_data in form.knowledge_bases.data:
            knowledge_base = KnowledgeBase(
                campaign_id=new_campaign.campaign_id,
                faq_entries=kb_data['faq_entries'],
                data_source=kb_data['data_source'],
                knowledge_base=kb_data['knowledge_base']
            )
            db.session.add(knowledge_base)

        # Add Agents and Campaign Agents
        for agent_data in form.agents.data:
            # Create the Agent entry
            agent = Agent(
                agent_name=agent_data['agent_name'],
                role=agent_data['role'],
                campaign_id=new_campaign.campaign_id 
            )
            db.session.add(agent)
            db.session.commit()  # Commit to get the agent ID
            
            # Now create the CampaignAgent entry
            campaign_agent = CampaignAgent(
                campaign_id=new_campaign.campaign_id,
                agent_id=agent.agent_id,  # Use the newly created agent ID
                phone_number=form.campaign_agents[0].phone_number.data  # Get the phone number from the form
            )
            db.session.add(campaign_agent)

        # Only create Scheduled Calls if the campaign type is outbound
        if new_campaign.campaign_type == 'outbound':
            if not form.scheduled_calls.data or all(
                not call['date_from'] and not call['time_from'] and not call['date_to'] and not call['time_to']
                for call in form.scheduled_calls.data):
                form.scheduled_calls.errors.append("At least one scheduled call must be provided.")
                return render_template('create_campaign.html', form=form)
            
            for call_data in form.scheduled_calls.data:
                scheduled_call = ScheduledCall(
                    campaign_id=new_campaign.campaign_id,
                    date_from=call_data['date_from'],  # Keep date_from separate
                    time_from=call_data['time_from'],  # Time field
                    date_to=call_data['date_to'],      # Keep date_to separate
                    time_to=call_data['time_to'],      # Time field
                    status='scheduled'  # Set default status as 'scheduled'
                )
                db.session.add(scheduled_call)

        db.session.commit()  # Commit all changes
        flash('Campaign created successfully!', 'success')
        return redirect(url_for('campaigns.manage_campaigns'))

    return render_template('create_campaign.html', form=form)

@campaign_bp.route('/edit_campaign/<int:campaign_id>', methods=['GET', 'POST'])
@login_required
def edit_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    form = CampaignForm(obj=campaign)  # Prepopulate the form with existing campaign data

    if form.validate_on_submit():
        # Update campaign details
        campaign.campaign_name = form.campaign_name.data
        campaign.greeting = form.greeting.data
        campaign.prompt = form.prompt.data
        campaign.call_numbers = form.call_numbers.data
        campaign.routing_group = form.routing_group.data
        campaign.campaign_type = form.campaign_type.data
        
        # Clear existing knowledge base entries and re-add them
        KnowledgeBase.query.filter_by(campaign_id=campaign_id).delete()
        for kb_data in form.knowledge_bases.data:
            knowledge_base = KnowledgeBase(
                campaign_id=campaign_id,
                faq_entries=kb_data['faq_entries'],
                data_source=kb_data['data_source'],
                knowledge_base=kb_data['knowledge_base']
            )
            db.session.add(knowledge_base)

        # Clear existing agents and re-add them
        Agent.query.filter_by(campaign_id=campaign_id).delete()
        for agent_data in form.agents.data:
            agent = Agent(
                agent_name=agent_data['agent_name'],
                role=agent_data['role'],
                campaign_id=campaign_id
            )
            db.session.add(agent)

        # Clear existing scheduled calls and re-add them
        ScheduledCall.query.filter_by(campaign_id=campaign_id).delete()
        if campaign.campaign_type == 'outbound':
            for call_data in form.scheduled_calls.data:
                scheduled_call = ScheduledCall(
                    campaign_id=campaign_id,
                    date_from=call_data['date_from'],
                    time_from=call_data['time_from'],
                    date_to=call_data['date_to'],
                    time_to=call_data['time_to'],
                    status='scheduled'
                )
                db.session.add(scheduled_call)

        db.session.commit()  # Commit updates to the campaign
        flash('Campaign updated successfully!', 'success')
        return redirect(url_for('campaigns.manage_campaigns'))

    return render_template('edit_campaign.html', form=form, campaign=campaign)
@campaign_bp.route('/delete_campaign/<int:campaign_id>', methods=['POST'])
@login_required
def delete_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)

    # Delete related data such as scheduled calls, knowledge bases, and campaign agents
    CampaignAgent.query.filter_by(campaign_id=campaign_id).delete()  # Delete campaign agents
    ScheduledCall.query.filter_by(campaign_id=campaign_id).delete()  # Delete scheduled calls
    KnowledgeBase.query.filter_by(campaign_id=campaign_id).delete()  # Delete knowledge bases
    
    db.session.delete(campaign)  # Finally, delete the campaign
    db.session.commit()
    flash('Campaign deleted successfully!', 'success')
    return redirect(url_for('campaigns.manage_campaigns'))


@campaign_bp.route('/view_campaign/<int:campaign_id>', methods=['GET'])
@login_required
def view_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    scheduled_calls = ScheduledCall.query.filter_by(campaign_id=campaign_id).all()
    knowledge_bases = KnowledgeBase.query.filter_by(campaign_id=campaign_id).all()
    agents = Agent.query.filter_by(campaign_id=campaign_id).all()

    return render_template('view_campaign.html', campaign=campaign, scheduled_calls=scheduled_calls, knowledge_bases=knowledge_bases, agents=agents)
