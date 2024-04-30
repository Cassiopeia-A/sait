from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    submit = SubmitField('Поиск')