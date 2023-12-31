import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class ProcData:
    def __init__(self, year, outliers):
        self.year = year
        self.outliers = outliers
 
    def save_graph(self, data, column):
        plt.figure(figsize=(6, 6))
        sns.boxplot(x=data[column])
        if self.outliers.lower() == 'yes':
            plt.title(f'Boxplot of {column} (25th to 75th percentile of the data) - {self.year}')
            output_dir = f'../../output/figures/{self.year}/outliers_removed'
            os.makedirs(output_dir, exist_ok=True)
            plt.savefig(os.path.join(output_dir, f'{column}_{self.year}_boxplot_or.png'))
        else:
            plt.title(f'Boxplot of {column} - {self.year}')
            output_dir = f'../../output/figures/{self.year}/outliers'
            os.makedirs(output_dir, exist_ok=True)
            plt.savefig(os.path.join(output_dir, f'{column}_{self.year}_boxplot.png'))        
        plt.close()


    def run(self):

        if self.outliers.lower() == 'yes':
            # Load the normalized data
            normalized_data = pd.read_csv(f'../../data/interim/nba_{self.year}_normalized_or.csv')
        else:
            normalized_data = pd.read_csv(f'../../data/interim/nba_{self.year}_normalized.csv')

        # Identify numeric columns (float or int)
        numeric_cols = normalized_data.select_dtypes(include=['float64', 'int64']).columns

        # Group by 'Rk' and 'Player', compute mean on numeric columns, reset index, and sort by 'Rk'
        aggregated_data = normalized_data.groupby(['Rk', 'Player','Pos'], as_index=False)[numeric_cols].mean().reset_index(drop=True)

        # Save aggregated data to a new CSV file
        aggregated_data.to_csv(f'../../data/interim/nba_{self.year}_aggregated.csv', index=False)

        # Select only the relevant columns
        selected_data = aggregated_data[['Rk', 'Player','Pos', 'Age', 'PER', 'BPM', 'VORP', 'WS', 'PTS', 'AST', 'TRB','MP','WLp','SRS']]

        

        if self.outliers.lower() == 'yes':
            # Save selected data to a new CSV file
            selected_data.to_csv(f'../../data/processed/nba_{self.year}_proc_or.csv', index=False)
        else:
            # Save selected data to a new CSV file
            selected_data.to_csv(f'../../data/processed/nba_{self.year}_proc.csv', index=False)

        # Ask the user if they want to graph the visualizations
        graph = input("Do you want to save the graphs as PNG? (yes/no): ")

        if graph.lower() == 'yes':
            save_graphs = input("Do you want to graph the visualizations? (yes/no): ")
        
            # Set the style of the visualization
            sns.set(style="whitegrid")

            # Create a boxplot for each column of the selected data
            for column in selected_data.columns:
                if column not in ['Rk', 'Player','Pos','Tm']:
                    if save_graphs.lower() == 'yes':
                        self.save_graph(selected_data, column)
                        plt.figure(figsize=(6, 6))
                        sns.boxplot(x=selected_data[column])
                        if self.outliers.lower() == 'yes':
                            plt.title(f'Boxplot of {column} (25th to 75th percentile of the data) - {self.year}')
                        else:
                            plt.title(f'Boxplot of {column} - {self.year}')
                        plt.show()
                    else: 
                        self.save_graph(selected_data, column)
                        
