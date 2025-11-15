from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    prn_number = StringField('PRN Number', validators=[DataRequired()])
    password = PasswordField('Password (Mother Name + DOB)', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class ProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Profile')

class RegisterForm(FlaskForm):
    prn_number = StringField('PRN Number', validators=[DataRequired(), Length(min=8, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mother_name = StringField('Mother Name', validators=[DataRequired(), Length(min=2, max=100)])
    dob = StringField('Date of Birth (DDMMYYYY)', validators=[DataRequired(), Length(min=8, max=8)])
    phone = StringField('Phone Number', validators=[Length(max=15)])
    address = StringField('Address', validators=[Length(max=200)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('student', 'Student'), ('admin', 'Admin')], default='student')
    submit = SubmitField('Register')