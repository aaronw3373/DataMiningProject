import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

class CorrelationAnalysis:
    def __init__(self, year, outliers,simple):
        self.year = year
        self.outliers = outliers
        self.simple = simple

    def load_data(self, filename):
        try:
            return pd.read_csv(filename)
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return None

    def perform_analysis(self, data):
        # Calculate the correlation matrix
        
        if self.simple.lower() == 'yes':
            correlation_matrix = data[['PER', 'BPM', 'WLp', 'SRS']].corr()
        

            # Visualize the correlation matrix with a heatmap
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')

            plt.title(f'Correlation matrix of PER, BPM, Win/Loss Percentage and SRS - {self.year}')
            output_dir = f'../../output/figures/{self.year}/analysis'
            os.makedirs(output_dir, exist_ok=True)
            plt.savefig(f'../../output/figures/{self.year}/analysis/correlation_matrix.png')
            plt.show()

            # Take a subset of the data containing only the first 20 players
            data_subset = data

            # Pairplot of the subset of the data
            sns.pairplot(data_subset[['PER', 'BPM', 'WLp', 'SRS']])
            plt.suptitle(f'Pairplot for the first 20 players - {self.year}', y=1.02)
            plt.savefig(f'../../output/figures/{self.year}/analysis/pairplot.png')
            plt.show()


        else:
            plt.figure(figsize=(15, 9))
            correlation_matrix = data[['Age', 'PER', 'BPM', 'VORP', 'WS', 'PTS', 'AST', 'TRB','MP','WLp','SRS']].corr()
                 # Visualize the correlation matrix with a heatmap
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')

            plt.title(f'Correlation matrix of Advanced Stats - {self.year}')
            output_dir = f'../../output/figures/{self.year}/analysis'
            os.makedirs(output_dir, exist_ok=True)
            plt.savefig(f'../../output/figures/{self.year}/analysis/correlation_matrix_full.png')
            correlation_matrix.to_csv(f'../../output/figures/{self.year}/analysis/correlation_matrix.csv', index=False)
            plt.show()

             # Take a subset of the data containing only the first 20 players
            data_subset = data

            # Pairplot of the subset of the data
            sns.pairplot(data_subset[['Age', 'PER', 'BPM', 'VORP', 'WS', 'PTS', 'AST', 'TRB','MP','WLp','SRS']])
            plt.suptitle(f'Pairplot for the first 20 players - {self.year}', y=1.02)
            plt.savefig(f'../../output/figures/{self.year}/analysis/pairplot_full.png')
            plt.show()


       
    def run(self):
        if self.outliers.lower() == 'yes':
            file = f'../../data/processed/nba_{self.year}_proc_or.csv'
        else:
            file = f'../../data/processed/nba_{self.year}_proc.csv'

        data = self.load_data(file)

        if data is not None:
            self.perform_analysis(data)