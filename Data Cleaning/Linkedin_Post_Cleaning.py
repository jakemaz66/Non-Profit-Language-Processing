import pandas as pd
import string

#Reading in Data
df_linkedin = pd.read_excel(r'C:\Users\jakem\Non-Profit-Language-Processing\Raw Data Files\bethlehem-haven_content_LinkedInData_01_23__01_24 (1).xls',
                            sheet_name='All posts')

def display(df: pd.DataFrame):
    """
    Takes in a dataframe and displays it

    Args:
    A Pandas Dataframe
    
    """
    print(df.head())
    print(df.columns)
    print(df.shape)

def count_punctuation(text):
    """
    This function takes in text and returns the number of punctuation marks

    Args:
    text: a string
    
    """
    return sum(1 for char in text if char in string.punctuation)

def count_hashtags(text):
    """
    This function takes in text and returns the number of hashtags

    Args:
    text: a string
    
    """
    return sum(1 for char in text if char in ['#'])

#Renaming columns
df_linkedin.columns = ['Posts', 'Post Link', 'Post Type', 'Campaign name', 'Posted by',
                       'Created date', 'Campaign start date', 'Campaign end date', 'Audience',
                       'Impressions', 'Views (Excluding offsite video views)', 'Offsite Views',
                       'Clicks', 'Click through rate (CTR)', 'Likes', 'Comments', 'Reposts',
                       'Follows', 'Engagement rate', 'Content Type']

#Getting rid of existing headers
df_linkedin = df_linkedin.iloc[1:, :]

#Subsetting columns of interest
linked_in_interest = df_linkedin[['Posts', 'Impressions', 'Likes', 'Comments', 'Reposts']]

display(linked_in_interest)

#Adding Feature Columns
linked_in_interest['Post Length'] = linked_in_interest['Posts'].apply(lambda x: len(x))
linked_in_interest['Punctuation_Count'] = linked_in_interest['Posts'].apply(count_punctuation)
linked_in_interest['Hashtag_Count'] = linked_in_interest['Posts'].apply(count_hashtags)


#Exporting to File
excel_filename = 'Cleaned LinkedIn Data.xlsx'
linked_in_interest.to_excel(excel_filename)



