from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
from urllib.parse import urlparse


# Function to extract the URL of pages
def Extracting_URL(main_url, links):
    URL = main_url
    # initiating the webdriver. Parameter includes the path of the webdriver.
    driver = webdriver.Chrome('C:/Users/Prudhvi/Anaconda3/chromedriver')
    # time.sleep(5)
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
            #             print(tag['href'])
            if ('www.yelp.com/search?find_desc=' in tag['href']) and (tag['href'] not in links) and (
                    'login' not in tag['href']) and ('signup' not in tag['href']) and ('biz' not in tag['href']):
                # if (tag['href'] not in links) and ('login' not in tag['href']) and ('signup'not in tag['href']) and ('biz' not in tag['href']):
                print(tag['href'])
                links.append(tag['href'])
    return links


# and (base_url + tag['href'] not in Business_links
def Extracting_Business_URL(main_url, base_url, Business_links):
    URL = main_url
    # initiating the webdriver. Parameter includes the path of the webdriver.
    driver = webdriver.Chrome('C:/Users/Prudhvi/Anaconda3/chromedriver')
    time.sleep(2)
    driver.get(URL)
    # this is just to ensure that the page is loaded
    time.sleep(3)
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all("a", class_="css-166la90")
    #     print(tags)
    for tag in tags:
        if ("osq" in tag["href"]):
            Business_links.append(base_url + tag['href'])

    return Business_links


def main(base_url, main_url, num):
    # list to store the links of pages with business list
    links = []
    # list to store the list of business url
    Business_links = []
    # adding the first page url with business list
    #     links.append(main_url + '&start=0')
    # Extracting all page urls with business list
    for i in range(1, 6):
        links = Extracting_URL(main_url, links)
        url = links[-1]
        main_url = url
    #     print(links)

    # Extracting all Business URL from all pages
    for link in links:
        Business_links = Extracting_Business_URL(link, base_url, Business_links)
    # Saving all the Business URL to csv file
    df = pd.DataFrame({'Business_links': Business_links})
    df.to_csv(f'Businesslinks_with_zipcode/Business_links{num}.csv')
    # print(len(Business_links))
    return Business_links


if __name__ == '__main__':
    # Oklahoma City Zipcodes
    zipcode = [73101, 73102, 73103, 73104, 73105, 73106, 73107, 73108, 73109, 73110,
               73111, 73112, 73113, 73114, 73115, 73116, 73117, 73118, 73119, 73120,
               73121, 73122, 73123, 73124, 73125, 73126, 73127, 73128, 73129, 73130,
               73131, 73132, 73134, 73135, 73136, 73137, 73139, 73140, 73141, 73142,
               73143, 73144, 73145, 73146, 73147, 73148, 73149, 73150, 73151, 73152,
               73153, 73154, 73155, 73156, 73157, 73159, 73160, 73162, 73163, 73164,
               73165, 73167, 73169, 73170, 73172, 73173, 73178, 73179, 73184, 73185,
               73189, 73190, 73194, 73195, 73196]

    # Generating the URL based on Zipcode
    zipcode_URL = []
    for i in zipcode:
        #adding the URL for category and zipcode
        zipcode_URL.append(f'https://www.yelp.com/search?find_desc=plumbing&find_loc={i}&start=0')

    df_temp = pd.DataFrame(columns=['Zipcode_url'])
    df_temp['Zipcode_url'] = zipcode_URL
    Zipcode_URl_list = df_temp['Zipcode_url']
    Zipcode_URl_list = Zipcode_URl_list.tolist()
    #     len(Zipcode_URl_list)
    for num in range(0, len(Zipcode_URl_list), 1):
        # main_url is the intial search page url with results
        main_url = Zipcode_URl_list[num]
        parse = urlparse(main_url)
        main_url = parse.geturl()
        # Base yelp url
        print(main_url)
        num = zipcode[num]
        base_url = 'https://www.yelp.com'
        main(base_url, main_url, num)
