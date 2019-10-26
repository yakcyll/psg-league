from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AddMatchForm(FlaskForm):
    black_player = StringField('Gracz czarny', validators=[DataRequired()])
    white_player = StringField('Gracz biały', validators=[DataRequired()])
    sgf_file = FileField('SGF', validators=[FileRequired(), FileAllowed(['sgf'])])
    submit = SubmitField('Zapisz')
