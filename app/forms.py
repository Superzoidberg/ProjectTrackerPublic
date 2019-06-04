from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, DataRequired, Email, EqualTo
from wtforms.widgets import TextArea
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username)	:
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address')


class NewProjectForm(FlaskForm):
	company = StringField('Company', validators=[DataRequired()])
	requester = StringField('Requester', validators=[DataRequired()])
	department = StringField('Department', validators=[DataRequired()])
	status = StringField('Status')
	priority = StringField("Developer's Priority")
	priority_dept = StringField("Department's Priority")
	ticket = StringField('Ticket')
	hours = StringField('Hours')
	description = StringField('Description', validators=[DataRequired()])
	submit = SubmitField('Add')


class EditProjectForm(FlaskForm):
	company = StringField('Company', validators=[DataRequired()])
	requester = StringField('Requester', validators=[DataRequired()])
	description = StringField(
	    'Description', widget=TextArea(), validators=[DataRequired()])
	department = StringField('Department', validators=[DataRequired()])
	status = StringField('Status')
	priority = StringField("Developer's Priority")
	priority_dept = StringField("Department's Priority")
	ticket = StringField('Ticket')
	hours = StringField('Hours')
	comment = StringField('Add Comment', widget = TextArea())
	submit = SubmitField('Update')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

