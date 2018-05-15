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
    date = DateField("Date of the event (mm/dd/yyyy):",format ='%m/%d/%Y')
    description = TextField("Description:",[validators.Required("Please enter a description of the date")])
    submit = SubmitField("Add Date")

class AddGift(FlaskForm):
    person = SelectField("Gift idea for whom?",[validators.Required("Please pick a person")])
    gift = TextField("Gift Idea:", [validators.Required("Please describe your gift idea")])
    link = TextField("Amazon URL", [validators.Required("Include a URL or put n/a")])
    submit = SubmitField("Add Gift Idea")

class QueryGift(FlaskForm):
    person = SelectField("Gift idea for whom?",[validators.Required("Please pick a person")])
    submit = SubmitField("Refresh")

class Login(FlaskForm):
    username = TextField("Enter username:",[validators.Required("Please enter a username")])
    submit = SubmitField("Log In")