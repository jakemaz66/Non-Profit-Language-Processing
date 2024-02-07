#Importing Libraries
import pandas as pd
import json

#Defining file path to JSON Data
file_path = r'C:\Users\jakem\Non-Profit-Language-Processing\Raw Data Files\reels.json'

#Reading in data
with open(file_path, 'r') as file:
    data = json.load(file)


#Collecting Titles from data and storing in list
titles = []
for dictionary in data['organic_insights_reels']:
    titles.append((dictionary['media_map_data']['Media Thumbnail']['title']))

#Defining rest of feature lists
Upload_Timestamp = []
Duration = []
accounts_reached = []
Instagram_Plays = []
Instagram_Likes = []
Instagram_Comments = []
Instagram_Shares= []
Instagram_Saves = []
interest_topics = []

def collect(data=data) -> pd.DataFrame:
    """
    This function takes in a list of dictionaries in json format (default is data)

    Args:
    data is the json data source

    Returns:
    A pandas dataframe
    """
    for dictionary in data['organic_insights_reels']:
        Upload_Timestamp.append((dictionary['string_map_data']['Upload Timestamp']['timestamp']))

        Duration.append((dictionary['string_map_data']['Duration']['value']))

        accounts_reached.append((dictionary['string_map_data']['Accounts reached']['value']))

        Instagram_Plays.append((dictionary['string_map_data']['Instagram Plays']['value']))

        Instagram_Likes.append((dictionary['string_map_data']['Instagram Likes']['value']))

        Instagram_Comments.append((dictionary['string_map_data']['Instagram Comments']['value']))

        Instagram_Shares.append((dictionary['string_map_data']['Instagram Shares']['value']))

        Instagram_Saves.append((dictionary['string_map_data']['Instagram Saves']['value']))


        if 'interest_topics' in dictionary['media_map_data']['Media Thumbnail']:
            interest_topics.append((dictionary['media_map_data']['Media Thumbnail']['interest_topics']))
        else:
            interest_topics.append('No Topics')

    return pd.DataFrame({'Post Title': titles, 'Duration': Duration, 'Plays': Instagram_Plays,
                    'Accounts Reached': accounts_reached, 'Saves': Instagram_Saves, 'Likes': Instagram_Likes, 'Comments': Instagram_Comments,
                    'Shares': Instagram_Shares, 'Timestamp': Upload_Timestamp, 'Interest Topics':interest_topics })

#Getting dataframe from collect
df = collect(data)

#Converting to Excel File
excel_filename = 'Cleaned Reels Data.xlsx'
df.to_excel(excel_filename)