#Importing Libraries
import pandas as pd
import json
import string
import datetime
import time
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
    file_path = r'C:\Users\jakem\Non-Profit-Language-Processing\Data Cleaning\data\Raw Data Files\reels.json'

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

if __name__ == "__main__":
    #Getting dataframe from collect
    df = collect()

    #Adding Feature Columns
    df['Post Length'] = df['Post Title'].apply(lambda x: len(x))
    df['Punctuation_Count'] = df['Post Title'].apply(count_punctuation)/df['Post Length']
    df['Exclam_Count'] = df['Post Title'].apply(count_exclam)/df['Post Length']
    df['Hashtag_Count'] = df['Post Title'].apply(count_hashtags)
    df['Emoji_Count'] = df['Post Title'].apply(is_emoji)
    df['Posts_Sentence_Length'] = df['Post Title'].apply(split_sent)

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

    #Converting to Excel File
    excel_filename = 'Cleaned Reels Data.xlsx'
    df.to_excel(excel_filename)