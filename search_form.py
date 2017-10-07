from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import Required
from wtforms_components import DateField, SelectField
from datetime import datetime, timedelta
import os

class SearchForm(FlaskForm):
    #chain = SelectField("Chain")
    chain = StringField("Chain")
    submit = SubmitField("Submit")
