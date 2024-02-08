#Importing Libraries
import pandas as pd
import json
import string

#Defining file path to JSON Data
file_path = r'C:\Users\jakem\Non-Profit-Language-Processing\Raw Data Files\posts.json'

#Reading in data
with open(file_path, 'r') as file:
    data = json.load(file)

#Collecting Titles from data and storing in list
titles = []
for dictionary in data['organic_insights_posts']:
    titles.append((dictionary['media_map_data']['Media Thumbnail']['title']))

#Defining rest of feature lists
profile_visits = []
impressions_visits = []
accounts_reached = []
saves = []
likes = []
comments = []
shares = []
timestamp = []

def collect(data=data) -> pd.DataFrame:
    """
    This function takes in a list of dictionaries in json format (default is data)

    Args:
    data is the json data source

    Returns:
    A pandas dataframe
    """
    for dictionary in data['organic_insights_posts']:
        profile_visits.append((dictionary['string_map_data']['Profile Visits']['value']))

        impressions_visits.append((dictionary['string_map_data']['Impressions']['value']))

        accounts_reached.append((dictionary['string_map_data']['Accounts reached']['value']))

        saves.append((dictionary['string_map_data']['Saves']['value']))

        likes.append((dictionary['string_map_data']['Likes']['value']))

        comments.append((dictionary['string_map_data']['Comments']['value']))

        shares.append((dictionary['string_map_data']['Shares']['value']))

        timestamp.append((dictionary['media_map_data']['Media Thumbnail']['creation_timestamp']))

    return pd.DataFrame({'Post Title': titles, 'Profile Visits': profile_visits, 'Impressions': impressions_visits,
                    'Accounts Reached': accounts_reached, 'Saves': saves, 'Likes': likes, 'Comments': comments,
                    'Shares': shares, 'Timestamp': timestamp})


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

#Calling collect function to get dataframe
df = collect(data)

#Adding Feature Columns
df['Post Length'] = df['Post Title'].apply(lambda x: len(x))
df['Punctuation_Count'] = df['Post Title'].apply(count_punctuation)
df['Hashtag_Count'] = df['Post Title'].apply(count_hashtags)

#Converting to Excel File
file_name = 'CleanedPosts.xlsx'
df.to_excel(file_name)
