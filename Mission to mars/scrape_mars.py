import pymongo
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

# For all reference homeworks on database setup and creation, scrape craigslist, and scrape costa example homeworks 
# https://www.w3schools.com/python/python_mongodb_create_db.asp

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars 

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'C:/Users/IRENE/.wdm/drivers/chromedriver/win32/87.0.4280.20/chromedriver.exe'}
    return Browser("chrome", **executable_path,headless=False)

def scrape():
    browser = init_browser()
    collection.drop()

 # visit Nasa Mars news, find elements of title and define

    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(1)
    news_html = browser.html
    news_soup = bs(news_html,'lxml')
    news_title = news_soup.find("div", class_="content_title").text
    news_paragraph = news_soup.find("div", class_="article_teaser_body").text

# JPL Mars Space Images -visit Featured Image find elements and define path. ref: https://www.w3schools.com/python/ref_string_rstrip.asp
    jurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jurl)
    time.sleep(1)
    jhtml = browser.html
    jpl_soup = bs(jhtml,"html.parser")
    image_url = jpl_soup.find('div',class_='carousel_container').article.footer.a['data-fancybox-href']
    image_link = "https:"+jpl_soup.find('div', class_='jpl_logo').a['href'].rstrip('/')
    feature_url = image_link+image_url
    featured_image_title = jpl_soup.find('h1', class_="media_feature_title").text.strip()
   

#References:Mars Facts;find table identifiers, pandas read and convert to html, add columns.
#https://www.pluralsight.com/guides/extracting-data-html-beautifulsoup
#https://stackoverflow.com/questions/61987454/how-to-make-bootstrap-table-filter-control-work-with-flask-jinja-and-dataframe
#visit website, find table, use bs to parse html, initiate a list, iterate through values in columns adding to list,
#pass dictionary to create dataframe and convert to html
    mars_fact_url = 'https://space-facts.com/mars/'
    browser.visit(mars_fact_url)
    time.sleep(1)
    mars_fact_html = browser.html
    mars_fact_bs = bs(mars_fact_html, 'html.parser')     
    fact_table = mars_fact_bs.find('table', class_='tablepress tablepress-id-p-mars')
    column1 = fact_table.find_all('td', class_='column-1')
    column2 = fact_table.find_all('td', class_='column-2')

    descriptors = []
    values = []

    for row in column1:
        descriptor = row.text.strip()
        descriptors.append(descriptor)
        
    for row in column2:
        value = row.text.strip()
        values.append(value)
        
    mars_fact = pd.DataFrame({
        "Descriptor":descriptors,
        "Value":values
        })

    mars_fact_html = mars_fact.to_html(header=False, index=False)
    

# Mars Hemispheres. Tutor help plus ref scrape costa lesson for relative image path etc
#ref:https://stackoverflow.com/questions/36107353/python-beautifulsoup-get-all-href-in-children-of-div
#visit url, initiate dictionary for hemi's, define pathway, iterate through list of hemis and add to dictionary
#https://www.w3schools.com/tags/tag_a.asp
    mhemiurl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mhemiurl)  
    time.sleep(1)
    mhtml = browser.html 
    mhemi_soup = bs(mhtml,"html.parser") 
    hemispheres = mhemi_soup.find_all("div",class_='item')
    hemisphere_image_urls = []
    for hemisphere in hemispheres:
        hemispheres = {}
        titles = hemisphere.find('h3').text
        image_path = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + image_path  
        browser.visit(image_link)
        html = browser.html
        soup= bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemispheres['title']= titles
        hemispheres['image_url']= image_url
        hemisphere_image_urls.append(hemispheres)
  

    # Close the browser after scraping
    browser.quit()

    # Return results,store in dictionary ref: lesson 3,5/6. Homeworks on databse creation and scrape/craigslist
    mars_data ={
        'news_title' : news_title,
        'paragraph': news_paragraph,
        'featured_image': feature_url,
        'featured_image_title': featured_image_title,
        'fact_table': mars_fact_html,
        'hemisphere_image_urls': hemisphere_image_urls,
        
        }
    collection.insert(mars_data)








