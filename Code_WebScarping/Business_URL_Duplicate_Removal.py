import glob
import re
import pandas as pd

def Remove_Duplicates(DataFrame, path, city, category):
    for fname in glob.glob(path):
        df = pd.read_csv(fname)
        DataFrame = DataFrame.append(df, ignore_index=True)

    # Dropping the Duplicate values:
    print("The length of Data frame with Duplicate URL :",len(DataFrame))
    DataFrame = DataFrame.drop_duplicates(subset="Business_links")
    print('The length of DataFrame after droping the Duplicates :', len(DataFrame))

    DataFrame.to_csv('../Data_Business_URL_Links/Business_links_{0}_{1}.csv'.format(category, city))

    return 0

if __name__ == '__main__':
    
    #####################################Input Data#############################################   
    # Reading the input data city and category from json file
    with open('../Data_HTML_Tags/Input.json') as f:
        Input_data = json.load(f)
    
    city = Input_data['city']
    category = Input_data['category']
    
    
    DataFrame = pd.DataFrame()
    path = '../Data_Business_URL_City_and_Category_Wise/{0}/{1}/Business_links_*.csv'.format(city,category)

    Remove_Duplicates(DataFrame, path, city, category)