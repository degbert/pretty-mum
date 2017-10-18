from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import Required
from wtforms_components import DateField, SelectField
from datetime import datetime, timedelta
import os

class SearchForm(FlaskForm):
    free_text = StringField("Free text search")
    chain = StringField("Chain")
    org = StringField("Org")
    submit = SubmitField("Submit")
