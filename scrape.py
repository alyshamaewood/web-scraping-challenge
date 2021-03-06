# create imports
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

import pandas as pd

#  super_scrape function
def super_scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    title, paragraph = nasa_news(browser)

    mars_data = {
        "title" : title,
        "paragraph" : paragraph,
        "image" : jpl_image(browser),
        "facts_table" : facts_table(),
        "hemispheres" : hemisphere(browser),
        "last_modified" : dt.datetime.now()
    }
    
    browser.quit()
    return mars_data

# define function for scraping nasa news data
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

# define function for scraping mars image
def jpl_image(browser):
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    image_button = browser.find_by_id("full_image")
    image_button.click()

    info_button = browser.links.find_by_partial_text("more info")
    info_button.click()

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    try:
        image = soup.find("img", class_="main_image").get("src")
        image_url = f'https://www.jpl.nasa.gov{image}'

    except AttributeError:
        return None

    return image_url

# define function for scraping mars facts
def facts_table():
    fact_url = 'https://space-facts.com/mars/'

    tables = pd.read_html(fact_url)[0]
    tables.columns=['mars attribute', 'value']
    tables.set_index('mars attribute', inplace=True)
    tables.to_html()

    return tables.to_html()

# define function for scraping mars hemisphere images
def hemisphere(browser):
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)

    image_links = browser.find_by_css("a.product-item h3")

    picture_list = []

    for i in range(len(image_links)):
        picture = {}
        browser.find_by_css("a.product-item h3")[i].click()
    
        image_button = browser.links.find_by_partial_text("Sample").first
        picture["href"] = image_button["href"]
    
        picture["title"] = browser.find_by_css("h2.title").text
        picture_list.append(picture)
    
        browser.back()
    
    return picture_list