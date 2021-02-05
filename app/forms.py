from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from flask_uploads import IMAGES
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, InputRequired
from app.models import User, Categs


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class PostForm(FlaskForm):
    post = TextAreaField('Go Fun The World!', validators=[DataRequired(), Length(min=1, max=140)])
    image = FileField('Choose Your Meme', validators=[
        FileRequired(),
        FileAllowed(IMAGES, 'Images only!')
    ])
    category = SelectField('Categories', choices=[(c.id, c.name) for c in Categs.query.order_by('name')], coerce=int,
                           validators=[InputRequired()])
    submit = SubmitField('Submit')
