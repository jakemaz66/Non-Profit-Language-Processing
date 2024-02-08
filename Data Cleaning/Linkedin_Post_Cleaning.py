import pandas as pd

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

#Exporting to File
excel_filename = 'Cleaned LinkedIn Data.xlsx'
linked_in_interest.to_excel(excel_filename)



