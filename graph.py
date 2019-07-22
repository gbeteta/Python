{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 77,
   "metadata": {},
   "outputs": [],
   "source": [
    "from pandas_datareader import data\n",
    "import datetime\n",
    "from bokeh.plotting import figure, show, output_file\n",
    "from bokeh.embed import components\n",
    "from bokeh.resources import CDN\n",
    "\n",
    "start=datetime.datetime(2015,11,1)\n",
    "end=datetime.datetime(2016,3,10)\n",
    "\n",
    "df=data.DataReader(name=\"GOOG\",data_source=\"yahoo\",start=start,end=end)\n",
    "\n",
    "\n",
    "def inc_dec(c, o):\n",
    "    if c > o:\n",
    "        value=\"Increase\"\n",
    "    elif c < o:\n",
    "        value=\"Decrease\"\n",
    "    else:\n",
    "        value=\"Equal\"\n",
    "    return value\n",
    "\n",
    "df[\"Status\"]=[inc_dec(c,o) for c, o in zip(df.Close,df.Open)]\n",
    "df[\"Middle\"]=(df.Open+df.Close)/2\n",
    "df[\"Height\"]=abs(df.Close-df.Open)\n",
    "\n",
    "p=figure(x_axis_type='datetime', width=1000, height=300)\n",
    "p.title.text=\"Candlestick Chart\"\n",
    "p.grid.grid_line_alpha=0.4\n",
    "\n",
    "hours_12=12*60*60*1000\n",
    "\n",
    "p.segment(df.index, df.High, df.index, df.Low, color=\"Black\")\n",
    "\n",
    "p.rect(df.index[df.Status==\"Increase\"],df.Middle[df.Status==\"Increase\"], \n",
    "       hours_12, df.Height[df.Status==\"Increase\"], fill_color=\"#CCFFFF\",line_color=\"black\")\n",
    "\n",
    "p.rect(df.index[df.Status==\"Decrease\"],df.Middle[df.Status==\"Decrease\"], \n",
    "       hours_12, df.Height[df.Status==\"Decrease\"], fill_color=\"#FF3333\",line_color=\"black\")\n",
    "\n",
    "script1, div1 =components(p)\n",
    "cdn_js=CDN.js_files[0]\n",
    "cdn_css=CDN.css_files[0]\n",
    "\n",
    "#Comment this out once it is implemented into the plot.html file\n",
    "output_file(\"CS.html\")\n",
    "show(p)\n",
    "\n",
    "#print (div1)\n",
    "\n",
    "#cdn_js[0]\n",
    "\n",
    "#cdn_css[0]"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
