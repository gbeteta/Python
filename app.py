#This is the main code for the python web app
#utilizing flask

from flask import Flask, flash, request, render_template, url_for, redirect
from wtf import DataForm, DateTicker                                    #This is inputing wtf.py that handles the user input form using wt forms
from pandas_datareader import data                                      #used to grab stock market data from a website
import datetime                                                         #used to verify if dates are valid and to be passed to the line above ^
from bokeh.plotting import figure, show


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

monthdaydict = {1:31, 2:29, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}                          #Dictionary telling how many days are in each month used for error checking later on (yes problems would occur here with leap days)


def valid_date(year1, month1, day1, year2, month2, day2):               #function that Andres and Diego wrote that checks if datetime 1 comes before 2
    date1 = datetime.datetime(year1, month1, day1)
    date2 = datetime.datetime(year2, month2, day2)
    if date2 >= date1:
        return True
    else:
        return False


@app.route("/")
@app.route("/Home")                                         #Home Page
def home():                                                 #just returns the html template for this page
    return render_template('Home.html')


@app.route("/Team_Members")                                 #Team Members Page
def Team_Members():                                         #just returns the html template for this page
    return render_template('Team_Members.html')


@app.route("/stocks", methods=['POST', 'GET'])
def stocks():
    
    form = DataForm() #creating a form object
    content = {'Tesla': ('TSLA', 'tesla_logo.jpg'), 'Amazon': ('AMZN', 'amazon_logo.jpg'),
    'Apple': ('AAPL', 'apple_logo.png'), 'Google': ('GOOG', 'google_logo.png'), 
    'Starbucks': ('SBUX', 'starbucks_logo.jpg'), 'Nike': ('NKE', 'nike_logo.jpg'),
    'Microsoft': ('MSFT', 'microsoft_logo.jpg'), 'Facebook': ('FB','facebook_logo.png'),
    'Exxonmobil': ('XOM','exxonmobil_logo.png'), 'Disney': ('DIS', 'disney_logo.jpg'),
    'Walmart': ('WMT','walmart_logo.jpg'), 'Visa': ('V', 'visa_logo.png'),
    'Mcdonalds': ('MCD','mcdonalds_logo.jpg'), 'Intel': ('INTC', 'intel_logo.png'),
    'Nintendo': ('NTDOY', 'nintendo_logo.jpg')}
    name = str(request.form.get('comp_select'))#receiving the input from the user selection. 
    if name in content.keys():
        return redirect(url_for('Company_Page', name=name.lower()))
    return render_template('data.html', form=form, content=content)


@app.route("/stocks/<name>", methods=['POST', 'GET'])                                                    #dynamic url where the "<name>" part is the valid company name that the user inputted
def Company_Page(name):
    abb = companydict[name][0]                                                  #grabs the stock abbreviation that corresponds to the company name from the company dictionary
    logo = companydict[name][1]                                                 #grabs the logo picture file extension that corresponds to the company name from the company dictionary
    form = DateTicker()                                                                 #wt form that gets the year, month, and day that you want your stock market data to start at

    #Prefilling end day with the current day. User can change it afterwards if they want to
    if request.method == "GET":
        now = datetime.datetime.now()
        form.endyear.data = now.year
        form.endmonth.data = now.month
        form.endday.data = now.day

    if form.validate_on_submit():
        message = ' '                                                                                 #Used for displaying error messages. Default no error message
        # Beginning of the code that andres and diego wrote to get stock market data from yahoo (with James's error checking and message system)
        now = datetime.datetime.now()                                                               #creating a datetime object to represent the present. Used to check if inputted start and end dates have already happened and aren't in the future
        currentyear = now.year
        currentmonth = now.month
        currentday = now.day
        current = datetime.datetime(currentyear, currentmonth, currentday)

        startyear = form.startyear.data                                                             #getting the data that was submitted in the wt form
        startmonth = form.startmonth.data
        startday = form.startday.data
        endyear = form.endyear.data
        endmonth = form.endmonth.data
        endday = form.endday.data

        #Error checking dates. If there are any issues with the inputted dates then return a link to the company page that they were already on
        if startmonth > 12 or startmonth < 1 or endmonth > 12 or endmonth < 1:                                                #checking if valid month was inputted
            message = 'Error: Please enter a valid month (1-12)'
            return render_template('Company_Page.html', name=name, abb=abb, logo=logo, form=form, message=message)
        elif startmonth == 2 and startday == 29:                                                                              #checking leap year for start day
            if startyear % 4 != 0:
                message = 'Error: That year does not have a leap day'
                return render_template('Company_Page.html', name=name, abb=abb, logo=logo, form=form, message=message)
            elif startyear % 100 == 0 and startyear % 400 != 0:
                    message = 'Error: That year does not have a leap day'
                    return render_template('Company_Page.html', name=name, abb=abb, logo=logo, form=form, message=message)
        elif endmonth == 2 and endday == 29:                                                                                  #checking leap year for end day
            if endyear % 4 != 0:
                message = 'Error: That year does not have a leap day'
                return render_template('Company_Page.html', name=name, abb=abb, logo=logo, form=form, message=message)
            elif endyear % 100 == 0 and endyear % 400 != 0:
                    message = 'Error: That year does not have a leap day'
                    return render_template('Company_Page.html', name=name, abb=abb, logo=logo, form=form, message=message)
        elif startyear < 1990 or endyear < 1990:
            message = 'Error: Enter a year 1990 or later'
            return render_template('Company_Page.html', name=name, abb=abb, logo=logo, form=form, message=message)
        elif startday < 1 or endday < 1 or monthdaydict[startmonth] < startday or monthdaydict[endmonth] < endday:            #checking that the day enter exists in the month that was entered
            message = 'Error: Enter a valid day number for the month you inputted'
            return render_template('Company_Page.html', name=name, abb=abb, logo=logo, form=form, message=message)
        elif valid_date(startyear, startmonth, startday, currentyear, currentmonth, currentday) == False:                     #checking that the start day isn't in the future
            message = 'Error: Please enter a start day that is not in the future'
            return render_template('Company_Page.html', name=name, abb=abb, logo=logo, form=form, message=message)
        elif valid_date(endyear, endmonth, endday, currentyear, currentmonth, currentday) == False:                           #checking that the end day isn't in the future
            message = 'Error: Please enter an end day that is not in the future'
            return render_template('Company_Page.html', name=name, abb=abb, logo=logo, form=form, message=message)
        elif valid_date(startyear, startmonth, startday, endyear, endmonth, endday) == False:                                 #checking that the startday comes before the end day
            message = 'Error: Please enter a start day that comes before the end day'
            return render_template('Company_Page.html', name=name, abb=abb, logo=logo, form=form, message=message)
        #Valid Input so going out to yahoo to get the stock data

        start = datetime.datetime(startyear, startmonth, startday)                                                          #start getting stock data at the start date
        end = datetime.datetime(endyear, endmonth, endday)                                                                  #up until the current day
        df = data.DataReader(name=abb, data_source="yahoo", start=start, end=end)                                   #***** this bit of code is what grabs the stock data from yahoo *****

        #Andres's graphing
        def inc_dec(c, o):
            if c > o:
                value = "Increase"
            elif c < o:
                value = "Decrease"
            else:
                value = "Equal"
            return value
        df["Status"] = [inc_dec(c, o) for c, o in zip(df.Close, df.Open)]
        df["Middle"] = (df.Open + df.Close) / 2
        df["Height"] = abs(df.Close - df.Open)
        p = figure(x_axis_type='datetime', width=1600, height=500)
        abb = companydict[name][0]
        p.title.text = name.capitalize() + " (" + abb + ")"
        p.grid.grid_line_alpha = 0.4
        hours_12 = 12 * 60 * 60 * 1000
        p.segment(df.index, df.High, df.index, df.Low, color="Black")
        p.rect(df.index[df.Status == "Increase"], df.Middle[df.Status == "Increase"],
               hours_12, df.Height[df.Status == "Increase"], fill_color="#CCFFFF", line_color="black")
        p.rect(df.index[df.Status == "Decrease"], df.Middle[df.Status == "Decrease"],
               hours_12, df.Height[df.Status == "Decrease"], fill_color="#FF3333", line_color="black")
        show(p)
        #End Andres's Graph Stuff

        form = DataForm()
        content = {'Tesla': ('TSLA', 'tesla_logo.jpg'), 'Amazon': ('AMZN', 'amazon_logo.jpg'), 'Apple': ('AAPL', 'apple_logo.png'), 'Google': ('GOOG', 'google_logo.png'),
        'Starbucks': ('SBUX', 'starbucks_logo.jpg'), 'Nike': ('NKE', 'nike_logo.jpg'),
        'Microsoft': ('MSFT', 'microsoft_logo.jpg'), 'Facebook': ('FB','facebook_logo.png'),
        'Exxonmobil': ('XOM','exxonmobil_logo.png'), 'Disney': ('DIS', 'disney_logo.jpg'),
        'Walmart': ('WMT','walmart_logo.jpg'), 'Visa': ('V', 'visa_logo.png'),
        'Mcdonalds': ('MCD','mcdonalds_logo.jpg'), 'Intel': ('INTC', 'intel_logo.png'),
        'Nintendo': ('NTDOY', 'nintendo_logo.jpg')}
        return render_template('data.html', form=form, content=content)                                               #displaying new html page at same url that will display the candlestick graph (right now just prints data in raw number form)
    return render_template('Company_Page.html', name=name, abb=abb, logo=logo, form=form)                                   #passes the company name, abbreviation, and logo file extension to the html file so that
                                                                                                                                #the web page can be dynamically rendered with company specifics on it

if __name__ == '__main__':                                  #main
   app.run(debug= True)

