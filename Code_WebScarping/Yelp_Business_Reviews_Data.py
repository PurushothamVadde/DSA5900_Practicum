# !pip install selenium
import requests
import urllib
from bs4 import BeautifulSoup
import string
import re
import pandas as pd
import time
from selenium import webdriver
import json
import os
import sys


def Customer_Review_Data(Review_div, html_tags):
    # Intializing the customer features
    Customer_Friends_count = 0
    Customer_Reviews_count = 0
    Customer_Photos_count = 0
    # Customer Name
    try:
        Customer_Name = Review_div.find('span', class_=html_tags['C_Name']).text
    except:
        print("error: The HTML string for C_Name in html_tags Json is not Correct")
    try:
        # Customer Data like friends reviews photos
        Customer_data = Review_div.find('div', class_=html_tags['C_Data'])
        for i in Customer_data.find_all('div'):
            if (i['aria-label']) == 'Friends':
                Customer_Friends_count = i.text
            if (i['aria-label']) == 'Reviews':
                Customer_Reviews_count = i.text
            if (i['aria-label']) == 'Photos':
                Customer_Photos_count = i.text
    except:
        print("error: The HTML string for C_Data in html_tags Json is not Correct")

    try:
        # Customer Rating For Restaurant
        Customer_Rating = (Review_div.find('div', class_=re.compile(html_tags['C_Rating']))['aria-label']).split()[0]
    except:
        print("error: The HTML string for C_Rating in html_tags Json is not Correct")

    try:
        # Customer Review
        Customer_Review = Review_div.find('p', class_=html_tags['C_Review']).text
    except:
        print("error: The HTML string for C_Review in html_tags Json is not Correct")

    try:
        # Customer Review Date
        Customer_Review_Date = Review_div.find('div', class_=html_tags['C_R_Date']).text
    except:
        print("error: The HTML string for C_R_Date in html_tags Json is not Correct")

    try:
        # Like Categories
        likes_class = Review_div.find('div', class_=html_tags['Like_class'])

        Temp_emoji = []
        for span in likes_class.find_all('span', class_=html_tags['Like_Category']):
            if (len((span.text).split()) > 1):
                Temp_emoji.append((span.text).split()[1])
            else:
                Temp_emoji.append(0)

        Customer_Review_Useful = Temp_emoji[0]
        Customer_Review_Funny = Temp_emoji[1]
        Customer_Review_Cool = Temp_emoji[2]
    except:
        print("error: The HTML string for Like_class/Like_Category in html_tags Json is not Correct")

    #######################################################################################################
    # Customer Uploaded photos
    if (Review_div.find('span', class_=html_tags['C_R_Photos'])):
        Customer_Review_Uploaded_Photos = (Review_div.find('span', class_=html_tags['C_R_Photos']).text.split()[0])
    else:
        Customer_Review_Uploaded_Photos = 0

    # Is Customer in Elite Group
    if Review_div.find('p', class_=html_tags['C_Elite']):
        Customer_Elite = 'Yes'
        Customer_Elite_Year = (Review_div.find('p', class_=html_tags['C_Elite'])).text.split()[1]
    else:
        Customer_Elite = 'No'
        Customer_Elite_Year = '0'

        # Business Response class
    if Review_div.find('div', class_=html_tags['B_R_Class']):
        Business_response_class = Review_div.find('div', class_=html_tags['B_R_Class'])
        if Business_response_class.find('div', class_=html_tags['B_R_Check']):
            # Business Response by
            Business_response_By = (Business_response_class.find('p', class_=html_tags['B_R_by'])).text
            # Business Response date
            Business_response_Date = (Business_response_class.find('div', class_=html_tags['B_R_Date'])).text
            # Business  Response
            if Business_response_class.find('p', class_=html_tags['B_Response']):
                Business_Response_for_Review = (Business_response_class.find('p', class_=html_tags['B_Response'])).text
                Business_Response = '1'
            else:
                Business_Response_for_Review = 'Null'
                Business_Response = '0'
        else:
            Business_response_By = 'Null'
            Business_response_Date = 'Null'
            Business_Response_for_Review = 'Null'
            Business_Response = '0'
    else:
        Business_response_By = 'Null'
        Business_response_Date = 'Null'
        Business_Response_for_Review = 'Null'
        Business_Response = '0'

    ######################################################################################################
    Customer_Review_Details = [Customer_Name, Customer_Friends_count, Customer_Reviews_count,
                               Customer_Photos_count, Customer_Elite, Customer_Elite_Year,  Customer_Rating,
                               Customer_Review, Customer_Review_Date, Customer_Review_Uploaded_Photos,
                               Customer_Review_Useful, Customer_Review_Funny, Customer_Review_Cool,
                               Business_response_By, Business_response_Date,Business_Response_for_Review,
                               Business_Response]

    return Customer_Review_Details


def Customer_Data(link, html_tags, Business_Details, Data_Frame):
    for i in range(0, int(Business_Details[2]), 20):
        #         print(i)
        # initiating the webdriver. Parameter includes the path of the webdriver.
        driver = webdriver.Chrome('C:/Users/Prudhvi/Anaconda3/chromedriver')
        driver.get(link + '?start=' + str(i))
        # this is just to ensure that the page is loaded
        time.sleep(2)
        html = driver.page_source
        driver.quit()
        # Now, we could simply apply bs4 to html variable
        soup = BeautifulSoup(html, "html.parser")
        # Getting the Customer Reviews Div

        try:
            Customer_Reviews_div = soup.find_all('div', class_=html_tags['Reviews_Div'])
        except:
            print("error: The HTML string for Reviews_Div in html_tags Json is not Correct")

        # creating  a Data frame to save data
        Data_Frame = pd.DataFrame(columns=['Business_Name',
                                           'Business_Address',
                                           'Business_ReviewCount',
                                           'Business_Rating',
                                           'Business_Photos_Count',
                                           'Business_Timings',
                                           'Business_Claim_status',
                                           'Customer_Name',
                                           'Customer_Friends_count',
                                           'Customer_Reviews_count',
                                           'Customer_Photos_count',
                                           'Customer_Elite',
                                           'Customer_Elite_Year',
                                           'Customer_Rating',
                                           'Customer_Review',
                                           'Customer_Review_Date',
                                           'Customer_Review_Uploaded_Photos',
                                           'Customer_Review_Useful',
                                           'Customer_Review_Funny',
                                           'Customer_Review_Cool',
                                           'Business_response_By',
                                           'Business_response_Date',
                                           'Business_Response_for_Review',
                                           'Business_Response'])

        for div in Customer_Reviews_div:
            # calling Customer Review Data Function
            Customer_Review_Details = Customer_Review_Data(div, html_tags)
            # writing the Business and Customer Review details to a Data frame
            data = [{'Business_Name': Business_Details[0],
                     'Business_Address': Business_Details[1],
                     'Business_ReviewCount': Business_Details[2],
                     'Business_Rating': Business_Details[3],
                     'Business_Photos_Count': Business_Details[4],
                     'Business_Timings': Business_Details[5],
                     'Business_Claim_status': Business_Details[6],
                     'Customer_Name': Customer_Review_Details[0],
                     'Customer_Friends_count': Customer_Review_Details[1],
                     'Customer_Reviews_count': Customer_Review_Details[2],
                     'Customer_Photos_count': Customer_Review_Details[3],
                     'Customer_Elite': Customer_Review_Details[4],
                     'Customer_Elite_Year': Customer_Review_Details[5],
                     'Customer_Rating': Customer_Review_Details[6],
                     'Customer_Review': Customer_Review_Details[7],
                     'Customer_Review_Date': Customer_Review_Details[8],
                     'Customer_Review_Uploaded_Photos': Customer_Review_Details[9],
                     'Customer_Review_Useful': Customer_Review_Details[10],
                     'Customer_Review_Funny': Customer_Review_Details[11],
                     'Customer_Review_Cool': Customer_Review_Details[12],
                     'Business_response_By': Customer_Review_Details[13],
                     'Business_response_Date': Customer_Review_Details[14],
                     'Business_Response_for_Review': Customer_Review_Details[15],
                     'Business_Response': Customer_Review_Details[16]}]

            # appending data for each review div
            Data_Frame = Data_Frame.append(data, ignore_index=True, sort=False)

        Data_Frame.to_csv('../Data_Business_Reviews/Yelp_Business_Reviews_Seattle_Painters.csv', mode='a', header=False)

    return


def Business_Data(soup, html_tags, link, Data_Frame):
    try:
        # Reading the Business class from soup
        Business_class = soup.find('div', class_=html_tags['B_class'])
    except:
        print("error: The HTML string for B_class in html_tags Json is not Correct")
    try:
        # Business Name
        Business_Name = Business_class.find('h1', class_=html_tags['B_Name']).text
    except:
        print("error: The HTML string for B_Name in html_tags Json is not Correct")

    try:
        # Business Reviews Count
        Business_ReviewCount = (Business_class.find('span', class_=html_tags['B_Review']).text).split()[0]
    except:
        print("error: The HTML string for B_Review in html_tags Json is not Correct")
    try:
        # Business Rating
        Business_Rating = (Business_class.find('div', class_=re.compile(html_tags['B_Rating']))['aria-label']).split()[
            0]
    except:
        print("error: The HTML string for B_Rating in html_tags Json is not Correct")

    ####################################################################################################

    if soup.find_all(html_tags['B_Address']):
        # Business Address
        Business_Address = ''
        for class_ in soup.find_all(html_tags['B_Address']):
            Business_Address += class_.text
    else:
        Business_Address = 'Null'

    if (Business_class.find('span', class_=html_tags['B_photos'])):
        # Business  Photos Count
        Business_Photos_Count = (Business_class.find('span', class_=html_tags['B_photos']).text).split()[1]
    else:
        Business_Photos_Count = 'Null'

    if Business_class.find('span', class_=html_tags['B_Claim']):
        # Business Claimed Status
        Business_Claim_status = (Business_class.find('span', class_=html_tags['B_Claim']).text).strip()
    else:
        Business_Claim_status = 'Null'

    # Business Timings
    if Business_class.find('span', class_=html_tags['B_Timings']):
        Business_Timings = Business_class.find('span', class_=html_tags['B_Timings']).text
    else:
        Business_Timings = 'Null'

    ###################################################################################################
    Business_Details = [Business_Name,
                        Business_Address,
                        Business_ReviewCount,
                        Business_Rating,
                        Business_Photos_Count,
                        Business_Timings,
                        Business_Claim_status]

    #     print(Business_Details)
    # Iterating each page of business to get reviews and customer html_tags
    Customer_Data(link, html_tags, Business_Details, Data_Frame)

    return Business_Details


if __name__ == '__main__':

    # Loading the HTML tags from Data json file
    with open('../Data_HTML_Tags/html_tags.json') as f:
        html_tags = json.load(f)

    # Reading the business links from the CSV and storing into list
    df = pd.read_csv('../Data_Business_URL_Links/Business_links_Painters_Seattle.csv')

    Business_links = df['Business_links']
    print(len(Business_links))
    Business_links = Business_links.tolist()
    # creating  a Data frame to save data
    Data_Frame = pd.DataFrame(columns=['Business_Name', 'Business_Address', 'Business_ReviewCount', 'Business_Rating',
                                       'Business_Photos_Count', 'Business_Timings', 'Business_Claim_status',
                                       'Customer_Name',
                                       'Customer_Friends_count', 'Customer_Reviews_count', 'Customer_Photos_count',
                                       'Customer_Elite',
                                       'Customer_Elite_Year', 'Customer_Rating', 'Customer_Review',
                                       'Customer_Review_Date',
                                       'Customer_Review_Uploaded_Photos', 'Customer_Review_Useful',
                                       'Customer_Review_Funny',
                                       'Customer_Review_Cool', 'Business_response_By', 'Business_response_Date',
                                       'Business_Response_for_Review', 'Business_Response'])

    # Creating a CSV file with headers to save data
    Data_Frame.to_csv('../Data_Business_Reviews/Yelp_Business_Reviews_Seattle_Painters.csv', header=True)

    for i in range(0, len(Business_links), 1):

        link = Business_links[i]
        driver = webdriver.Chrome('C:/Users/Prudhvi/Anaconda3/chromedriver')
        driver.get(link)
        # this is just to ensure that the page is loaded
        time.sleep(2)
        html = driver.page_source
        driver.quit()
        # Now, we could simply apply bs4 to html variable
        soup = BeautifulSoup(html, "html.parser")
        Business_class = soup.find('div', class_=html_tags['B_class'])
        #         Reviwes_check =((Business_class.find('span', class_=html_tags['B_Review']).text).split()[0]).isnumeric()
        #         print((Business_class.find('span', class_=html_tags['B_Review']).text).split()[0])

        Reviews_check = soup.find_all('div', class_=html_tags['Reviews_Div'])
        if Reviews_check:
            print(i, link)
            Business_Data(soup, html_tags, link, Data_Frame)
        else:
            print('No Reviews')
            print(i, link)
        break