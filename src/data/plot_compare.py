import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import seaborn as sns
import os

class PlotCompare:
    def __init__(self, year, compare, save_fig):
        self.year = year
        self.compare = compare
        self.save_fig = save_fig

    def load_data(self, filename):
        try:
            return pd.read_csv(filename)
        except FileNotFoundError:
            print(f"File {filename} not found. \nTo use Comparison: First gather, clean, and process both outliers and non-outliers files first.")
            return None
        
        

    def plot_comparison(self, data_orig, data_or, column):
        plt.figure(figsize=(10, 6))
        
        # Make sure we're working with a copy of the data and not a view
        data_orig = data_orig.copy()
        data_orig['Type'] = 'Original'
        data_or = data_or.copy()
        data_or['Type'] = 'Outliers Removed'

        # Concatenate the data
        data_all = pd.concat([data_orig, data_or])
        
        sns.boxplot(y=column, x='Type', data=data_all, palette=['coral', 'lightblue'], showfliers=False)

        plt.title(f'Boxplot Comparison of {column} - {self.year}')

        
        if self.save_fig.lower() == 'yes':
            output_dir = f'../../output/figures/{self.year}/comparison'
            os.makedirs(output_dir, exist_ok=True)
            plt.savefig(os.path.join(output_dir, f'{column}_{self.year}_boxplot_comparison.png'))

        
        plt.show()


    def run(self):
        file_orig = f'../../data/processed/nba_{self.year}_proc.csv'
        file_or = f'../../data/processed/nba_{self.year}_proc_or.csv'

        data_orig = self.load_data(file_orig)
        data_or = self.load_data(file_or)

        if data_orig is None or data_or is None:
            return

        
        if self.compare.lower() == 'yes':
            # Select only the relevant columns
            selected_data_orig = data_orig[['Age', 'PER', 'BPM', 'VORP', 'WS', 'PTS', 'AST', 'TRB','MP']]
            selected_data_or = data_or[['Age', 'PER', 'BPM', 'VORP', 'WS', 'PTS', 'AST', 'TRB','MP']]

            # Create a boxplot for each column of the selected data
            for column in selected_data_orig.columns:
                self.plot_comparison(selected_data_orig, selected_data_or, column)
