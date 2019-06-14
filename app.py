#This is the main code for the python web app
#utilizing flask

from flask import Flask, flash, request, render_template, url_for, redirect
from wtf import DataForm                                    #This is inputing wtf.py that handles the user input form using wt forms
from flask_wtf import FlaskForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '4a154d92aa66f3d7ee1970f60e3be066'       #having a secret key is required for security purposes on wt forms

@app.route("/")
@app.route("/Home")                                         #Home Page
def home():                                                 #just returns the html template for this page
    return render_template('Home.html')

@app.route("/Team_Members")                                 #Team Members Page
def Team_Members():                                         #just returns the html template for this page
    return render_template('Team_Members.html')

@app.route("/stocks", methods=['POST', 'GET'])
def stocks():
    form = DataForm()                                                           #creating a form object
    if form.validate_on_submit():                                               #when the form is submitted (pressing the submit("Create Graph") button doesn't work right now,
        if form.company.data == 'Tesla' or form.company.data == 'tesla':            #you have to just press <enter>
            return redirect(url_for('home'))                                    #!!!!!!!create and change appropriate /stocks/companyname urls
        else:
            flash('Please Enter One of the Company Names Listed Below')         #error message for typing in a company name that we aren't supporting
    return render_template('data.html', form=form)


if __name__ == '__main__':                                  #main
   app.run(debug= True)

