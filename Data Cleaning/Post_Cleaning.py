#Importing Libraries
import pandas as pd
import json
import string
import time
import datetime
import emoji
import spacy

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

#Calling collect function to get dataframe
df = collect(data)

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

df['Posts_Sentence_Length'] = df['Post Title'].apply(split_sent)

#Function to detect spelling mistakes

#Function to detect emojis (so they will not be counted in the mistakes)
def is_emoji(word):
    """
    This function takes in a string and returns the number of emojis

    Args:
    word -> a string
    """
    return sum(1 for character in word if emoji.is_emoji(character))


#Work in Progress Function
#def detect_mistakes(col):
    checker = SpellChecker()
    words = col.split()

    #Filtering out any emojis present
    words = [word for word in words if not is_emoji(word)]

    mistakes = checker.unknown(words)

    number_mistakes = len(mistakes)
    return number_mistakes

df['Emoji_Count'] = df['Post Title'].apply(is_emoji)

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

#Adding columns for part of speech tagging
df['Adjective_Count'] = df['Post Title'].apply(count_adjectives)/df['Post Length']
df['Verb_Count'] = df['Post Title'].apply(count_verbs)/df['Post Length']
df['Entities_Count'] = df['Post Title'].apply(count_named_entities)/df['Post Length']

#Converting to Excel File
file_name = 'CleanedPosts.xlsx'
df.to_excel(file_name)
