import pandas as pd
import numpy as np
import pyfpgrowth
import matplotlib.pyplot as plt
import itertools


trades_2023 = [
    ["Josh Richardson", "Devonte' Graham"],
    ["Danny Green", "Eric Gordon", "Luke Kennard"],
    ["Mo Bamba", "Patrick Beverley"],
    ["Saddiq Bey", "James Wiseman", "Kevin Knox", "Garrison Mathews", "Bruno Fernando", "Justin Holiday", "Frank Kaminsky"],
    ["Bones Hyland"],
    ["George Hill", "Serge Ibaka", "Jordan Nwora", "Jae Crowder"],
    ["Matisse Thybulle", "Jalen McDaniels", "Svi Mykhailiuk"],
    ["Thomas Bryant", "Davon Reed"],
    ["Mike Muscala", "Justin Jackson"],
    ["Kevin Durant", "T.J. Warren", "Mikal Bridges", "Cameron Johnson", "Jae Crowder"],
    ["Jakob Poeltl", "Khem Birch"],
    ["Josh Hart", "Cam Reddish", "Ryan Arcidiacono", "Svi Mykhailiuk"],
    ["D'Angelo Russell", "Malik Beasley", "Jarred Vanderbilt", "Mike Conley", "Nickeil Alexander-Walker", "Russell Westbrook", "Juan Toscano-Anderson", "Damian Jones"],
    ["Kessler Edwards"],
    ["Dewayne Dedmon"],
    ["Kyrie Irving", "Markieff Morris", "Spencer Dinwiddie", "Dorian Finney-Smith"],
    ["Rui Hachimura", "Kendrick Nunn"],
    ["Noah Vonleh"],
    ["David Nwaba", "Sterling Brown", "Trey Burke", "Marquese Chriss", "Derrick Favors", "Ty Jerome", "Maurice Harkless", "Theo Maledon"],
    ["Maurice Harkless"],
    ["Kelly Olynyk", "Saben Lee", "Bojan Bogdanovic"],
    ["Lauri Markkanen", "Ochai Agbaji", "Collin Sexton", "Donovan Mitchell"],
    ["Rudy Gobert", "Malik Beasley", "Patrick Beverley", "Walker Kessler", "Jarred Vanderbilt", "Leandro Bolmaro"],
    ["Malcolm Brogdon", "Nik Stauskas", "Malik Fitts", "Juwan Morgan", "Daniel Theis", "Aaron Nesmith"],
    ["Justin Holiday", "Maurice Harkless"],
    ["Royce O'Neale"],
    ["Dejounte Murray", "Danilo Gallinari"],
    ["Will Barton", "Monte Morris", "Kentavious Caldwell-Pope", "Ish Smith"]
]


class AssociationRuleMining:
    def __init__(self, year):
        self.year = year


    def load_data(self, filename):
        try:
            return pd.read_csv(filename)
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return None
        
    def convert_trades(self, file, players_traded):
        data = self.load_data(file)
        

        # Create bins for statistics
        data['PER_bin'] = pd.cut(data['PER'], bins=[0, 15, 20, 25, 100], labels=['PER<15', '15<=PER<20', '20<=PER<25', 'PER>=25'])
        data['BPM_bin'] = pd.cut(data['BPM'], bins=[-10, -5, 0, 5, 10], labels=['BPM<-5', '-5<=BPM<0', '0<=BPM<5', 'BPM>=5'])
        data['VORP_bin'] = pd.cut(data['VORP'], bins=[0, 5, 10, 15, 20], labels=['VORP<5', '5<=VORP<10', '10<=VORP<15', 'VORP>=15'])
        data['WS_bin'] = pd.cut(data['WS'], bins=[0, 5, 10, 15, 20], labels=['WS<5', '5<=WS<10', '10<=WS<15', 'WS>=15'])
        #data['PTS_bin'] = pd.cut(data['PTS'], bins=[0, 10, 20, 30, 40], labels=['PTS<10', '10<=PTS<20', '20<=PTS<30', 'PTS>=30'])
        #data['AST_bin'] = pd.cut(data['AST'], bins=[0, 5, 10, 15, 20], labels=['AST<5', '5<=AST<10', '10<=AST<15', 'AST>=15'])
        #data['TRB_bin'] = pd.cut(data['TRB'], bins=[0, 5, 10, 15, 20], labels=['TRB<5', '5<=TRB<10', '10<=TRB<15', 'TRB>=15'])
        #data['MP_bin'] = pd.cut(data['MP'], bins=[0, 10, 20, 30, 40], labels=['MP<10', '10<=MP<20', '20<=MP<30', 'MP>=30'])
        #data['WLp_bin'] = pd.cut(data['WLp'], bins=[0, 0.25, 0.5, 0.75, 1], labels=['WLp<0.25', '0.25<=WLp<0.5', '0.5<=WLp<0.75', 'WLp>=0.75'])
        #data['SRS_bin'] = pd.cut(data['SRS'], bins=[-10, -5, 0, 5, 10], labels=['SRS<-5', '-5<=SRS<0', '0<=SRS<5', 'SRS>=5'])

        # Create a list of all bin column names
        bin_cols = ['PER_bin', 'BPM_bin', 'VORP_bin', 'WS_bin']
        transactions = []

        # For each trade, create a new transaction
        for trade in players_traded:
            transaction = []
            for player in trade:
                if player in data['Player'].values:
                    for bin_col in bin_cols:
                        bin_val = data.loc[data['Player'] == player, bin_col].values[0]
                        if pd.notnull(bin_val):
                            # Create an item that represents the player and the bin value
                            item = f"{player}_{bin_val}"
                            transaction.append(item)
            transactions.append(transaction)

        transactions = transactions[:-1]
        return transactions

    

    def visualize_rules(self, rules_df):
        plt.figure(figsize=(10, 10))

        # Scatter plot using 'support' and 'confidence' columns, and color points by 'lift'
        scatter = plt.scatter(rules_df['Support'], rules_df['Confidence'], c=rules_df['Lift'], cmap='viridis')

        plt.xlabel('Support')
        plt.ylabel('Confidence')

        # Add a colorbar
        cbar = plt.colorbar(scatter)
        cbar.set_label('Lift')

        plt.show()


        
    def fpgrowth(self, transactions):
        # Compute minimum support count as 10% of the number of transactions
        min_support_count = int(len(transactions) * 0.1)
        print(min_support_count)

        # Generate all possible combinations of 2 or 3 items from each transaction
        transactions_combinations = [list(itertools.combinations(transaction, r)) for transaction in transactions for r in range(2, 4)]
        print(len(transactions_combinations))

        # Find frequent patterns and generate rules based on these combinations
        patterns = pyfpgrowth.find_frequent_patterns(transactions_combinations, min_support_count)
        print(len(patterns))
        rules_dict = pyfpgrowth.generate_association_rules(patterns, 0.7)

        # Compute the support of each itemset as a fraction of the total number of transactions
        support = {itemset: count / len(transactions) for itemset, count in patterns.items()}

        # Convert rules_dict into a list of rules
        rules = []
        for antecedent in rules_dict:
            consequent, confidence = rules_dict[antecedent]
             # Compute lift
            lift = confidence / support[frozenset(consequent)] if frozenset(consequent) in support else 0
            support_antecedent = support[frozenset(antecedent)] if frozenset(antecedent) in support else 0  # Get support of antecedent
            rules.append([antecedent, consequent, support_antecedent, confidence, lift])

        # Convert rules to a DataFrame
        rules_df = pd.DataFrame(rules, columns=['Antecedent', 'Consequent', 'Support', 'Confidence', 'Lift'])

        # Save rules to a CSV file
        rules_df.to_csv(f'../../models/data/{self.year}_rules.csv', index=False)

        self.visualize_rules(rules_df)




    def run(self):
        # Load data for year
        file = f'../../data/processed/nba_{self.year}_proc.csv'

        transactions = self.convert_trades(file, trades_2023)

        self.fpgrowth(transactions)
