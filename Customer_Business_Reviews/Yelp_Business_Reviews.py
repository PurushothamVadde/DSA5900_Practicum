from bs4 import BeautifulSoup
import re
import pandas as pd
import time
from selenium import webdriver
import json

####################Function to Get Customer Reviews#############################
def Customer_Review_Data(Review_div, Data):
    # Intializing the customer features
    Customer_Friends_count = 0
    Customer_Reviews_count = 0
    Customer_Photos_count = 0

    # Customer Name
    try:
        Customer_Name = Review_div.find('div', class_=Data['C_Name']).text
    except:
        print("error: The HTML string for C_Name in Data Json is not Correct")

    try:
        # Customer Data like friends reviews photos
        Customer_data = Review_div.find('div', class_=Data['C_Data'])
        for i in Customer_data.find_all('div'):
            if (i['aria-label']) == 'Friends':
                Customer_Friends_count = i.text
            if (i['aria-label']) == 'Reviews':
                Customer_Reviews_count = i.text
            if (i['aria-label']) == 'Photos':
                Customer_Photos_count = i.text
    except:
        print("error: The HTML string for C_Data in Data Json is not Correct")

    try:
        # Customer Rating For Restaurant
        Customer_Rating = (Review_div.find('div', class_=re.compile(Data['C_Rating']))['aria-label']).split()[0]
    except:
        print("error: The HTML string for C_Rating in Data Json is not Correct")

    try:
        # Customer Review
        Customer_Review = Review_div.find('p', class_=Data['C_Review']).text
    except:
        print("error: The HTML string for C_Review in Data Json is not Correct")

    try:
        # Customer Review Date
        Customer_Review_Date = Review_div.find('div', class_=Data['C_R_Date']).text
    except:
        print("error: The HTML string for C_R_Date in Data Json is not Correct")

    try:
        # Like Categories
        likes_class = Review_div.find('div', class_=Data['Like_class'])

        Temp_emoji = []
        for span in likes_class.find_all('span', class_=Data['Like_Category']):
            if (len((span.text).split()) > 1):
                Temp_emoji.append((span.text).split()[1])
            else:
                Temp_emoji.append(0)

        Customer_Review_Useful = Temp_emoji[0]
        Customer_Review_Funny = Temp_emoji[1]
        Customer_Review_Cool = Temp_emoji[2]
    except:
        print("error: The HTML string for Like_class/Like_Category in Data Json is not Correct")

    #######################################################################################################
    # Customer Uploaded photos
    if (Review_div.find('span', class_=Data['C_R_Photos'])):
        Customer_Review_Uploaded_Photos = (Review_div.find('span', class_=Data['C_R_Photos']).text.split()[0])
    else:
        Customer_Review_Uploaded_Photos = 0

    # Is Customer in Elite Group
    if Review_div.find('p', class_=Data['C_Elite']):
        Customer_Elite = 'Yes'
        Customer_Elite_Year = (Review_div.find('p', class_=Data['C_Elite'])).text.split()[1]
    else:
        Customer_Elite = 'No'
        Customer_Elite_Year = '0'

        # Business Response class
    if Review_div.find('div', class_=Data['B_R_Class']):
        Business_response_class = Review_div.find('div', class_=Data['B_R_Class'])
        if Business_response_class.find('div', class_=Data['B_R_Check']):
            # Business Response by
            Business_response_By = (Business_response_class.find('p', class_=Data['B_R_by'])).text
            # Business Response date
            Business_response_Date = (Business_response_class.find('p', class_=Data['B_R_Date'])).text
            # Business  Response
            if Business_response_class.find('p', class_=Data['B_Response']):
                Business_Response_for_Review = (Business_response_class.find('p', class_=Data['B_Response'])).text
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
    Customer_Review_Details = [Customer_Name,
                               Customer_Friends_count,
                               Customer_Reviews_count,
                               Customer_Photos_count,
                               Customer_Elite,
                               Customer_Elite_Year,
                               Customer_Rating,
                               Customer_Review,
                               Customer_Review_Date,
                               Customer_Review_Uploaded_Photos,
                               Customer_Review_Useful,
                               Customer_Review_Funny,
                               Customer_Review_Cool,
                               Business_response_By,
                               Business_response_Date,
                               Business_Response_for_Review,
                               Business_Response]
    return Customer_Review_Details

# Function to Get Customer Data

def Customer_Data(link, Data, Business_Details, Data_Frame):
    for i in range(0, int(40), 20):
        print(i)
        # initiating the webdriver. Parameter includes the path of the webdriver.
        driver = webdriver.Chrome('C:/Users/Prudhvi/Anaconda3/chromedriver')
        driver.get(link + '?start=' + str(i))
        # this is just to ensure that the page is loaded
        time.sleep(3)
        html = driver.page_source
        driver.quit()
        # Now, we could simply apply bs4 to html variable
        soup = BeautifulSoup(html, "html.parser")
        # Getting the Customer Reviews Div

        try:
            Customer_Reviews_div = soup.find_all('div', class_=Data['Reviews_Div'])
        except:
            print("error: The HTML string for Reviews_Div in Data Json is not Correct")

        # creating  a Data frame to save data
        Data_Frame = pd.DataFrame(columns=['Restaurant_Name', 'Restaurant_Address', 'Restaurant_ReviewCount',
                                           'Restaurant_Rating', 'Restaurant_Photos_Count', 'Restaurant_Timings',
                                           'Restaurant_Claim_status', 'Restaurant_Dollars', 'Restaurant_Food_Type',
                                           'Restaurant_Delivery_price', 'Restaurant_Delivey_Time',
                                           'Customer_Name', 'Customer_Friends_count', 'Customer_Reviews_count',
                                           'Customer_Photos_count', 'Customer_Elite', 'Customer_Elite_Year',
                                           'Customer_Rating', 'Customer_Review', 'Customer_Review_Date',
                                           'Customer_Review_Uploaded_Photos', 'Customer_Review_Useful',
                                           'Customer_Review_Funny', 'Customer_Review_Cool', 'Business_response_By',
                                           'Business_response_Date', 'Business_Response_for_Review',
                                           'Business_Response'])

        for div in Customer_Reviews_div:
            # calling Customer Review Data Function
            Customer_Review_Details = Customer_Review_Data(div, Data)
            # writing the Business and Customer Review details to a Data frame
            data = [{'Restaurant_Name': Business_Details[0],
                     'Restaurant_Address': Business_Details[1],
                     'Restaurant_ReviewCount': Business_Details[2],
                     'Restaurant_Rating': Business_Details[3],
                     'Restaurant_Photos_Count': Business_Details[4],
                     'Restaurant_Timings': Business_Details[5],
                     'Restaurant_Claim_status': Business_Details[6],
                     'Restaurant_Dollars': Business_Details[7],
                     'Restaurant_Food_Type': Business_Details[8],
                     'Restaurant_Delivery_price': Business_Details[9],
                     'Restaurant_Delivey_Time': Business_Details[10],
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

        Data_Frame.to_csv('Yelp_Business_Reviews.csv', mode='a', header=False)
    return

# Function to get Resturant Data

def Restaurant_Data(soup, Data, link, Data_Frame):
    try:
        # Reading the Restaurant class from soup
        Restaurant_class = soup.find('div', class_=Data['R_class'])
    except:
        print("error: The HTML string for R_class in Data Json is not Correct")
    try:
        # Restaurant Name
        Restaurant_Name = Restaurant_class.find('h1', class_=Data['R_Name']).text
    except:
        print("error: The HTML string for R_Name in Data Json is not Correct")

    try:
        # Restaurant Reviews Count
        Restaurant_ReviewCount = (Restaurant_class.find('span', class_=Data['R_Review']).text).split()[0]
    except:
        print("error: The HTML string for R_Review in Data Json is not Correct")
    try:
        # Restaurant Rating
        Restaurant_Rating = (Restaurant_class.find('div', class_=re.compile(Data['R_Rating']))['aria-label']).split()[0]
    except:
        print("error: The HTML string for R_Rating in Data Json is not Correct")

    ####################################################################################################

    if soup.find_all(Data['R_Address']):
        # Restaurant Address
        Restaurant_Address = ''
        for class_ in soup.find_all(Data['R_Address']):
            Restaurant_Address += class_.text
    else:
        Restaurant_Address = 'Null'

    if (Restaurant_class.find('span', class_=Data['R_photos'])):
        # Restaurant  Photos Count
        Restaurant_Photos_Count = (Restaurant_class.find('span', class_=Data['R_photos']).text).split()[1]
    else:
        Restaurant_Photos_Count = 'Null'

    if Restaurant_class.find('span', class_=Data['R_Claim']):
        # Restaurant Claimed Status
        Restaurant_Claim_status = (Restaurant_class.find('span', class_=Data['R_Claim']).text).strip()
    else:
        Restaurant_Claim_status = 'Null'

    if (Restaurant_class.find('a', class_=Data['R_Food_type'])):
        # Restaurant Food Type
        Restaurant_Food_Type = Restaurant_class.find('a', class_=Data['R_Food_type']).text
    else:
        Restaurant_Food_Type = 'Null'

    # Restaurant Dollar
    if Restaurant_class.find('span', class_=Data['R_Dollar']):
        Restaurant_Dollars = (Restaurant_class.find('span', class_=Data['R_Dollar']).text).strip()
    else:
        Restaurant_Dollars = 'Null'

    # Restaurant Timings
    if Restaurant_class.find('span', class_=Data['R_Timings']):
        Restaurant_Timings = Restaurant_class.find('span', class_=Data['R_Timings']).text
    else:
        Restaurant_Timings = 'Null'

    # Restaurant Delivery Price and Time
    if soup.find('div', id=Data['R_Delivery_class']):
        Delivery_class = soup.find('div', id=Data['R_Delivery_class'])
        if (Delivery_class.find('div', class_=Data['R_Delivery_Price'])):
            Restaurant_Delivery_price = (Delivery_class.find('div', class_=Data['R_Delivery_Price']).text).split()[0]
        else:
            Restaurant_Delivery_price = 'Null'
        if (Delivery_class.find('div', class_=Data['R_Delivery_Time'])):
            Restaurant_Delivey_Time = (Delivery_class.find('div', class_=Data['R_Delivery_Time']).text)
        else:
            Restaurant_Delivey_Time = 'Null'
    else:
        Restaurant_Delivery_price = 'Null'
        Restaurant_Delivey_Time = 'Null'

        ###################################################################################################
    Business_Details = [Restaurant_Name,
                        Restaurant_Address,
                        Restaurant_ReviewCount,
                        Restaurant_Rating,
                        Restaurant_Photos_Count,
                        Restaurant_Timings,
                        Restaurant_Claim_status,
                        Restaurant_Dollars,
                        Restaurant_Food_Type,
                        Restaurant_Delivery_price,
                        Restaurant_Delivey_Time]

    # Iterating each page of business to get reviews and customer data
    Customer_Data(link, Data, Business_Details, Data_Frame)

    return Business_Details
################################################################################################

# Loading the HTML tags from Data json file
with open('Data.json') as f:
    Data = json.load(f)

# Reading the business links from the CSV and storing into list
df = pd.read_csv('Business_links.csv')
Business_links = df['Business_links']
Business_links = Business_links.tolist()
# Business_links


# creating  a Data frame to save data
Data_Frame = pd.DataFrame(columns=['Restaurant_Name', 'Restaurant_Address', 'Restaurant_ReviewCount',
                                   'Restaurant_Rating', 'Restaurant_Photos_Count', 'Restaurant_Timings',
                                   'Restaurant_Claim_status', 'Restaurant_Dollars', 'Restaurant_Food_Type',
                                   'Restaurant_Delivery_price', 'Restaurant_Delivey_Time',
                                   'Customer_Name', 'Customer_Friends_count', 'Customer_Reviews_count',
                                   'Customer_Photos_count', 'Customer_Elite', 'Customer_Elite_Year',
                                   'Customer_Rating', 'Customer_Review', 'Customer_Review_Date',
                                   'Customer_Review_Uploaded_Photos', 'Customer_Review_Useful',
                                   'Customer_Review_Funny','Customer_Review_Cool', 'Business_response_By',
                                   'Business_response_Date','Business_Response_for_Review', 'Business_Response'])
# Creating a CSV file with headers to save data
Data_Frame.to_csv('Yelp_Business_Reviews.csv', header=True)


i=0
for link in Business_links:
    # yelp URL
#     restarant_url = 'https://www.yelp.com/biz/skillet-capitol-hill-seattle-2?osq=Restaurants&start=360'

    # initiating the webdriver. Parameter includes the path of the webdriver.
    driver = webdriver.Chrome('C:/Users/Prudhvi/Anaconda3/chromedriver')
    driver.get(link)
    # this is just to ensure that the page is loaded
    time.sleep(10)
    html = driver.page_source
    driver.quit()
    # Now, we could simply apply bs4 to html variable
    soup = BeautifulSoup(html, "html.parser")
    Restaurant_Data(soup,Data,link,Data_Frame)
    i+=1
    if i== 1:
        break