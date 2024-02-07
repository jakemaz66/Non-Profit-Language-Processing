#Importing Libraries
import pandas as pd
import json

file_path = r"C:\Users\jakem\Downloads\posts.json"

with open(file_path, 'r') as file:
    data = json.load(file)

data['organic_insights_posts']

titles = []

for dictionary in data['organic_insights_posts']:
  print(dictionary)
    #if 'title' in dictionary:
     # titles.append(dictionary['title'])

titles = []


for dictionary in data['organic_insights_posts']:
    titles.append((dictionary['media_map_data']['Media Thumbnail']['title']))

profile_visits = []
impressions_visits = []
accounts_reached = []
saves = []
likes = []
comments = []
shares = []
timestamp = []

for dictionary in data['organic_insights_posts']:
    profile_visits.append((dictionary['string_map_data']['Profile Visits']['value']))

    impressions_visits.append((dictionary['string_map_data']['Impressions']['value']))

    accounts_reached.append((dictionary['string_map_data']['Accounts reached']['value']))

    saves.append((dictionary['string_map_data']['Saves']['value']))

    likes.append((dictionary['string_map_data']['Likes']['value']))

    comments.append((dictionary['string_map_data']['Comments']['value']))

    shares.append((dictionary['string_map_data']['Shares']['value']))

    timestamp.append((dictionary['media_map_data']['Media Thumbnail']['creation_timestamp']))

df = pd.DataFrame({'Post Title': titles, 'Profile Visits': profile_visits, 'Impressions': impressions_visits,
                   'Accounts Reached': accounts_reached, 'Saves': saves, 'Likes': likes, 'Comments': comments,
                   'Shares': shares, 'Timestamp': timestamp})


excel_filename = 'Cleaned Post Data.xlsx'
df.to_excel(excel_filename)