from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from blog.models import User


class Reg(FlaskForm):
	username = StringField(label='Username', validators = [Length(min=2, max=30), DataRequired()])
	email = StringField(label='Email Id', validators = [Email(), DataRequired()])
	password = PasswordField(label='Password', validators = [Length(min=8), DataRequired()])
	confirm_password = PasswordField(label='Confirm Password', validators = [EqualTo('password'), DataRequired()])
	submit = SubmitField(label='Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username already exists!')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email already exists!')

class Login(FlaskForm):
	email = StringField(label='Email Id', validators = [Email(), DataRequired()])
	password = PasswordField(label='Password', validators = [DataRequired()])
	remember = BooleanField(label='Remember Me')
	submit = SubmitField(label='Log In')

class Update(FlaskForm):
	username = StringField(label='Username', validators = [Length(min=2, max=30), DataRequired()])
	email = StringField(label='Email Id', validators = [Email(), DataRequired()])
	picture = FileField(label='Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png '])])
	submit = SubmitField(label='Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username already exists!')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Email already exists!')


