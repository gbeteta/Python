import settings
from bs4 import BeautifulSoup
import pandas as pd
import requests


business_news_page = requests.get("https://www.nasdaq.com/news/market-headlines.aspx")
soup = BeautifulSoup(business_news_page.content,'html.parser')
counter=0
business_lists=[]
for a in soup.find_all('a', {"id": "two_column_main_content_la1_rptArticles_hlArticleLink_0"}):
    news_title = (a.get_text())
    news_web_location = (a['href'])
    business_lists.append(news_title)
    business_lists.append(news_web_location)
    #counter+=1
print (business_lists, end="\n")

"""
#page = requests.get(""
newsLnk = "https://www.nasdaq.com/symbol/"
settings.init()
newsletter = {}
value = 1
all_news = False
if all_news == True:        #Decides whether we want all the news
    for (abr, cname) in settings.myDict.items():
        newsLnk+=abr
        newsLnk+="/news-headlines"
        news_page = requests.get(newsLnk)
        soup = BeautifulSoup(news_page.content, 'html.parser')
        newsletter[cname]=[]
        if value == 1:      #gets one new for all companies
            for a in soup.find_all('a', href=True):
                if cname in a['href']:
                    news_title = (a.get_text())
                    news_web_location = (a['href'])
                    newsletter[cname].append(news_title)
                    newsletter[cname].append(news_web_location)
                    break
        
        else:    #Gets all news for all companies
            for a in soup.find_all('a', href=True):
                if cname in a['href']:
                    news_title = (a.get_text())
                    news_web_location = (a['href'])
                    newsletter.update({cname:[news_title, news_web_location]})
                #newsLnk = "https://www.nasdaq.com/symbol/"
        newsLnk = "https://www.nasdaq.com/symbol/"
else:   #decides whether we want all the news of one company
    for (abr, cname) in settings.myDict.items():
        newsLnk+=abr
        newsLnk+="/news-headlines"
        news_page = requests.get(newsLnk)
        soup = BeautifulSoup(news_page.content, 'html.parser')
        newsletter[cname]=[]
        for a in soup.find_all('a', href=True):
            if cname in a['href']:
                news_title = (a.get_text())
                news_web_location = (a['href'])
                newsletter[cname].append(news_title)
                newsletter[cname].append(news_web_location)
        newsLnk = "https://www.nasdaq.com/symbol/"
        break
print(newsletter)

"""