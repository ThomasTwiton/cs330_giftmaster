from flask_wtf import FlaskForm
from wtforms import SelectField, BooleanField, SubmitField, DateField, TextField
from wtforms import validators, ValidationError

#Forms#

class AddPerson(FlaskForm):
    first_name = TextField("First name:", [validators.Required("Please enter a first name")])
    middle_name = TextField("Middle name:",[validators.Required("Please enter a middle name")])
    last_name = TextField("Last name:", [validators.Required("Please enter a last name")])
    nickname = TextField("Nickname:", [validators.Required("Please enter a nickname (first name again will do)")])
    relationship = TextField("Relationship:", [validators.Required("Please describe your relationship to this person")])
    submit = SubmitField("Add Person")

class AddDate(FlaskForm):
    person = SelectField("Important date for whom?",[validators.Required("Please pick a person")])
    date = TextField("Date of the event (mm/dd/yyyy):",[validators.Required("Please enter a date in MM/DD/YYYY form")])
    description = TextField("Description:",[validators.Required("Please enter a description of the date")])
    submit = SubmitField("Add Date")
    