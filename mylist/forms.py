from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from mylist.models import User,Entry
from flask_login import login_user, current_user, logout_user, login_required

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        #need to check if not same as the old one
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        #need to check if not same as the old one 
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class EntryAddForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=50)])
    picture = FileField('Image', validators=[FileAllowed(['jpg', 'png'])])
    submit1 = SubmitField('Add')

    def validate_title(self,title):
        duplitcate = Entry.query.filter_by(title = title.data).first()
        if duplitcate:
            raise ValidationError("The Entry already exits")

class EntryUpdateForm(FlaskForm):
    title = StringField('Title', validators=[])
    picture = FileField('Image', validators=[FileAllowed(['jpg', 'png'])])
    
    delete = SubmitField("Delete")
    submit2 = SubmitField('Update')

    def validate_title(self, title):
        if title.data != "":
            entry = Entry.query.filter_by(user = current_user).filter_by(title = title.data).first()
            if entry:
                raise ValidationError("This Entry is already there. Choose different one")
