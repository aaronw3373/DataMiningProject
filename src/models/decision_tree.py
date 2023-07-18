import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler

class DecisionTreeAnalysis:
    def __init__(self, year):
        self.year = year

    def load_data(self, filename):
        try:
            return pd.read_csv(filename)
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return None
        
    

    def calculate_trade_value(self, data, cols_to_scale):
        # Define the weights for the normalized statistics
        weights = {
            'PER': 0.3,
            'WS': 0.25,
            'BPM': 0.15,
            'VORP': 0.1,
            'PTS': 0.05,
            'AST': 0.05,
            'TRB': 0.05,
            'MP': 0.025,
            'Age': -0.025
        }

        # Apply Z-Scaling to the selected columns
        scaler = StandardScaler()
        data_scaled = data.copy()
        data_scaled[cols_to_scale] = scaler.fit_transform(data[cols_to_scale])

        # Compute the trade value for each row
        trade_value = sum(data_scaled[col] * weight for col, weight in weights.items())

        return trade_value


    def perform_analysis(self, data):
        # Calculate the trade value for each player
        cols_to_scale = ['Age', 'PER', 'BPM', 'VORP', 'WS', 'PTS', 'AST', 'TRB', 'MP']
        data['Trade Value'] = self.calculate_trade_value(data, cols_to_scale)
        # Split the data into train and test sets
        X = data[['Age', 'PER', 'BPM', 'VORP', 'WS', 'PTS', 'AST', 'TRB', 'MP']]
        y = data['Trade Value']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initialize the decision tree regressor and fit it to the training data
        tree = DecisionTreeRegressor(random_state=42)
        tree.fit(X_train, y_train)

        # Predict Player Trade Value for the test set and calculate the R^2 score
        predictions = tree.predict(X_test)
        r2_score = tree.score(X_test, y_test)

        print(f'R^2 score of the decision tree model: {r2_score}')

        # Perform cross-validation
        scores = cross_val_score(tree, X, y, cv=5)

        print(f'Cross-Validation R^2 scores: {scores}')
        print(f'Average R^2 score: {scores.mean()}')

    def run(self):
        file = f'../../data/processed/nba_{self.year}_proc_or.csv'

        data = self.load_data(file)

        if data is not None:
            self.perform_analysis(data)