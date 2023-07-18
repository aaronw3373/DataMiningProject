import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

class PlayerCorrelationAnalysis:
    def __init__(self, year, outliers, players):
        self.year = year
        self.outliers = outliers
        self.players = players

    def load_data(self, filename):
        try:
            return pd.read_csv(filename)
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return None

    def perform_analysis(self, player_data, player_name):

        cols_to_convert = ['Age', 'PER', 'BPM', 'VORP', 'WS', 'PTS', 'AST', 'TRB', 'MP', 'WLp', 'SRS']
        for col in cols_to_convert:
            player_data.loc[:, col] = pd.to_numeric(player_data[col], errors='coerce')


        # Calculate the correlation matrix
        correlation_matrix = player_data[['Age', 'PER', 'BPM', 'VORP', 'WS', 'PTS', 'AST', 'TRB', 'MP', 'WLp', 'SRS']].corr()

        print(correlation_matrix)

        # Visualize the correlation matrix with a heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')

        plt.title(f'Correlation matrix of {player_name} - {self.year}')
        output_dir = f'../../output/figures/{self.year}/analysis/{player_name.replace(" ", "_")}'
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, f'correlation_matrix.png'))
        plt.show()


    def plot_stat_over_wlp_srs(self, player_data, player_name):
        plt.figure(figsize=(15, 10))

        stats = ['Age', 'PER', 'BPM', 'VORP', 'WS', 'PTS', 'AST', 'TRB', 'MP']

        for stat in stats:
            plt.subplot(2, 1, 1)
            plt.plot(player_data['WLp'], player_data[stat], label=stat)
            plt.title(f'{player_name} Stats over WLp')
            plt.xlabel('WLp')
            plt.legend()

            plt.subplot(2, 1, 2)
            plt.plot(player_data['SRS'], player_data[stat], label=stat)
            plt.title(f'{player_name} Stats over SRS')
            plt.xlabel('SRS')
            plt.legend()

        plt.tight_layout()
        plt.show()

        

    def scatter_plot(self, data, stats, ylabel):
        fig, axs = plt.subplots(nrows=len(stats), figsize=(17, 11))

        for ax, stat in zip(axs, stats):
            for player in self.players:
                player_data = data[data['Player'] == player]
                ax.scatter(player_data[ylabel], player_data[stat], label=player)

            ax.set_xlabel(ylabel)
            ax.set_ylabel(stat)
            ax.set_title(f'{stat} vs {ylabel} for Different Point Guards')
            ax.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

        plt.tight_layout()
        plt.show()

        output_dir = f'../../output/figures/{self.year}/analysis'
        os.makedirs(output_dir, exist_ok=True)
        fig.savefig(f'../../output/figures/{self.year}/analysis/player_{ylabel}.png')


    def run(self):
        if self.outliers.lower() == 'yes':
            file = f'../../data/processed/nba_{self.year}_proc_or.csv'
        else:
            file = f'../../data/processed/nba_{self.year}_proc.csv'

        data = self.load_data(file)

        if data is not None:
            stats = ['PER', 'BPM', 'VORP']
            self.scatter_plot(data, stats, 'WLp')
            self.scatter_plot(data, stats, 'SRS')
            #for player in self.players:
                #player_data = data[data['Player'] == player]
                #if not player_data.empty:
                    #self.plot_stat_over_wlp_srs(player_data, player)
                #else:
                    #print(f"No data available for player: {player}")
