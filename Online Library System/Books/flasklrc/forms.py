from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flasklrc.models import Students, Books

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    gnumber = StringField('Gnumber',
                            validators=[DataRequired(), Length(min=9, max=9)])
    name = StringField('Name',
                            validators=[DataRequired(), Length(min=2, max=60)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_password', 
                            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        student = Students.query.filter_by(email=email.data).first()
        if student:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_gnumber(self, gnumber):
        student = Students.query.filter_by(gnumber=gnumber.data).first()
        if student:
            raise ValidationError('That username is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    gnumber = StringField('Gnumber',
                            validators=[DataRequired(), Length(min=9, max=9)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    gnumber = StringField('Gnumber',
                            validators=[DataRequired(), Length(min=9, max=9)])
    name = StringField('Name',
                            validators=[DataRequired(), Length(min=2, max=60)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            student = Students.query.filter_by(email=email.data).first()
            if student:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_gnumber(self, gnumber):
        if gnumber.data != current_user.gnumber:
            student = Students.query.filter_by(gnumber=gnumber.data).first()
            if student:
                raise ValidationError('That username is taken. Please choose a different one.')

class AddBooksForm(FlaskForm):
    ISBN = StringField('ISBN', validators=[DataRequired()])
    publisher = StringField('Publisher', validators=[DataRequired(), Length(min=5, max=120)])
    name = StringField('Name', validators=[DataRequired(), Length(min=5, max=120)])
    author = StringField('Author', validators=[DataRequired(), Length(min=5, max=120)])
    level = StringField('Level', validators=[DataRequired()])
    submit = SubmitField('Add')

class Check_in(FlaskForm):
    gnumber = StringField('Gnumber', validators=[DataRequired(), Length(min=9, max=9)])
    ISBN = StringField('ISBN', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_gnumber(self, gnumber):
        student = Students.query.filter_by(gnumber=gnumber.data).first()
        if not student:
            raise ValidationError('Gnumber Incorrect/User is not Registered')

    def validate_ISBN(self, ISBN):
        book = Books.query.filter_by(ISBN=ISBN.data).first()
        if not book:
            raise ValidationError('ISBN is incorrect.')


class Check_out(FlaskForm):
    gnumber = StringField('Gnumber', validators=[DataRequired(), Length(min=9, max=9)])
    ISBN = StringField('ISBN', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_gnumber(self, gnumber):
        student = Students.query.filter_by(gnumber=gnumber.data).first()
        if not student:
            raise ValidationError('Gnumber Incorrect/User is not Registered')

    def validate_ISBN(self, ISBN):
        book = Books.query.filter_by(ISBN=ISBN.data).first()
        if not book:
            raise ValidationError('ISBN is incorrect.')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        stud = Students.query.filter_by(email=email.data).first()
        if stud is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class ChangePasswordForm(FlaskForm):
    gnumber = StringField('Gnumber', validators=[DataRequired(), Length(min=9, max=9)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')