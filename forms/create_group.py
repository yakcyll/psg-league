from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import PlayingGroup

class CreateGroup(FlaskForm):
    name = StringField('Nazwa grupy', validators=[DataRequired()])
    notes = TextAreaField('Opis')
    hidden = BooleanField('Ukryta')
    submit = SubmitField('Utwórz')

    def validate_name(self, name):
        group = PlayingGroup.query.filter_by(name=name.data).first()
        if group is not None:
            raise ValidationError('Istnieje już grupa o takiej nazwie.')
