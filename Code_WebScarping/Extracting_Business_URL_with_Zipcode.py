# !pip install selenium
import pandas as pd
import urllib
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from urllib.parse import urlparse
import time
import json


# Returns a list of url's where each url in the list is yelp page url for combination of zipcode and category
def Extracting_Yelp_Main_URl_By_Zipcodes(category, zipcodes):
    zipcode_URL = []
    for zipcode in zipcodes:
        zipcode_URL.append('https://www.yelp.com/search?find_desc={0}&find_loc={1}&start=0'.format(category,zipcode))
    return zipcode_URL


# Function to extract the URL of pages which has the business links
def Extracting_URL(main_url, links):
    
    # initiating the webdriver. Parameter includes the path of the webdriver.
    driver = webdriver.Chrome('../chromedriver/chromedriver.exe')
    driver.get(main_url)
    # this is just to ensure that the page is loaded
#     time.sleep(3)
    html = driver.page_source
    driver.quit()  
    # Now, we apply beautiful soup to html variable
    soup = BeautifulSoup(html, "html.parser")
    # finding all tags in the soup
    tags = soup('a', href=True)
    # checking each tag and appending to the links list if it is valid
    for tag in tags:
        if "start" in tag["href"]:
            if ('www.yelp.com/search?find_desc=' in tag['href'] ) and (tag['href'] not in links) and ('login' not in tag['href']) and ('signup'not in tag['href'])and ('biz' not in tag['href']):
                links.append(tag['href'])
    return links


# function to extract the Business URl from the page
def Extracting_Business_URL(main_url, base_url, Business_links):

    # initiating the webdriver. Parameter includes the path of the webdriver.
    driver = webdriver.Chrome('../chromedriver/chromedriver.exe')
    driver.get(main_url)
    # this is just to ensure that the page is loaded
#     time.sleep(3)
    html = driver.page_source
    driver.quit()
    
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all("a", class_="css-166la90")
    
    # checking each tag and if it is a business tag appending to the Business list if it is valid
    for tag in tags:
        if ("osq" in tag["href"]) :
            Business_links.append(base_url + tag['href'])

    return Business_links

# the main function accepts the below params
#  base_url : yelp url 
#  main_url : url obtained from category and zipcode combination
#  counter  : counter to know count of present url
#  city     : selected city
#  category : selected category

def main(base_url,main_url,current_zipcode, city, category):
    
    # list to store the url of pages with business list
    links = []
    
    # list to store the list of business url
    Business_links = []
    
    # Extracting all page urls with business list
    for i in range(1, 6):       
        #calling the function to extract the url pages with business url
        links = Extracting_URL(main_url, links)
        # setting the last url of the list from the result of above function as main_url
        if len(links)>0:
            main_url = links[-1]
            
    if len(links)>0:             
        for link in links:
            #calling the function to extract the business url from the function
            Business_links=Extracting_Business_URL(link, base_url, Business_links)
    else:
        Business_links=Extracting_Business_URL(main_url, base_url, Business_links)
        
    # Saving all the Business URL to csv file
    df = pd.DataFrame({'Business_links': Business_links})
    df.to_csv('../Data_Business_URL_City_and_Category_Wise/{0}/{1}/Business_links_{2}.csv'.format(city, category, current_zipcode))
    
    print(len(Business_links))
    return 0


if __name__== '__main__':
    
    # Loading the Zipcodes from the json file
    # Zipcode_data is a dictonary object with 'key'=city name and 'values' = zipcodes for city 
    with open('../Data_HTML_Tags/zipcodes.json') as f:
        zipcode_data = json.load(f)
     
    #####################################Input Data#############################################   
    # Reading the input data city and category from json file
    with open('../Data_HTML_Tags/Input.json') as f:
        Input_data = json.load(f)
    
    city = Input_data['city']
    category = Input_data['category']
    
    zipcodes = zipcode_data[city]
    
    print("starting time:", time.localtime(time.time()))
    zipcode_URL = Extracting_Yelp_Main_URl_By_Zipcodes(category, zipcodes)
#     print(len(zipcode_URL))
    
    for i in range(0,len(zipcode_URL),1):
#         try:
            # base URl is the main yelp URL
        base_url = 'https://www.yelp.com'
            
            # main_url is the intial search page url with results based on category and zipcode
        main_url = zipcode_URL[i]
        current_Zipcode = zipcodes[i]
            
            # parsing the url to make sure the url is correct
        parse = urlparse(main_url)
        main_url= parse.geturl()
        print(i,main_url)
                
            # calling the main function
        main(base_url, main_url, current_Zipcode, city, category) 
        
        break
#         except:
#             print('failed URL')
#             print(i,main_url)
#             pass


