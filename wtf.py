#This is the code for the form that accepts user input on the data page
#Utilizing wtforms from flask

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField     #Form, SubmitField
from wtforms.validators import DataRequired

class DataForm(FlaskForm):
    #The Data form has one variable, the name of the company. Data must be entered into the form in order to submit
    company = StringField('companyname', validators=[DataRequired()])
#submitt button wasn't working and I figured out how to add it inside of data.html so i'm still working on it
    #submit button
    #submit = SubmitField('Create graph')



