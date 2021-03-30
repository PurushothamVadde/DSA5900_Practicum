from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time


def Reading_Business_URL_by_Yelp_Search(URL, Business_Name, Business_Location):
    # initiating the webdriver. Parameter includes the path of the webdriver.
    driver = webdriver.Chrome('C:/Users/Prudhvi/Anaconda3/chromedriver')
    driver.get(URL)
    # this is just to ensure that the page is loaded
    time.sleep(2)

    # Perfomring business search operation in yelp using selinum
    driver.find_element_by_xpath('//*[@id="find_desc"]').send_keys(Business_Name)
    driver.find_element_by_xpath('//*[@id="dropperText_Mast"]').clear()
    driver.find_element_by_xpath('//*[@id="dropperText_Mast"]').send_keys(Business_Location)
    driver.find_element_by_xpath('//*[@id="header-search-submit"]').click()
    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('span', class_='css-1pxmz4g')
    # extracting the top search result from the results
    Business_links = []
    for tag in tags:
        if ("1." in tag.text):
            link = URL + tag.find('a')['href']

    driver.quit()
    return link


def main():
    # reading the business and location from the excel
    df = pd.read_csv('BusinessName_and_Location.csv')
    # creating  a Data frame to save data
    Data_Frame = pd.DataFrame(columns=['Business_links'])
    #     # Creating a CSV file with headers to save data
    Data_Frame.to_csv('Business_links.csv', header=True)
    # base yelp URL
    URL = 'https://www.yelp.com/'

    # iterating through each row in the 'BusinessName_and_Location.csv'
    for index, row in df.iterrows():
        Business_Name = row['Business_Name']
        Business_Location = row['Business_Location']
        link = Reading_Business_URL_by_Yelp_Search(URL, Business_Name, Business_Location)
        #         print(link)
        # appending business URL extracted
        Data_Frame = Data_Frame.append({'Business_links': link}, ignore_index=True, sort=False)
        # Data_Frame
    Data_Frame.to_csv('Business_links.csv', mode='a', header=False)
    return 0


if __name__== '__main__':
    main()
