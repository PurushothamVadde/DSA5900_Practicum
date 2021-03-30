from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
import json

def Business_Has_Reviews():
    # Loading the HTML tags from Data json file
    with open('html_tags.json') as f:
        html_tags = json.load(f)

    df = pd.read_csv('Business_links_Plumbing_0k.csv')
    links = df['Business_links']
    links.tolist()

    for i in range(0, len(links), 1):
        URL = links[i]
        print(i, links[i])
        driver = webdriver.Chrome('C:/Users/Prudhvi/Anaconda3/chromedriver')
        driver.get(URL)
        # this is just to ensure that the page is loaded
        time.sleep(5)
        html = driver.page_source
        driver.quit()
        # Now, we could simply apply bs4 to html variable
        soup = BeautifulSoup(html, "html.parser")
        Business_class = soup.find('div', class_=html_tags['B_class'])
        if (Business_class.find('button', class_="css-1gu7rbt")):
            Business_ReviewCount = (Business_class.find('span', class_=html_tags['B_Review']).text).split()[0]
            print(Business_ReviewCount)
            df.at[i, 'Has_reviews'] = 'Yes'
        else:
            df.at[i, 'Has_reviews'] = 'No'
            print('no reviews')

        if soup.find_all(html_tags['B_Address']):
            # Business Address
            Business_Address = ''
            for class_ in soup.find_all(html_tags['B_Address']):
                Business_Address += class_.text
        else:
            Business_Address = 'Null'
        # print(Business_Address.split()[-1])
        df.at[i, 'Actual_Zipcode'] = Business_Address.split()[-1]

    df.to_csv('Business_links_Final.csv')

    return 0

if __name__ == '__main__':
    Business_Has_Reviews()