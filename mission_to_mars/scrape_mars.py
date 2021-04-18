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

#------------------------
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
    # print(article_teaser)
    # print(news_title)

    print("Mars News Scraping Complete!....")

#--------------------------------------------
### JPL Mars Space Images - Featured Image
#-------------------------------------------

    # Visit the url for the Featured Space Image site 
    jpl_url = "https://spaceimages-mars.com"

    # Retrieve page with the requests module
    browser.visit(jpl_url)
    time.sleep(1)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(browser.html, 'html.parser')

    # print(soup.prettify())


    # find the image url for the current Featured Mars Image and assign the url string
    featured_image = soup.find('img', class_="headerimage fade-in")['src']


    #Make sure to save a complete url string for this image.
    featured_image_url = jpl_url + featured_image
    # featured_image_url
    
    print("JPL Scraping Complete!.....")

#--------------------------------------
### Mars Facts
#---------------------------------------

    #Visit the Mars Facts webpage 
    facts_url= 'https://galaxyfacts-mars.com'

    # Retrieve page with the requests module
    browser.visit(facts_url)
    time.sleep(1)

    # use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    table = pd.read_html(facts_url)
    #type(table)

    #save the data into a df
    df = table[0]
    df = df.drop([0])
    # print(df)

    #DataFrames as HTML

    #Pandas also had a `to_html` method that we can use to generate HTML tables from DataFrames.
    html_table = df.to_html()
    # print(html_table)

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
    hemisphere_img_urls = []

    hemispheres = soup.find_all("div", class_="description")
    # print(hemispheres)


    for x in range(4):
        
        hemisphere_dict = {}
        
        # Retrieve html to know what I'm scraping for
        html = hemispheres[x].find(class_="itemLink").get("href")
        print(html)
        img_url = f'{hemi_url}{html}'
        #print(img_url)
        
        #visit the img url site
        browser.visit(img_url)
        
        #click img 
        element = browser.find_by_text('Sample').first
        # print(element)
        
        #add it to the dict
        hemisphere_dict['title'] = browser.find_by_css('h2.title').text
    
        
        hemisphere_dict['img_url'] = element['href']
        # print(hemisphere_dict)
        
        hemisphere_img_urls.append(hemisphere_dict)
        
        #go back to the main page with all the other imgs
        browser.back()

        print("Mars Hemispheres Scraping Complete!.....")

        #Quit the browser
        browser.quit()


    
        mars_data = {'news_title': news_title,
            'articles_teaser': article_teaser,
            'featured_image_url': featured_image_url,
            'html_table': html_table,
            'hemisphere_img_urls': hemisphere_img_urls
        }
        # print(news_title)
        # print(article_teaser)
        # print(featured_image_url)
        # print(html_table)
        # print(hemisphere_img_urls)
        # print(hemisphere_dict)

        return mars_data

 #call the function        
if __name__ == "__main__":
    scrape()

