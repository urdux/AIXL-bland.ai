from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField , TextAreaField , BooleanField , FieldList, FormField , DateField, TimeField , DecimalField
from wtforms.validators import DataRequired, Email , Optional

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    business_name = StringField('Business Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class UserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('User', 'User'), ('Manager', 'Manager'), ('Editor', 'Editor')], validators=[DataRequired()])  # Exclude Super Admin
    business_name = StringField('Business Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Add User')

class ScheduledCallForm(FlaskForm):
    date_from = DateField('Date From', format='%Y-%m-%d', validators=[Optional()])
    time_from = TimeField('Time From', validators=[Optional()])
    date_to = DateField('Date To', format='%Y-%m-%d', validators=[Optional()])
    time_to = TimeField('Time To', validators=[Optional()])
    status = SelectField('Status', choices=[('scheduled', 'Scheduled')], default='scheduled', validators=[Optional()])

class AgentForm(FlaskForm):
    agent_name = StringField('Agent Name', validators=[DataRequired()])
    role = StringField('Role')

class CampaignAgentForm(FlaskForm):
    phone_number = StringField('Phone Number', validators=[DataRequired()])  # Phone number for the campaign agent

class KnowledgeBaseForm(FlaskForm):
    faq_entries = TextAreaField('FAQ Entries', validators=[DataRequired()])
    data_source = StringField('Data Source')
    knowledge_base = TextAreaField('Knowledge Base Content')
class CampaignForm(FlaskForm):
    campaign_name = StringField('Campaign Name', validators=[DataRequired()])
    greeting = TextAreaField('Greeting')
    prompt = TextAreaField('Prompt')
    call_numbers = TextAreaField('Call Numbers')
    routing_group = StringField('Routing Group')
    campaign_type = SelectField('Campaign Type', choices=[('inbound', 'Inbound'), ('outbound', 'Outbound')], validators=[DataRequired()])
    
    knowledge_bases = FieldList(FormField(KnowledgeBaseForm), min_entries=1)  # For multiple KB entries
    agents = FieldList(FormField(AgentForm), min_entries=1)  # For multiple agents
    campaign_agents = FieldList(FormField(CampaignAgentForm), min_entries=1)  # For campaign agent phone numbers
    scheduled_calls = FieldList(FormField(ScheduledCallForm), min_entries=1)  # Allow zero entries

    submit = SubmitField('Create Campaign')


class SubscriptionForm(FlaskForm):
    plan_name = StringField('Plan Name', validators=[DataRequired()])
    cost = DecimalField('Cost', validators=[DataRequired()])
    submit = SubmitField('Subscribe')


class WalletRechargeForm(FlaskForm):
    amount = DecimalField('Recharge Amount', validators=[DataRequired()])
    submit = SubmitField('Recharge Wallet')