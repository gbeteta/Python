#This is the code for the form that accepts user input on the data page
#Utilizing wtforms from flask

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, InputRequired

class DataForm(FlaskForm):
    #The Data form has one variable, the name of the company. Data must be entered into the form in order to submit
    company = StringField('companyname', validators=[DataRequired()])
    submit = SubmitField(label = 'Submit')

class DateTicker(FlaskForm):
    startyear = IntegerField('Enter the Start Year', validators=[DataRequired()])
    startmonth = IntegerField('Enter the Start Month(1-12)', validators=[DataRequired()])
    startday = IntegerField('Enter the Start Day', validators=[DataRequired()])
    submit = SubmitField(label = 'Submit')


