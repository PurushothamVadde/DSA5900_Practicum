import glob
import re
import pandas as pd



def Remove_Duplicates(DataFrame, path):
    for fname in glob.glob(path):
        zipcode_value = (re.findall('\d+',fname))
        zipcode_value= ''.join(map(str, zipcode_value))
        df = pd.read_csv(fname)
        df['Zipcode_searched'] = ''
        df.loc[0:,'Zipcode_searched'] = zipcode_value
        DataFrame = DataFrame.append(df, ignore_index=True)

    # Dropping the Duplicate values:
    print("The length of Data frame with Duplicate URL :",len(DataFrame))
    DataFrame = DataFrame.drop_duplicates(subset="Business_links")
    print('The length of DataFrame after droping the Duplicates :', len(DataFrame))

    DataFrame.to_csv('Business_links_Plumbing_0k.csv')

    # Count of URL by Zipcode
    URL_count = DataFrame.groupby(by=["Zipcode_searched"]).count()
    URL_count.to_csv('Business_links_count_by_Zipcode.csv')

    return 0

if __name__ == '__main__':
    DataFrame = pd.DataFrame()
    path = 'Businesslinks_with_zipcode/Business_links*.csv'

    Remove_Duplicates(DataFrame, path)