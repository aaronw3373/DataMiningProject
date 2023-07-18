import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt


class DecisionTreeAnalysis:
    def __init__(self, start_year, end_year):
        self.start_year = start_year
        self.end_year = end_year

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


    def perform_analysis(self, train_data, test_data):
        # Define the training data
        X_train = train_data[['Age', 'PER', 'BPM', 'VORP', 'WS', 'PTS', 'AST', 'TRB', 'MP']]
        y_train = train_data['Trade Value']

        # Define the testing data
        X_test = test_data[['Age', 'PER', 'BPM', 'VORP', 'WS', 'PTS', 'AST', 'TRB', 'MP']]
        y_test = test_data['Trade Value']

        # Initialize the decision tree regressor and fit it to the training data
        tree = DecisionTreeRegressor(random_state=42)
        tree.fit(X_train, y_train)

        # Predict Player Trade Value for the test set and calculate the R^2 score
        predictions = tree.predict(X_test)
        r2_score = tree.score(X_test, y_test)

        print(f'R^2 score of the decision tree model: {r2_score}')

        # Perform cross-validation
        scores = cross_val_score(tree, X_train, y_train, cv=5)

        print(f'Cross-Validation R^2 scores: {scores}')
        print(f'Average R^2 score: {scores.mean()}')

        # Calculate the RMSE
        rmse = sqrt(mean_squared_error(y_test, predictions))
        print(f'Root Mean Squared Error (RMSE) of the decision tree model: {rmse}')

        # Calculate the MAE
        mae = mean_absolute_error(y_test, predictions)
        print(f'Mean Absolute Error (MAE) of the decision tree model: {mae}')

        return predictions



    def run(self):
        # Start with an empty DataFrame
        data_training_years = pd.DataFrame()
        data_test_year = pd.DataFrame()

        # Load and concatenate data for each year
        for year in range(self.start_year, self.end_year):
            file = f'../../data/processed/nba_{year}_proc.csv'
            data_year = self.load_data(file)
            if data_year is not None:
                data_training_years = pd.concat([data_training_years, data_year], ignore_index=True)

        # Load data for test year
        file = f'../../data/processed/nba_{self.end_year}_proc.csv'
        data_test_year = self.load_data(file)

        if data_training_years is not None:
            cols_to_scale = ['Age', 'PER', 'BPM', 'VORP', 'WS', 'PTS', 'AST', 'TRB', 'MP']
            data_training_years['Trade Value'] = self.calculate_trade_value(data_training_years, cols_to_scale)

        if data_test_year is not None:
            cols_to_scale = ['Age', 'PER', 'BPM', 'VORP', 'WS', 'PTS', 'AST', 'TRB', 'MP']
            data_test_year['Trade Value'] = self.calculate_trade_value(data_test_year, cols_to_scale)

        # Perform analysis on data from all training years and test on the data from the test year
        if not data_training_years.empty and not data_test_year.empty:
            predictions = self.perform_analysis(data_training_years, data_test_year)

        # Map the predictions back to player names
        data_test_year['Predicted Trade Value'] = predictions
        print(data_test_year[['Player', 'Predicted Trade Value']])

        i = 0
        while i < len(data_test_year):
            if data_test_year.loc[i, 'MP'] <= 0.05:
                data_test_year = data_test_year.drop(i).reset_index(drop=True)
                #print('removed', i)
            i += 1

        i = 0
        while i < len(data_test_year):
            if data_test_year.loc[i, 'MP'] <= 0.05:
                data_test_year = data_test_year.drop(i)
                #print('removed', i)
            i += 1

        # Save to CSV
        data_test_year.to_csv(f'../../models/data/nba_predicted_trade_values.csv', index=False)