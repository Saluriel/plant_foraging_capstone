from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, HiddenField
from wtforms.validators import Email, Length, InputRequired

class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[InputRequired()])
    email = StringField('E-mail')
    password = PasswordField('Password (min. 6 characters)', validators=[Length(min=6)])
    location = StringField('(Optional) Location')

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class EditUserForm(FlaskForm):
    """Form for editing the current user"""

    username = StringField("New Username")
    email = StringField("New Email Address")
    location = StringField("New Location")
    password = PasswordField("Current Password", validators=[InputRequired()])

