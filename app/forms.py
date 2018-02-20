from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    origin = StringField('Username', validators=[DataRequired()])
    destination = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Find My Playlist!')
