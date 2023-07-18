import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_score

class DecisionTreeAnalysis:
    def __init__(self, year):
        self.year = year

    def load_data(self, filename):
        try:
            return pd.read_csv(filename)
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return None

    def perform_analysis(self, data):
        # Split the data into train and test sets
        X = data[['Age', 'BPM', 'VORP', 'WS', 'PTS', 'AST', 'TRB', 'MP']]
        y = data['PER']
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