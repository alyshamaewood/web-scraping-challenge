#create imports
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

import pandas as pd

def super_scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    title, paragraph = nasa_news(browser)

    mars_data = {
        "title" : title,
        "paragraph" : paragraph,
        "image" : "",
        "facts_table" : "",
        "hemispheres" : "",
        "last_modified" : dt.datetime.now()
    }
    print("hello world")
    browser.quit()
    return mars_data

def nasa_news(browser):
    url = "https://mars.nasa.gov/news/"

    browser.visit(url)

    browser.is_element_present_by_css("li.slide", wait_time=1)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    try:
        latestArticle = soup.find('li', class_='slide')

        title = latestArticle.find('div', class_='content_title').text

        paragraph = latestArticle.find('div', class_='article_teaser_body').text

    except AttributeError:
        return None, None

    return title, paragraph