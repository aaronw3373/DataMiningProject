import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from itertools import combinations
import matplotlib.pyplot as plt
import numpy as np
import joblib

from math import sqrt


class DecisionTreeAnalysis:
    def __init__(self, start_year, end_year):
        self.start_year = start_year
        self.end_year = end_year
        self.all_features = ['PER', 'BPM', 'VORP', 'PTS', 'AST', 'MP', 'SRS']

    def load_data(self, filename):
        try:
            return pd.read_csv(filename)
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return None
        
    

    def calculate_trade_value(self, data, cols_to_scale):
        # Define the weights for the normalized statistics

        file = f'../../output/figures/{self.end_year}/analysis/correlation_matrix.csv'
        correlation_matrix  = self.load_data(file)

        # Drop the 'WLp' and 'SRS' columns as they are to be used to measure the success of the trade
        correlation_matrix = correlation_matrix.drop(['WLp','SRS','Age'], axis=1)

        # Compute the sum of the absolute correlations for each statistic
        sum_abs_correlations = correlation_matrix.abs().sum()

        # Normalize the sum of absolute correlations to get the weights
        weights = sum_abs_correlations / sum_abs_correlations.sum()

        # Convert the weights to a dictionary
        weights_dict = weights.to_dict()

        # Add a weight for 'Age'
        weights_dict['Age'] = -0.025

        # Use the weights calculated from the correlation matrix
        weights = weights_dict

        # Apply Z-Scaling to the selected columns
        scaler = StandardScaler()
        data_scaled = data.copy()
        data_scaled[cols_to_scale] = scaler.fit_transform(data[cols_to_scale])

        # Compute the trade value for each row
        trade_value = sum(data_scaled[col] * weight for col, weight in weights.items())

        return trade_value
    

    def plot_feature_importance(self, model, features):
        # Check if the model has feature importances
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            indices = np.argsort(importances)

            plt.figure(figsize=(12,8))
            plt.title('Feature Importances')
            plt.barh(range(len(indices)), importances[indices], color='b', align='center')
            plt.yticks(range(len(indices)), [features[i] for i in indices])
            plt.xlabel('Relative Importance')
            plt.show()
        else:
            print("The model does not have feature importances")

    def perform_analysis(self, train_data, test_data):
        # List of target variables
        targets = ['Trade Value']

        # Initialize the models
        models = [
            ('DecisionTree', DecisionTreeRegressor(random_state=42)),
            ('RandomForest', RandomForestRegressor(random_state=42)),
            ('GradientBoosting', GradientBoostingRegressor(random_state=42))
        ]

        # Initialize a dictionary to store the best score for each model and target
        best_scores = {}

        # Define the DataFrame to save the best scores
        best_scores_df = pd.DataFrame()

        features = list(self.all_features)

        # Define the training data
        X_train = train_data[features]

        # Define the testing data
        X_test = test_data[features]

        for target in targets:
            y_train = train_data[target]
            y_test = test_data[target]

            print(f"\nTarget Variable: {target}, Features: {features}\n{'-'*50}")

            for model_name, model in models:
                # Fit the model to the training data
                model.fit(X_train, y_train)

                # Predict Player Trade Value for the test set and calculate the R^2 score
                predictions = model.predict(X_test)
                r2_score = model.score(X_test, y_test)

                # Perform cross-validation
                scores = cross_val_score(model, X_train, y_train, cv=5)

                # Calculate the RMSE
                rmse = sqrt(mean_squared_error(y_test, predictions))

                # Calculate the MAE
                mae = mean_absolute_error(y_test, predictions)

                # Update the best score for this model and target, if necessary
                key = (target, model_name)
                if key not in best_scores or r2_score > best_scores[key]['r2_score']:
                    best_scores[key] = {'target': target,
                                        'model_name': model_name,
                                        'r2_score': r2_score, 
                                        'cv_scores': scores, 
                                        'rmse': rmse, 
                                        'mae': mae, 
                                        'features': features, 
                                        'predictions': predictions}

        # Convert the best_scores dictionary into a DataFrame
        best_scores_df = pd.DataFrame(best_scores).T.reset_index()

        # Rename the columns
        best_scores_df.columns = ['Target', 'Model', 'Extra1', 'Extra2', 'R^2 Score', 'Cross-Validation Scores', 'RMSE', 'MAE', 'Features', 'Predictions']

        # Drop unnecessary columns
        best_scores_df = best_scores_df.drop(['Extra1', 'Extra2'], axis=1)

        # Save the best scores DataFrame to a CSV file
        best_scores_df.to_csv(f'../../models/data/nba_best_model_scores_{self.end_year}.csv', index=False)
                 

        # Print the best scores
        for (target, model_name), result in best_scores.items():
            print(f"\nBest R^2 score for {model_name} model with target {target}: {result['r2_score']}")
            print(f"Best Cross-Validation scores: {result['cv_scores']}")
            print(f"Best RMSE: {result['rmse']}")
            print(f"Best MAE: {result['mae']}")
            print(f"Best features: {result['features']}")

        # Plot the feature importance
        #self.plot_feature_importance(model, features)

        joblib.dump(model, f'../../models/best_model_{self.end_year}.pkl')

       # Return the best predictions for each target and model
        return {(target, model_name): best_scores[(target, model_name)]['predictions'] for target in targets for model_name, _ in models}



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
            cols_to_scale = self.all_features
            data_training_years['Trade Value'] = self.calculate_trade_value(data_training_years, cols_to_scale)

        if data_test_year is not None:
            cols_to_scale = self.all_features
            data_test_year['Trade Value'] = self.calculate_trade_value(data_test_year, cols_to_scale)

        # Perform analysis on data from all training years and test on the data from the test year
        if not data_training_years.empty and not data_test_year.empty:
            predictions_dict = self.perform_analysis(data_training_years, data_test_year)

        # Map the predictions back to player names for each model
        for (target, model_name), predictions in predictions_dict.items():
            data_test_year[f'Predicted {target} ({model_name})'] = predictions

        # Save to CSV
        data_test_year.to_csv(f'../../models/data/nba_predicted_trade_values_{self.end_year}.csv', index=False)
