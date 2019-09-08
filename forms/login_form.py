from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Użytkownik', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember_me = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')
