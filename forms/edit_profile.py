from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class EditProfileForm(FlaskForm):
    username = StringField('Użytkownik', validators=[DataRequired()])
    about_me = TextAreaField('Nota', validators=[Length(min=0, max=320)])
    submit = SubmitField('Zapisz')
