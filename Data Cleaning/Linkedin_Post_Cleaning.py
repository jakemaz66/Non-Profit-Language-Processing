import pandas as pd
import string
from spellchecker import SpellChecker
import emoji
import spacy

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
spacy.cli.download("en_core_web_lg")
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
    This function takes in a column and returns the number of adject in that column value

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

    #Reading in Data
    df_linkedin = pd.read_excel(r'C:\Users\jakem\Non-Profit-Language-Processing\Data Cleaning\data\Raw Data Files\bethlehem-haven_content_LinkedInData_01_23__01_24 (1).xls',
                                sheet_name='All posts')

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
    linked_in_interest['Punctuation_Count'] = linked_in_interest['Posts'].apply(count_punctuation)/linked_in_interest['Post Length']
    linked_in_interest['Exclam_Count'] = linked_in_interest['Posts'].apply(count_exclam)/linked_in_interest['Post Length']
    linked_in_interest['Hashtag_Count'] = linked_in_interest['Posts'].apply(count_hashtags)
    linked_in_interest['Posts_Sentence_Length'] = linked_in_interest['Posts'].apply(split_sent)
    linked_in_interest['Emoji_Count'] = linked_in_interest['Posts'].apply(is_emoji)

    #Adding columns for part of speech tagging
    linked_in_interest['Adjective_Count'] = linked_in_interest['Posts'].apply(count_adjectives)/linked_in_interest['Post Length']
    linked_in_interest['Verb_Count'] = linked_in_interest['Posts'].apply(count_verbs)/linked_in_interest['Post Length']
    linked_in_interest['Entities_Count'] = linked_in_interest['Posts'].apply(count_named_entities)/linked_in_interest['Post Length']
    linked_in_interest['day_of_week_str'] = linked_in_interest['Combined'].dt.strftime('%A')

    #Exporting to File
    excel_filename = 'Cleaned LinkedIn Data.xlsx'
    linked_in_interest.to_excel(excel_filename)



