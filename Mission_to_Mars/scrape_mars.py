import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    marsFeed = {}

    # Assign URL to variable
    url = "https://mars.nasa.gov/news/"

    # Send splinter module to the url
    browser.visit(url)

    # Give the site a few seconds to fully load
    time.sleep(0.5)

    # Assign splinter instance to a variable and make some soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Scrape first news headline into key:value pair
    marsFeed['headline'] = soup.find(
        'div', class_='bottom_gradient').find_all('h3')[0].text.strip()

    # Scrape first new headline description into key:value pair
    marsFeed["teaser"] = soup.find(
        "div", class_="article_teaser_body").get_text()

    # Assign URL string to variable
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    # Send splinter to URL
    browser.visit(url)

    # Navigate to full size photo of first mars image
    browser.find_by_id('filter_Mars').click()
    browser.find_by_css('.BaseImage').first.click()

    # Give the site a few seconds to fully load
    time.sleep(0.5)

    # Make a NEW soup object with the HTML where splinter stopped
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Scrape the URL for the full sized image into a key:value pair
    marsFeed['featured_image_url'] = soup.find(
        'img', class_='BaseImage')['data-src']

    # Assign URL ot a variable
    url = 'https://space-facts.com/mars/'

    # Using pandas read all tables on page into a list of tables
    tables = pd.read_html(url)

    # Assign required table to a dataframe
    df = tables[0]

    # Set Index to fact descriptor
    df.set_index(0, inplace=True)

    # Clean up column headers
    df = df.rename(columns={1: 'Mars'})
    df.index.name = 'Description'

    marsFeed['mars_facts'] = df.to_html(
        classes='table table-warning table-striped table-hover')

    # Empty dictionary container to hold web scrapes
    hemisphere_image_urls = []

    # Assign URL string to variable
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # Tell splinter to click link to navigate to full size photo of first mars image
    for x in range(0, 4):

        # Send splinter to URL
        browser.visit(url)

        # Initialize container to store key:value pairs
        mars_dict = {}

        # Click through the links
        browser.find_by_css('h3')[x].click()

        # Give the site a few seconds to fully load
        time.sleep(0.5)

        # Make a NEW soup object with the HTML where splinter stopped
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")

        # Scrape the URL for the full sized image into a key:value pair
        mars_dict['title'] = soup.find('h2', class_='title').get_text()
        mars_dict['img_url'] = soup.li.find('a')['href']

        # Append Dictionary to List
        hemisphere_image_urls.append(mars_dict)

    # Quit the Browser
    browser.quit()

    # Attachllist of dictionaries to parent dictionary
    marsFeed['hemisphere_images'] = hemisphere_image_urls

    return marsFeed
