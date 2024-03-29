import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer as sia
import string as st

#Sentiment Analysis
sia = sia()


def remove_stopwords(text):
    """
    This function removes the commonly used stopwords for sentiment analysis

    Args:
    text -> A string object
    """
    #Getting unique stop words
    stop_words = set(stopwords.words('english'))

    #Tokenizing the passed text
    words = word_tokenize(text)

    #Only keeping words that aren't a stop word
    filtered_words = [word for word in words if word.lower() not in stop_words]

    #Rejoining the list elements into one string and returning
    return ' '.join(filtered_words)

def fill(text):
        text = text.astype(str)
        if(len(text) == 0):
            return " "

def sentiment_model():
    #Downloading Necessary NLTK libraries
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('vader_lexicon')

    #Reading in cleaned dataframes
    df_linkedin = pd.read_excel(r'C:\Users\jakem\Non-Profit-Language-Processing\Data Cleaning\data\Cleaned LinkedIn Data.xlsx')
    df_intsa_reels = pd.read_excel(r'C:\Users\jakem\Non-Profit-Language-Processing\Data Cleaning\data\CleanedPosts.xlsx')
    df_insta = pd.read_excel(r'C:\Users\jakem\Non-Profit-Language-Processing\Data Cleaning\data\Cleaned Reels Data.xlsx')
        
    df_intsa_reels['Post Title'] = df_intsa_reels['Post Title'].astype(str)
    df_insta['Post Title'] = df_insta['Post Title'].astype(str)

    #Lowercasing all text
    df_linkedin['Posts'] = df_linkedin['Posts'].apply(lambda x: x.lower())
    df_intsa_reels['Post Title'] = df_intsa_reels['Post Title'].apply(lambda x: x.lower())
    df_insta['Post Title'] = df_insta['Post Title'].apply(lambda x: x.lower())

    # Apply the function to the 'text' column
    df_linkedin['Posts_Analysis'] = df_linkedin['Posts'].apply(remove_stopwords)
    df_intsa_reels['Posts_Analysis'] = df_intsa_reels['Post Title'].apply(remove_stopwords)
    df_insta['Posts_Analysis'] = df_insta['Post Title'].apply(remove_stopwords)

    df_linkedin['sentiment'] = df_linkedin['Posts_Analysis'].apply(lambda x: sia.polarity_scores(x)['compound'])
    df_intsa_reels['sentiment'] = df_intsa_reels['Posts_Analysis'].apply(lambda x: sia.polarity_scores(x)['compound'])
    df_insta['sentiment'] = df_insta['Posts_Analysis'].apply(lambda x: sia.polarity_scores(x)['compound'])

    # Categorize sentiment into positive, negative, or neutral
    df_linkedin['sentiment_category'] = df_linkedin['sentiment'].apply(lambda x: 'positive' if x > .85 
                                                                    else ('negative' if x < 0 else 'neutral'))

    df_intsa_reels['sentiment_category'] = df_intsa_reels['sentiment'].apply(lambda x: 'positive' if x > .85 
                                                                    else ('negative' if x < 0 else 'neutral'))

    df_insta['sentiment_category'] = df_insta['sentiment'].apply(lambda x: 'positive' if x > .85 
                                                                    else ('negative' if x < 0 else 'neutral'))

    df_linkedin_group = df_linkedin.groupby('sentiment_category')['Likes'].mean()
    sent_data = pd.DataFrame({'Sentiment': df_linkedin_group.index, 'Average Likes': df_linkedin_group.values})

    df_insta_group = df_insta.groupby('sentiment_category')['Likes'].mean()
    sent_data_2 = pd.DataFrame({'Sentiment': df_insta_group.index, 'Average Likes': df_insta_group.values})

    #Exporting to Dataframes
    file_name_1 = 'CleanedPosts.xlsx'
    df_insta.to_excel(file_name_1)

    file_name_2 = 'Cleaned LinkedIn Data.xlsx'
    df_linkedin.to_excel(file_name_2)

    file_name_3 = 'Cleaned Reels Data.xlsx'
    df_intsa_reels.to_excel(file_name_3)

if __name__ == '__main__':
     sentiment_model()

