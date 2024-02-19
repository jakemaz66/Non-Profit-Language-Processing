import pandas as pd
import string
from spellchecker import SpellChecker
import emoji


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

#Adding Sentence Length Column
def split_sent(col):
    sentences = col.replace('!', '.').replace('?', '.').split('.')
    sentences = [s.strip() for s in sentences if s.strip()]  
    total_length = sum(len(sentence.split()) for sentence in sentences)
    
    if len(sentences) > 0:
        average_length = total_length / len(sentences)
        return average_length
    else:
        return 0  

linked_in_interest['Posts_Sentence_Length'] = linked_in_interest['Posts'].apply(split_sent)

#Function to detect spelling mistakes

#Function to detect emojis (so they will not be counted in the mistakes)
def is_emoji(word):
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

linked_in_interest['Emoji_Count'] = linked_in_interest['Posts'].apply(is_emoji)


#Exporting to File
excel_filename = 'Cleaned LinkedIn Data.xlsx'
linked_in_interest.to_excel(excel_filename)



