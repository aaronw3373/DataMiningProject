import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the normalized data
normalized_data = pd.read_csv('../../data/interim/nba_2023_normalized.csv')

# Identify numeric columns (float or int)
numeric_cols = normalized_data.select_dtypes(include=['float64', 'int64']).columns

# Group by 'Rk' and 'Player', compute mean on numeric columns, reset index, and sort by 'Rk'
aggregated_data = normalized_data.groupby(['Rk', 'Player','Pos'], as_index=False)[numeric_cols].mean().reset_index(drop=True)

# Save aggregated data to a new CSV file
aggregated_data.to_csv('../../data/interim/nba_2023_aggregated.csv', index=False)

# Select only the relevant columns
selected_data = aggregated_data[['Rk', 'Player','Pos', 'Age', 'PER', 'BPM', 'VORP', 'WS', 'PTS', 'AST', 'TRB']]

# Save selected data to a new CSV file
selected_data.to_csv('../../data/processed/nba_2023_proc.csv', index=False)



# Set the style of the visualization
sns.set(style="whitegrid")

# Create a boxplot for each column of the selected data
for column in selected_data.columns:
    if column not in ['Rk', 'Player','Pos','Tm']:
        plt.figure(figsize=(6, 6))
        sns.boxplot(x=selected_data[column])
        plt.title(f'Boxplot of {column}')
        plt.show()