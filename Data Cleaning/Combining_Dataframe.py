import pandas as pd

df_1 = pd.read_excel(r'C:\Users\jakem\Non-Profit-Language-Processing\Data Cleaning\Cleaned Output Files\Cleaned LinkedIn Data.xlsx')
df_2 = pd.read_excel(r'C:\Users\jakem\Non-Profit-Language-Processing\Data Cleaning\Cleaned Output Files\Cleaned Reels Data.xlsx')
df_3 = pd.read_excel(r'C:\Users\jakem\Non-Profit-Language-Processing\Data Cleaning\Cleaned Output Files\CleanedPosts.xlsx')

combined_df = pd.concat([df_1, df_2, df_3], axis=1)

print(combined_df.columns)