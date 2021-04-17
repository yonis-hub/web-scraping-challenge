# Dependencies
import os
import time
import requests
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs

def init_browser():

    # Set Executable Path
    executable_path = {"executable_path": "/Users/hyonis/Downloads/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

### Scrape NASA Mars News!
#-----------------------
def scrape():
    browser = init_browser()

    # URL of page to be scraped
    news_url = "https://redplanetscience.com/"

    # Retrieve page with the requests module
    browser.visit(news_url)
    time.sleep(1)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(browser.html, 'html.parser')

    #collect the latest "News Title "and "Paragraph Text". 
    #Save these items to variables so that you can use them later. 

    news_title = soup.find('div', class_="content_title").get_text()
    article_teaser = soup.find('div', class_="article_teaser_body").get_text()

    print(news_title)
    print(article_teaser)

    print("Mars News Scraping Complete!....")


#--------------------------------------------
### JPL Mars Space Images - Featured Image
#-------------------------------------------

    # Visit the url for the Featured Space Image site 
    jpl_url = "https://spaceimages-mars.com"

    # Retrieve page with the requests module
    browser.visit(jpl_url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(browser.html, 'html.parser')

    print(soup.prettify())


    # find the image url for the current Featured Mars Image and assign the url string
    featured_image = soup.find('img', class_="headerimage fade-in")['src']


    #Make sure to save a complete url string for this image.
    featured_image_url = jpl_url + featured_image
    featured_image_url
    
    print("JPL Scraping Complete!.....")
#--------------------------------------
### Mars Facts
#---------------------------------------

    #Visit the Mars Facts webpage 
    facts_url= 'https://galaxyfacts-mars.com'

    # Retrieve page with the requests module
    browser.visit(facts_url)

    # use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    table = pd.read_html(facts_url)
    #type(table)

    #save the data into a df
    df = table[0]
    df = df.drop([0])
    print(df)

    #DataFrames as HTML

    #Pandas also had a `to_html` method that we can use to generate HTML tables from DataFrames.
    html_table = df.to_html()
    print(html_table)

    # strip unwanted newlines to clean up the table
    html_table.replace('\n', '')

    #save the table directly to a file
    df.to_html('table.html')

    print("Mars Facts Scraping Complete!.....")

#-----------------------------------------
### Mars Hemispheres
#-----------------------------------------

    #Visit the astrogeology site 
    hemi_url = 'https://marshemispheres.com/'   

    # Retrieve page with the requests module
    browser.visit(hemi_url)
    time.sleep(1) 

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(browser.html, 'html.parser')

    #obtain high resolution images for each of Mars's hemispheres.
    hemisphere_image_urls = []

    # results = soup.find("div", class_="collapsible results")
    # print(results)
    # hemispheres = soup.find("div", class_="item")
    # print(hemispheres)


    for x in range(4):
        
        # Retrieve html to know what I'm scraping for
        browser.links.find_by_partial_text('Hemisphere').click()
        html = browser.html
        soup = bs(html, 'html.parser')
        hemisphere_dict = {}

        # Extract the title
        hemi_title = soup.find('div', class_ = 'cover')
        hemi_title = hemi_title.h2.text.split(' ')[:-1]
        hemi_title = " ".join(hemi_title)
        hemisphere_dict['title'] = hemi_title

        # Extract image url
        image_url = soup.find('ul').li.a['href']
        hemisphere_dict['img_url'] = f"{url}{image_url}"
        
        # Append dict to list
        hemisphere_image_urls.append(hemisphere_dict)
        
        # Go back to main page 
        browser.links.find_by_partial_text('Back').click()

    print("Mars Hemispheres Scraping Complete!.....")


    scrape_data = {
        'news_title': news_title,
        'articles_teaser': article_teaser,
        'featured_image_url': featured_image_url,
        'html_table': html_table,

    }

    return scrape_data