#This is the main code for the python web app
#utilizing flask

from flask import Flask, flash, request, render_template, url_for, redirect
from wtf import DataForm, DateTicker                                    #This is inputing wtf.py that handles the user input form using wt forms
from flask_wtf import FlaskForm
from pandas_datareader import data                                      #used to grab stock market data from a website
import datetime                                                         #used to verify if dates are valid and to be passed to the line above ^

app = Flask(__name__)

app.config['SECRET_KEY'] = '4a154d92aa66f3d7ee1970f60e3be066'       #having a secret key is required for security purposes on wt forms

# creating dictionary that stores company names (all lowercase) that we are supporting.
#key is the companies name for easy searching. Value is a tuple where first element is the
#company's stock market abbreviation and the second element is the name of the image of the company's logo
companydict = {'tesla': ('TSLA', 'tesla_logo.jpg'), 'amazon': ('AMZN', 'amazon_logo.jpg'),
               'apple': ('AAPL', 'apple_logo.png'), 'google': ('GOOG', 'google_logo.png'),
               'starbucks': ('SBUX', 'starbucks_logo.jpg'), 'nike': ('NKE', 'nike_logo.jpg'),
               'microsoft': ('MSFT', 'microsoft_logo.jpg'), 'facebook': ('FB','facebook_logo.png'),
               'exxonmobil': ('XOM','exxonmobil_logo.png'), 'disney': ('DIS', 'disney_logo.jpg'),
               'walmart': ('WMT','walmart_logo.jpg'), 'visa': ('V', 'visa_logo.png'),
               'mcdonalds': ('MCD','mcdonalds_logo.jpg'), 'intel': ('INTC', 'intel_logo.png'),
               'nintendo': ('NTDOY', 'nintendo_logo.jpg')}

abbdict = {'tsla': 'tesla', 'amzn':'amazon', 'aapl':'apple', 'goog':'google', 'sbux':'starbucks', 'nke':'nike', 'msft':'microsoft',
           'fb':'facebook', 'xom':'exxonmobil', 'dis':'disney', 'wmt':'walmart', 'v':'visa', 'mcd': 'mcdonalds', 'intc':'intel', 'ntdoy':'nintendo'}

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
    if form.validate_on_submit():                                               #when the form is submitted (pressing the submit("Create Graph") button doesn't work right now, you have to just press <enter>
        name = form.company.data.lower()                                        #convert user input to all lower case
        if name in companydict.keys():                                              #check if the user input is one of the keys in the dictionary companydict
            return redirect(url_for('Company_Page', name=name))                 #if valid company name redirect to custom url with extension /stocks/<companyname>
        if name in abbdict.keys():                                                  #if user didn't type in valid company name check if they typed in the
            name = abbdict[name]                                                #stock market abbreviation for one of the companies and associate this
            return redirect(url_for('Company_Page', name=name))                 #abbreviation back to the company's name
        else:                                                                       #if invalid company name print error message
            flash('Please Enter One of the Company Names Listed Below')         #error message for typing in a company name that we aren't supporting
    return render_template('data.html', form=form)


@app.route("/stocks/<name>", methods=['POST', 'GET'])                                                    #dynamic url where the "<name>" part is the valid company name that the user inputted
def Company_Page(name):
    abb = companydict[name][0]                                                  #grabs the stock abbreviation that corresponds to the company name from the company dictionary
    logo = companydict[name][1]                                                 #grabs the logo picture file extension that corresponds to the company name from the company dictionary
    form = DateTicker()                                                                 #wt form that gets the year, month, and day that you want your stock market data to start at
    if form.validate_on_submit():
        #beginning of the code that andres and diego wrote to get stock market data from yahoo
        startyear = form.startyear.data                                                             #getting the data that was submitted in the wt form
        startmonth = form.startmonth.data
        startday = form.startday.data
        now = datetime.datetime.now()                                                               #creating a datetime object to represent the present to be passed to the pandas datareader
        a = now.year
        b = now.month
        c = now.day
        start = datetime.datetime(startyear, startmonth, startday)                                  #start getting stock data at the start date
        end = datetime.datetime(a, b, c)                                                                        #up until the current day
        AlltheData = data.DataReader(name=abb, data_source="yahoo", start=start, end=end)           #***** this bit of code is what grabs the stock data from yahoo *****
        #end of andres and diego's code
        return render_template('Plot.html', name=name, AlltheData=AlltheData)                       #displaying new html page at same url that will display the candlestick graph (right now just prints data in raw number form)
    return render_template('Company_Page.html', name=name, abb=abb, logo=logo, form=form)                           #passes the company name, abbreviation, and logo file extension to the html file so that
                                                                                                                                #the web page can be dynamically rendered with company specifics on it



if __name__ == '__main__':                                  #main
   app.run(debug= True)

