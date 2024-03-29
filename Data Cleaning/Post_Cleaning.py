#Importing Libraries
import pandas as pd
import json
import string
import time
import datetime
import emoji
import spacy


def collect(data) -> pd.DataFrame:
    """
    This function takes in a list of dictionaries in json format (default is data)

    Args:
    data is the json data source

    Returns:
    A pandas dataframe
    
    """
    #Defining file path to JSON Data
    file_path = r'C:\Users\jakem\Non-Profit-Language-Processing\Data Cleaning\data\Raw Data Files\posts.json'

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

def count_exclam(text):
    """
    This function takes in text and returns the number of exclamation marks

    Args:
    text: a string
    
    """
    return sum(1 for char in text if char == '!')

def count_hashtags(text):
    """
    This function takes in text and returns the number of hashtags

    Args:
    text: a string
    
    """
    return sum(1 for char in text if char in ['#'])

#Adding Sentence Length Column
def split_sent(col):
    """
    This function takes in a string and returns the average length per sentence of the entire string

    Args:
    col -> a string column
    """
    sentences = col.replace('!', '.').replace('?', '.').split('.')
    sentences = [s.strip() for s in sentences if s.strip()]  
    total_length = sum(len(sentence.split()) for sentence in sentences)
    
    if len(sentences) > 0:
        average_length = total_length / len(sentences)
        return average_length
    else:
        return 0  

#Function to detect emojis (so they will not be counted in the mistakes)
def is_emoji(word):
    """
    This function takes in a string and returns the number of emojis

    Args:
    word -> a string
    """
    return sum(1 for character in word if emoji.is_emoji(character))

#Part of Speech Tagging
#spacy.cli.download("en_core_web_lg")
nlp = spacy.load('en_core_web_lg')

def count_adjectives(col):
    """
    This function takes in a column and returns the number of adjectives in that column value

    Args:
    col -> column of a pandas dataframe
    """
    words = nlp(col)

    adjectives = [nlp.token.text for nlp.token in words if nlp.token.pos_ == 'ADJ']

    return(len(adjectives))

def count_verbs(col):
    """
    This function takes in a column and returns the number of verbs in that column value

    Args:
    col -> column of a pandas dataframe
    """
    words = nlp(col)

    verbs = [nlp.token.text for nlp.token in words if nlp.token.pos_ == 'VERB']

    return(len(verbs))

def count_named_entities(col):
    """
    This function takes in a column and returns the number of named entities in that column value

    Args:
    col -> column of a pandas dataframe
    
    """
    words = nlp(col)

    #Count named entities
    named_entities_count = len(words.ents)

    return named_entities_count

if __name__ == '__main__':
    #Calling collect function to get dataframe
    df = collect()

    #Adding Feature Columns
    df['Post Length'] = df['Post Title'].apply(lambda x: len(x))
    df['Punctuation_Count'] = df['Post Title'].apply(count_punctuation)/df['Post Length']
    df['Exclam_Count'] = df['Post Title'].apply(count_exclam)/df['Post Length']
    df['Hashtag_Count'] = df['Post Title'].apply(count_hashtags)
    df['Date'] = df['Timestamp'].apply(lambda x: time.ctime(x))

    date_format = "%a %b %d %H:%M:%S %Y"

    df['Date'] = df['Date'].apply(lambda x: datetime.datetime.strptime(x, date_format))

    df['Year'] = df['Date'].apply(lambda x: x.year)
    df['Month'] = df['Date'].apply(lambda x: x.month)
    df['Day'] = df['Date'].apply(lambda x: x.day)

    df['Combined'] = df.apply(lambda row: datetime.datetime(row['Year'], row['Month'], row['Day']), axis=1)

    #Adding columns for part of speech tagging
    df['Adjective_Count'] = df['Post Title'].apply(count_adjectives)/df['Post Length']
    df['Verb_Count'] = df['Post Title'].apply(count_verbs)/df['Post Length']
    df['Entities_Count'] = df['Post Title'].apply(count_named_entities)/df['Post Length']
    df['day_of_week_str'] = df['Combined'].dt.strftime('%A')
    df['Posts_Sentence_Length'] = df['Post Title'].apply(split_sent)
    
    df['Emoji_Count'] = df['Post Title'].apply(is_emoji)

    df['Score'] = 5.732761 + 0.01142 * len(df['Post Title']) + 1.86986 * df['Exclam_Count'] - 0.79648 * df['Hashtag_Count'] - 0.02131 * df['Posts_Sentence_Length'] - 0.25153 * df['Adjective_Count'] - 0.11134 * df['Verb_Count'] - 0.04224 * df['Entities_Count']

    #Converting to Excel File
    file_name = 'CleanedPosts.xlsx'
    df.to_excel(file_name)
