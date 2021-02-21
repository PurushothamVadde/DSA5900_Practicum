import urllib
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time


# Function to extract the URL of pages
def Extracting_URL(mainpage,links):
    URL = mainpage
    # initiating the webdriver. Parameter includes the path of the webdriver.
    driver = webdriver.Chrome('C:/Users/Prudhvi/Anaconda3/chromedriver')
    driver.get(URL)
    # this is just to ensure that the page is loaded
    time.sleep(3)
    html = driver.page_source
    driver.quit()
    # Now, we could simply apply bs4 to html variable
    soup = BeautifulSoup(html, "html.parser")
    tags = soup('a', href=True)
    for tag in tags:
        if "start" in tag["href"]:
            if (tag['href'] not in links) and ('login' not in tag['href']) and ('signup'not in tag['href']):
                # print(tag['href'])
                links.append(tag['href'])
    return links


def Extracting_Business_URL(main_url, base_url, Business_links):
    URL = main_url
    # initiating the webdriver. Parameter includes the path of the webdriver.
    driver = webdriver.Chrome('C:/Users/Prudhvi/Anaconda3/chromedriver')
    driver.get(URL)
    # this is just to ensure that the page is loaded
    time.sleep(3)
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all("a", class_="css-166la90")
    #     print(tags)
    for tag in tags:
        if ("osq=Restaurants" in tag["href"]) and (base_url + tag['href'] not in Business_links):
            Business_links.append(base_url + tag['href'])

    return Business_links


def main(base_url,main_url):
    # list to store the links of pages with business list
    links = []
    # list to store the list of business url
    Business_links = []
    # adding the first page url with business list
    links.append(main_url + '&start=0')
    # Extracting all page urls with business list
    for i in range(1, 10):
        links = Extracting_URL(main_url, links)
        url = links[-1]
        main_url = url
    # links
    # Extracting all Business URL from all pages
    for link in links:
        Extracting_Business_URL(link, base_url, Business_links)
    # Saving all the Business URL to csv file
    df = pd.DataFrame({'Business_links': Business_links})
    df.to_csv('Business_links.csv')

    return Business_links


if __name__== '__main__':

    # main_url is the intial search page url with results
    main_url = 'https://www.yelp.com/search?find_desc=Restaurants&find_loc=Seattle%2C%20WA'
    # Base yelp url
    base_url = 'https://www.yelp.com'
    main(base_url,main_url)
