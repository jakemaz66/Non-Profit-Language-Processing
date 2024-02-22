#Loading in data
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#Reading in cleaned dataframes
df_linkedin = pd.read_excel(r'Data Cleaning/data/Cleaned LinkedIn Data.xlsx')
df_intsa_reels = pd.read_excel(r'Data Cleaning/data/Cleaned Reels Data.xlsx')
df_insta = pd.read_excel(r'Data Cleaning/data/CleanedPosts.xlsx')

print(df_insta.columns)

#Defining a features list
features = ['Post Length', 'Punctuation_Count', 'Hashtag_Count', 'Posts_Sentence_Length', 'Emoji_Count', 
            'Adjective_Count', 'Verb_Count', 'Entities_Count']

correlation_matrix = df_insta[features].corr()

#Display the correlation matrix
print(correlation_matrix)

sns.set(font_scale=0.9)  
plt.figure(figsize=(10, 8))  
heatmap = sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")

heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation=45, horizontalalignment='right', font_scale=0.7)

plt.show()