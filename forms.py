from flask_wtf import FlaskForm
from wtforms import SelectField, BooleanField, SubmitField, DateField, TextField
from wtforms import validators, ValidationError

#Forms#

class AddPerson(FlaskForm):
    first_name = TextField("First name:", [validators.Required("Please enter a first name")])
    middle_name = TextField("Middle name:")
    last_name = TextField("Last name:", [validators.Required("Please enter a last name")])
    nickname = TextField("Nickname:")
    relation = TextField("Relationship:")
    submit = SubmitField("Add Person")

