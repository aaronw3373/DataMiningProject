import pandas as pd

# Load the raw data
raw_data = pd.read_csv('../../data/raw/nba_2023_per_game_raw.csv')

# Fill missing data with a placeholder value (like 0 or 'unknown')
cleaned_data = raw_data.fillna(0)

# Save cleaned data to interim folder
cleaned_data.to_csv('../../data/interim/nba_2023_per_game_cleaned.csv', index=False)


# Clean the data
cleaned_data = cleaned_data.copy()

i = 20
while i < len(cleaned_data):
    if cleaned_data.loc[i, 'Rk'] == 'Rk':
        cleaned_data = cleaned_data.drop(i).reset_index(drop=True)
        print('erased: ', i)
    i += 1
     



for col in cleaned_data.columns:
    # convert all columns to numeric, if possible
    
    
    # Normalize the data if the column isn't 'Player' or 'Tm'
    if col not in ['Rk','Age','Player', 'Tm']:
        cleaned_data[col] = pd.to_numeric(cleaned_data[col], errors='coerce')
        cleaned_data[col] = (cleaned_data[col] - cleaned_data[col].min()) / (cleaned_data[col].max() - cleaned_data[col].min())

# Save the Normalized data
cleaned_data.to_csv('../../data/interim/nba_2023_per_game_normalized.csv', index=False)