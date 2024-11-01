from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField , TextAreaField , BooleanField
from wtforms.validators import DataRequired, Email

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


class CampaignForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    assigned_phone_numbers = TextAreaField('Assigned Phone Numbers (JSON format)', validators=[DataRequired()])
    custom_faq = BooleanField('Custom FAQ')
    knowledge_base = TextAreaField('Knowledge Base')
    data_source_type = SelectField('Data Source Type', choices=[('API', 'API'), ('flat_file', 'Flat File'), ('database', 'Database')], validators=[DataRequired()])
    data_source_details = TextAreaField('Data Source Details')
    submit = SubmitField('Submit')