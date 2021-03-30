# !pip install selenium
import pandas as pd
import urllib
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
from urllib.parse import urlparse
import time


######################################################### Zipcodes######################################################
# Change the Zip Codes based on City 75

# zipcodes = [73101, 73102, 73103, 73104, 73105, 73106, 73107, 73108, 73109, 73110,
#            73111, 73112, 73113, 73114, 73115, 73116, 73117, 73118, 73119, 73120, 
#            73121, 73122, 73123, 73124, 73125, 73126, 73127, 73128, 73129, 73130,
#            73131, 73132, 73134, 73135, 73136, 73137, 73139, 73140, 73141, 73142,
#            73143, 73144, 73145, 73146, 73147, 73148, 73149, 73150, 73151, 73152,
#            73153, 73154, 73155, 73156, 73157, 73159, 73160, 73162, 73163, 73164,
#            73165, 73167, 73169, 73170, 73172, 73173, 73178, 73179, 73184, 73185,
#            73189, 73190, 73194, 73195, 73196]

# seattle Zipcodes 59

zipcodes = [98101, 98102, 98103, 98104, 98105, 98106, 98107, 98108, 98109, 98111,
            98112, 98113, 98114, 98115, 98116, 98117, 98118, 98119, 98121, 98122,
            98124, 98125, 98126, 98127, 98129, 98131, 98133, 98134, 98136, 98138,
            98139, 98141, 98144, 98145, 98146, 98148, 98154, 98155, 98158, 98160,
            98161, 98164, 98165, 98166, 98168, 98170, 98174, 98175, 98177, 98178,
            98181, 98185, 98188, 98190, 98191, 98194, 98195, 98198, 98199]


#Los Angeles Zipcode 94

# zipcodes = [90001, 90002, 90003, 90004, 90005, 90006, 90007, 90008, 90009, 90010, 
#             90011, 90012, 90013, 90014, 90015, 90016, 90017, 90018, 90019, 90020, 
#             90021, 90022, 90023, 90024, 90025, 90026, 90027, 90028, 90029, 90030,
#             90031, 90032, 90033, 90034, 90035, 90036, 90037, 90038, 90039, 90040,
#             90041, 90042, 90043, 90044, 90045, 90046, 90047, 90048, 90049, 90050,
#             90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058, 90059, 90060, 
#             90061, 90062, 90063, 90064, 90065, 90066, 90067, 90068, 90070, 90071, 
#             90072, 90073, 90074, 90075, 90076, 90077, 90078, 90079, 90080, 90081, 
#             90082, 90083, 90084, 90086, 90087, 90088, 90089, 90091, 90093, 90095, 
#             90096, 90099, 90134, 90189]


# Newyork Zipcodes 146

# zipcodes = [ 10001, 10002, 10003, 10004, 10005, 10006, 10007, 10008, 10009, 10010,
#              10011, 10012, 10013, 10014, 10016, 10017, 10018, 10019, 10020, 10021,
#              10022, 10023, 10024, 10025, 10026, 10027, 10028, 10029, 10030, 10031,
#              10032, 10033, 10034, 10035, 10036, 10037, 10038, 10039, 10040, 10041,
#              10043, 10044, 10045, 10055, 10060, 10065, 10069, 10075, 10080, 10081, 
#              10087, 10090, 10101, 10102, 10103, 10104, 10105, 10106, 10107, 10108,
#              10109, 10110, 10111, 10112, 10113, 10114, 10115, 10116, 10117, 10118,
#              10119, 10120, 10121, 10122, 10123, 10124, 10125, 10126, 10128, 10129, 
#              10130, 10131, 10132, 10133, 10138, 10150, 10151, 10152, 10153, 10154,
#              10155, 10156, 10157, 10158, 10159, 10160, 10161, 10162, 10163, 10164,
#              10165, 10166, 10167, 10168, 10169, 10170, 10171, 10172, 10173, 10174,
#              10175, 10176, 10177, 10178, 10179, 10185, 10199, 10203, 10211, 10212, 
#              10213, 10242, 10249, 10256, 10258, 10259, 10260, 10261, 10265, 10268, 
#              10269, 10270, 10271, 10272, 10273, 10274, 10275, 10276, 10277, 10278,
#              10279, 10280, 10281, 10282, 10285, 10286]

# Miami Zipcodes 95
# zipcodes =  [33101, 33102, 33106, 33111, 33112, 33116, 33122, 33124, 33125, 33126,
#              33127, 33128, 33129, 33130, 33131, 33132, 33133, 33134, 33135, 33136, 
#              33137, 33138, 33142, 33143, 33144, 33145, 33146, 33147, 33150, 33151, 
#              33152, 33153, 33155, 33156, 33157, 33158, 33161, 33162, 33163, 33164, 
#              33165, 33166, 33167, 33168, 33169, 33170, 33172, 33173, 33174, 33175, 
#              33176, 33177, 33178, 33179, 33180, 33181, 33182, 33183, 33184, 33185, 
#              33186, 33187, 33188, 33189, 33190, 33191, 33192, 33193, 33194, 33195,
#              33196, 33197, 33198, 33199, 33206, 33222, 33231, 33233, 33234, 33238, 
#              33242, 33243, 33245, 33247, 33255, 33256, 33257, 33261, 33265, 33266,
#              33269, 33280, 33283, 33296, 33299]

# Palm Beach  22
# zipcodes = [33401, 33402, 33403, 33404, 33405, 33406, 33407, 33409, 33411, 33412, 
#             33413, 33415, 33416, 33417, 33419, 33420, 33422, 33408, 33410, 33418,
#             33421, 33480]


# Returns the URL list where each element is a result of search operation based on Category and Zipcode 
# Example : URL for search operation in the yelp page by category(plumbing) and zipcode as 73071

def Extracting_Yelp_Main_URl_By_Zipcodes(zipcodes):
    zipcode_URL = []
    for i in zipcodes:
#         zipcode_URL.append(f'https://www.yelp.com/search?find_desc=plumbing&find_loc={i}&start=0')
#         zipcode_URL.append(f'https://www.yelp.com/search?find_desc=HVAC&find_loc={i}&start=0')
        zipcode_URL.append(f'https://www.yelp.com/search?find_desc=Painters&find_loc={i}&start=0')
#         zipcode_URL.append(f'https://www.yelp.com/search?find_desc=Landscaping&find_loc={i}&start=0')
#         zipcode_URL.append(f'https://www.yelp.com/search?find_desc=autorepair&find_loc={i}&start=0')
#         zipcode_URL.append(f'https://www.yelp.com/search?find_desc=Tires&find_loc={i}&start=0')
#         zipcode_URL.append(f'https://www.yelp.com/search?find_desc=Transmission%20Repair&find_loc={i}&start=0')
#         zipcode_URL.append(f'https://www.yelp.com/search?find_desc=contractors&find_loc={i}&start=0')
#         zipcode_URL.append(f'https://www.yelp.com/search?find_desc=electricians&find_loc={i}&start=0')
#         zipcode_URL.append(f'https://www.yelp.com/search?find_desc=Flooring&find_loc={i}&start=0')
#         zipcode_URL.append(f'https://www.yelp.com/search?find_desc=Handyman&find_loc={i}&start=0')
    return zipcode_URL


# Function to extract the URL of pages
def Extracting_URL(main_url, links):
    URL = main_url
    # initiating the webdriver. Parameter includes the path of the webdriver.
    driver = webdriver.Chrome('C:/Users/Prudhvi/Anaconda3/chromedriver')
    # time.sleep(5)
    driver.get(URL)
    # this is just to ensure that the page is loaded
#     time.sleep(3)
    html = driver.page_source
    driver.quit()
    # Now, we could simply apply bs4 to html variable
    soup = BeautifulSoup(html, "html.parser")
    tags = soup('a', href=True)
    for tag in tags:
        if "start" in tag["href"]:
#             print(tag['href'])
            if ('www.yelp.com/search?find_desc=' in tag['href'] ) and (tag['href'] not in links) and ('login' not in tag['href']) and ('signup'not in tag['href'])and ('biz' not in tag['href']):
            # if (tag['href'] not in links) and ('login' not in tag['href']) and ('signup'not in tag['href']) and ('biz' not in tag['href']):
#                 print(tag['href'])
                links.append(tag['href'])
    return links

# and (base_url + tag['href'] not in Business_links
def Extracting_Business_URL(main_url, base_url, Business_links):
    URL = main_url
    # initiating the webdriver. Parameter includes the path of the webdriver.
    driver = webdriver.Chrome('C:/Users/Prudhvi/Anaconda3/chromedriver')
#     time.sleep(2)
    driver.get(URL)
    # this is just to ensure that the page is loaded
#     time.sleep(3)
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all("a", class_="css-166la90")
    #     print(tags)
    for tag in tags:
        if ("osq" in tag["href"]) :
            Business_links.append(base_url + tag['href'])

    return Business_links


def main(base_url,main_url,counter):
    # list to store the links of pages with business list
    links = []
    # list to store the list of business url
    Business_links = []
    # Extracting all page urls with business list
    for i in range(1, 6):
        links = Extracting_URL(main_url, links)
        url = links[-1]
        main_url = url    
    # Extracting all Business URL from all pages
    for link in links:
        Business_links=Extracting_Business_URL(link, base_url, Business_links)
    # Saving all the Business URL to csv file
    df = pd.DataFrame({'Business_links': Business_links})
    df.to_csv(f'../Data_Business_URL_City_and_Category_Wise/Seattle/Painters/Business_links{counter}.csv')
    print(len(Business_links))
    return Business_links
    


if __name__== '__main__':
    

    print("starting time:", time.localtime(time.time()))
    zipcode_URL = Extracting_Yelp_Main_URl_By_Zipcodes(zipcodes)
    print(len(zipcode_URL))
    
    for i in range(0,len(zipcode_URL),1):
        try:
            start_time = time.clock()
            # main_url is the intial search page url with results based on category and zipcode
            main_url = zipcode_URL[i]
            parse = urlparse(main_url)
            main_url= parse.geturl()
            # Base yelp url
            print(i,main_url)
            base_url = 'https://www.yelp.com'
            main(base_url,main_url,i)
            print (time.clock() - start_time, "seconds")
        # break
        except:
            print('failed URL')
            print(i,main_url)
            pass
  