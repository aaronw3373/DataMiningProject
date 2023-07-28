import pandas as pd
import matplotlib.pyplot as plt


class Comparison:
    def __init__(self, year):
        self.year = year
    def trade_comparison(self):
        # Load the data
        data_2022 = pd.read_csv('../../models/data/nba_predicted_trade_values_2022.csv')
        data_2023 = pd.read_csv('../../models/data/nba_predicted_trade_values_2023.csv')

        # Create a list of traded players
        traded_players = [
            "Josh Richardson", "Devonte' Graham", "Danny Green", "Eric Gordon", "Luke Kennard", 
            "Mo Bamba", "Patrick Beverley", "Saddiq Bey", "James Wiseman", "Kevin Knox", 
            "Garrison Mathews", "Bruno Fernando", "Justin Holiday", "Frank Kaminsky", 
            "Bones Hyland", "George Hill", "Serge Ibaka", "Jordan Nwora", "Jae Crowder", 
            "Matisse Thybulle", "Jalen McDaniels", "Svi Mykhailiuk", "Thomas Bryant", "Davon Reed", 
            "Mike Muscala", "Justin Jackson", "Kevin Durant", "T.J. Warren", "Mikal Bridges", 
            "Cameron Johnson", "Jakob Poeltl", "Khem Birch", "Josh Hart", "Cam Reddish", 
            "Ryan Arcidiacono", "D'Angelo Russell", "Malik Beasley", "Jarred Vanderbilt", 
            "Mike Conley", "Nickeil Alexander-Walker", "Russell Westbrook", "Juan Toscano-Anderson", 
            "Damian Jones", "Kessler Edwards", "Dewayne Dedmon", "Kyrie Irving", "Markieff Morris", 
            "Spencer Dinwiddie", "Dorian Finney-Smith", "Rui Hachimura", "Kendrick Nunn", "Noah Vonleh", 
            "David Nwaba", "Sterling Brown", "Trey Burke", "Marquese Chriss", "Derrick Favors", 
            "Ty Jerome", "Maurice Harkless", "Theo Maledon", "Kelly Olynyk", "Saben Lee", 
            "Bojan Bogdanovic", "Lauri Markkanen", "Ochai Agbaji", "Collin Sexton", "Donovan Mitchell", 
            "Rudy Gobert", "Patrick Beverley", "Walker Kessler", "Leandro Bolmaro", "Malcolm Brogdon", 
            "Nik Stauskas", "Malik Fitts", "Juwan Morgan", "Daniel Theis", "Aaron Nesmith", 
            "Royce O'Neale", "Dejounte Murray", "Danilo Gallinari", "Will Barton", "Monte Morris", 
            "Kentavious Caldwell-Pope", "Ish Smith"
        ]

        # Filter the data for traded players
        data_2022_traded = data_2022[data_2022['Player'].isin(traded_players)]
        data_2023_traded = data_2023[data_2023['Player'].isin(traded_players)]

        # Merge the 2022 and 2023 data
        data_traded = pd.merge(data_2022_traded, data_2023_traded, on='Player', suffixes=('_2022', '_2023'))

        # Calculate the difference in Trade Value
        data_traded['Difference_TV'] = data_traded['Trade Value_2023'] - data_traded['Trade Value_2022']
        # Calculate the difference in WLp
        data_traded['Difference_WLp'] = data_traded['WLp_2023'] - data_traded['WLp_2022']
        # Calculate the difference in SRS
        data_traded['Difference_SRS'] = data_traded['SRS_2023'] - data_traded['SRS_2022']
        # Select only the columns we're interested in
        data_traded = data_traded[['Player', 'Trade Value_2022', 'Trade Value_2023', 'Difference_TV','WLp_2022','WLp_2023','Difference_WLp','SRS_2022','SRS_2023','Difference_SRS','Predicted Trade Value (RandomForest)_2023']]

        return data_traded
    
    def plots(self,data_traded):
        # List of numeric columns to average
        numeric_columns = ['Trade Value_2022', 'SRS_2022', 'Trade Value_2023', 'SRS_2023', 'WLp_2022', 'WLp_2023']

        # Average out duplicate points for numeric columns only
        data_traded[numeric_columns] = data_traded.groupby(['Trade Value_2022', 'SRS_2022'])[numeric_columns].transform('mean')

        # Drop duplicates
        data_traded = data_traded.drop_duplicates(subset=['Trade Value_2022', 'SRS_2022'])

        data_traded.drop_duplicates(subset='Player', inplace=True)

        # Sort by Average_SRS
        data_traded_sorted = data_traded.sort_values(by='Predicted Trade Value (RandomForest)_2023')

        plt.figure(figsize=(10, 6))
        plt.scatter(data_traded_sorted['Trade Value_2023'], data_traded_sorted['Predicted Trade Value (RandomForest)_2023'], alpha=0.5)
        plt.plot([data_traded_sorted['Trade Value_2023'].min(), data_traded_sorted['Trade Value_2023'].max()], 
                [data_traded_sorted['Trade Value_2023'].min(), data_traded_sorted['Trade Value_2023'].max()], 
                'k--', lw=2,label='Perfect Predictions')
        plt.xlabel('Actual Trade Value')
        plt.ylabel('Predicted Trade Value')
        plt.title('Actual vs Predicted Trade Value (RandomForest)')
        plt.grid(True)
        plt.savefig('../../output/models/data/acutual_predicted_tv.png')
        plt.legend()
        plt.show()

        # Sort by SRS_2022
        data_traded_sorted_2022 = data_traded.sort_values(by='Trade Value_2022')

        # Sort by SRS_2023
        data_traded_sorted_2023 = data_traded.sort_values(by='Trade Value_2023')

        # Plot Trade Value_2022 Vs SRS_2022
        plt.figure(figsize=(10, 6))
        plt.plot(data_traded_sorted_2022['Trade Value_2022'], data_traded_sorted_2022['SRS_2022'], marker='o')
        plt.title('Trade Value 2022 vs SRS 2022')
        plt.xlabel('Trade Value 2022')
        plt.ylabel('SRS 2022')
        plt.grid(True)
        plt.savefig('../../output/models/data/tv_SRS_2022.png')
        plt.show()

        # Plot Trade Value_2023 Vs SRS_2023
        plt.figure(figsize=(10, 6))
        plt.plot(data_traded_sorted_2023['Trade Value_2023'], data_traded_sorted_2023['SRS_2023'], marker='o')
        plt.title('Trade Value 2023 vs SRS 2023')
        plt.xlabel('Trade Value 2023')
        plt.ylabel('SRS 2023')
        plt.grid(True)
        plt.savefig('../../output/models/data/tv_SRS_2023.png')
        plt.show()


        # Plot Trade Value_2022 Vs WLp_2022
        plt.figure(figsize=(10, 6))
        plt.plot(data_traded_sorted_2022['Trade Value_2022'], data_traded_sorted_2022['WLp_2022'], marker='o')
        plt.title('Trade Value 2022 vs WLp 2022')
        plt.xlabel('Trade Value 2022')
        plt.ylabel('WLp 2022')
        plt.grid(True)
        plt.savefig('../../output/models/data/tv_wlp_2022.png')
        plt.show()

        # Plot Trade Value_2023 Vs WLp_2023
        plt.figure(figsize=(10, 6))
        plt.plot(data_traded_sorted_2023['Trade Value_2023'], data_traded_sorted_2023['WLp_2023'], marker='o')
        plt.title('Trade Value 2023 vs WLp 2023')
        plt.xlabel('Trade Value 2023')
        plt.ylabel('WLp 2023')
        plt.grid(True)
        plt.savefig('../../output/models/data/tv_wlp_2023.png')
        plt.show()

        # Sort by Difference_TV
        data_traded_sorted = data_traded.sort_values(by='Difference_TV')
        # Plot Difference
        plt.figure(figsize=(20, 10))
        plt.plot(data_traded_sorted['Player'], data_traded_sorted['Difference_TV'], marker='o')
        #plt.plot(data_traded_sorted['Player'], data_traded_sorted['Difference_WLp'], marker='o')
        #plt.plot(data_traded_sorted['Player'], data_traded_sorted['Difference_SRS'], marker='o')
        plt.title('Difference in Trade Value from 2022 to 2023')
        plt.xlabel('Player')
        plt.ylabel('Difference')
        plt.xticks(rotation=90)
        plt.grid(True)
        plt.savefig('../../output/models/data/TV.png')
        plt.show()

        # Sort by Difference_TV
        data_traded_sorted = data_traded.sort_values(by='Difference_SRS')
        # Plot Difference
        plt.figure(figsize=(20, 10))
        plt.plot(data_traded_sorted['Player'], data_traded_sorted['Difference_SRS'], marker='o')
        #plt.plot(data_traded_sorted['Player'], data_traded_sorted['Difference_WLp'], marker='o')
        #plt.plot(data_traded_sorted['Player'], data_traded_sorted['Difference_SRS'], marker='o')
        plt.title('Difference in SRS from 2022 to 2023')
        plt.xlabel('Player')
        plt.ylabel('Difference')
        plt.xticks(rotation=90)
        plt.grid(True)
        plt.savefig('../../output/models/data/SRS.png')
        plt.show()

        # Sort by Difference_TV
        data_traded_sorted = data_traded.sort_values(by='Difference_WLp')
        # Plot Difference
        plt.figure(figsize=(20, 10))
        plt.plot(data_traded_sorted['Player'], data_traded_sorted['Difference_WLp'], marker='o')
        #plt.plot(data_traded_sorted['Player'], data_traded_sorted['Difference_WLp'], marker='o')
        #plt.plot(data_traded_sorted['Player'], data_traded_sorted['Difference_SRS'], marker='o')
        plt.title('Difference in WLp from 2022 to 2023')
        plt.xlabel('Player')
        plt.ylabel('Difference')
        plt.xticks(rotation=90)
        plt.grid(True)
        plt.savefig('../../output/models/data/WLp.png')
        plt.show()


        data_traded_sorted = data_traded.sort_values(by='Trade Value_2023')
        # Plot Difference
        plt.figure(figsize=(20, 10))
        plt.plot(data_traded_sorted['Player'], data_traded_sorted['Trade Value_2023'], marker='o')
        plt.title('Trade Value 2023')
        plt.xlabel('Player')
        plt.ylabel('Trade Value')
        plt.xticks(rotation=90)
        plt.grid(True)
        plt.savefig('../../output/models/data/TV_2023.png')
        plt.show()

        data_traded_sorted = data_traded.sort_values(by='Difference_TV')
        # Plot Difference
        plt.figure(figsize=(20, 10))
        plt.plot(data_traded_sorted['Player'], data_traded_sorted['Trade Value_2023'], marker='o',label='Trade Value 2023')
        plt.plot(data_traded_sorted['Player'], data_traded_sorted['Trade Value_2022'], marker='o',label='Trade Value 2022')
        plt.plot(data_traded_sorted['Player'], data_traded_sorted['Difference_TV'], marker='o',label='Difference')
        plt.title('Trade Values -Sorted by Difference')
        plt.xlabel('Player')
        plt.ylabel('Trade Value')
        plt.xticks(rotation=90)
        plt.legend()
        plt.grid(True)
        plt.savefig('../../output/models/data/tv_diff.png')
        plt.show()

        data_traded_sorted = data_traded.sort_values(by='Difference_WLp')
        # Plot Difference
        plt.figure(figsize=(20, 10))
        plt.plot(data_traded_sorted['Player'], data_traded_sorted['WLp_2023'], marker='o', label='WLp 2023')
        plt.plot(data_traded_sorted['Player'], data_traded_sorted['WLp_2022'], marker='o', label='WLp 2022')
        plt.plot(data_traded_sorted['Player'], data_traded_sorted['Difference_WLp'], marker='o',label='Difference')
        plt.title('WLp -Sorted by Difference')
        plt.xlabel('Player')
        plt.ylabel('WLp')
        plt.xticks(rotation=90)
        plt.legend()
        plt.grid(True)
        plt.savefig('../../output/models/data/WLp_diff.png')
        plt.show()

        data_traded_sorted = data_traded.sort_values(by='Difference_SRS')
        # Plot Difference
        plt.figure(figsize=(20, 10))
        plt.plot(data_traded_sorted['Player'], data_traded_sorted['SRS_2023'], marker='o',label='SRS 2023')
        plt.plot(data_traded_sorted['Player'], data_traded_sorted['SRS_2022'], marker='o',label='SRS 2022')
        plt.plot(data_traded_sorted['Player'], data_traded_sorted['Difference_SRS'], marker='o',label='Difference')
        plt.title('SRS -Sorted by Difference')
        plt.xlabel('Player')
        plt.ylabel('SRS')
        plt.xticks(rotation=90)
        plt.legend()
        plt.grid(True)
        plt.savefig('../../output/models/data/SRS_diff.png')
        plt.show()

        # Calculate average Trade Value, WLp, and SRS
        data_traded['Average_TV'] = (data_traded['Trade Value_2022'] + data_traded['Trade Value_2023']) / 2
        data_traded['Average_WLp'] = (data_traded['WLp_2022'] + data_traded['WLp_2023']) / 2
        data_traded['Average_SRS'] = (data_traded['SRS_2022'] + data_traded['SRS_2023']) / 2

        # Sort by Average_TV
        data_traded_sorted = data_traded.sort_values(by='Average_TV')

        # Plot Trade Values
        plt.figure(figsize=(20, 10))
        plt.plot(data_traded_sorted['Player'], data_traded_sorted['Trade Value_2023'], marker='o', label='Trade Value 2023')
        plt.plot(data_traded_sorted['Player'], data_traded_sorted['Trade Value_2022'], marker='o', label='Trade Value 2022')
        plt.plot(data_traded_sorted['Player'], data_traded_sorted['Average_TV'], marker='o', label='Average Trade Value')
        plt.title('Trade Values -Sorted by Avg')
        plt.xlabel('Player')
        plt.ylabel('Trade Value')
        plt.xticks(rotation=90)
        plt.legend()
        plt.grid(True)
        plt.savefig('../../output/models/data/tv_avg.png')
        plt.show()

        # Sort by Average_WLp
        data_traded_sorted = data_traded.sort_values(by='WLp_2023')

        # Plot WLp
        plt.figure(figsize=(20, 10))
        plt.plot(data_traded_sorted['Player'], data_traded_sorted['WLp_2023'], marker='o', label='WLp 2023')        
        plt.plot(data_traded_sorted['Player'], data_traded_sorted['WLp_2022'], marker='o', label='WLp 2022')
        plt.plot(data_traded_sorted['Player'], data_traded_sorted['Average_WLp'], marker='o', label='Average WLp')
        plt.title('WLp -Sorted by WLp 2023')
        plt.xlabel('Player')
        plt.ylabel('WLp')
        plt.xticks(rotation=90)
        plt.legend()
        plt.grid(True)
        plt.savefig('../../output/models/data/WLp_wlp2023.png')
        plt.show()

        # Sort by Average_SRS
        data_traded_sorted = data_traded.sort_values(by='SRS_2023')

        # Plot SRS
        plt.figure(figsize=(20, 10))
        plt.plot(data_traded_sorted['Player'], data_traded_sorted['SRS_2023'], marker='o', label='SRS 2023')        
        plt.plot(data_traded_sorted['Player'], data_traded_sorted['SRS_2022'], marker='o', label='SRS 2022')
        plt.plot(data_traded_sorted['Player'], data_traded_sorted['Average_SRS'], marker='o', label='Average SRS')
        plt.title('SRS -Sorted by SRS 2023')
        plt.xlabel('Player')
        plt.ylabel('SRS')
        plt.xticks(rotation=90)
        plt.legend()
        plt.grid(True)
        plt.savefig('../../output/models/data/SRS_srs2023.png')
        plt.show()




    def run(self):
        data_traded = self.trade_comparison()
        # Save to CSV
        data_traded.to_csv('../../models/data/nba_traded_players_trade_values.csv', index=False)
        self.plots(data_traded)
