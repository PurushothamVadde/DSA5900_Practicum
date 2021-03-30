import glob
import re
import pandas as pd

def Remove_Duplicates(DataFrame, path):
    for fname in glob.glob(path):
        df = pd.read_csv(fname)
        DataFrame = DataFrame.append(df, ignore_index=True)
    # Dropping the Duplicate values:
    print("The length of Data frame with Duplicate URL :",len(DataFrame))
    DataFrame = DataFrame.drop_duplicates(subset="Business_links")
    print('The length of DataFrame after droping the Duplicates :', len(DataFrame))
    DataFrame.to_csv('../Data_Business_URL_Links/Business_links_Painters_Seattle.csv')
    return 0

if __name__ == '__main__':
    DataFrame = pd.DataFrame()
    path = '../Data_Business_URL_City_and_Category_Wise/Seattle/Painters/Business_links*.csv'
    Remove_Duplicates(DataFrame, path)