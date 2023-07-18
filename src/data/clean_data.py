import pandas as pd


class CleanData:
    def __init__(self, year, outliers):
        self.year = year
        self.outliers = outliers

    def remove_outliers(self, df, column_name):
        Q1 = df[column_name].quantile(0.25)
        Q3 = df[column_name].quantile(0.75)
        IQR = Q3 - Q1

        # Only keep rows in the dataframe that are within the IQR
        df = df[~((df[column_name] < (Q1 - 1.5 * IQR)) | (df[column_name] > (Q3 + 1.5 * IQR)))]
        return df

    def run(self):

        # Load the raw data
        raw_data = pd.read_csv(f'../../data/raw/nba_{self.year}_final_raw.csv')

        # Fill missing data with a placeholder value (like 0 or 'unknown')
        cleaned_data = raw_data.fillna(0)

        # Create a new column 'MP' which is the average of 'MP_x' and 'MP_y'
        cleaned_data['MP_x'] = pd.to_numeric(cleaned_data['MP_x'], errors='coerce')
        cleaned_data['MP_y'] = pd.to_numeric(cleaned_data['MP_y'], errors='coerce')
        cleaned_data['MP'] = (cleaned_data['MP_x'] + cleaned_data['MP_y']) / 2

        # Drop the 'MP_x' and 'MP_y' columns
        cleaned_data = cleaned_data.drop(columns=['MP_x', 'MP_y'])

        # Filter out 'Unnamed' columns
        cleaned_data = cleaned_data.filter(regex='^(?!Unnamed)')

        # Reset the index and drop the original index
        cleaned_data.reset_index(drop=True, inplace=True)

        # Clean the data
        cleaned_data = cleaned_data.copy()


        #Remove not needed rows
        i = 5
        while i < len(cleaned_data):
            if cleaned_data.loc[i, 'Rk'] == 'Rk':
                cleaned_data = cleaned_data.drop(i).reset_index(drop=True)
                #print('removed', i)
            i += 1

        i = 5
        while i < len(cleaned_data):
            if cleaned_data.loc[i, 'Rk'] == 'Rk':
                cleaned_data = cleaned_data.drop(i)
                #print('removed', i)
            i += 1

        # Save cleaned data to interim folder
        cleaned_data.to_csv(f'../../data/interim/nba_{self.year}_cleaned.csv', index=False)
        print(cleaned_data.head())



        for col in cleaned_data.columns:
            # Normalize the data if the column isn't in these columns
            if col not in ['Rk','Age','Player', 'Pos','Tm', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%','PER','BPM','VORP','FTr','FG%','3P%','2P%','eFG%', 'TS%','3PAr','OWS','DWS','WS','WS/48','OBPM',	'DBPM']:
                cleaned_data[col] = pd.to_numeric(cleaned_data[col], errors='coerce')
                cleaned_data[col] = (cleaned_data[col] - cleaned_data[col].min()) / (cleaned_data[col].max() - cleaned_data[col].min())

        
        if self.outliers.lower() == 'yes':
            for column in cleaned_data.columns:
                if cleaned_data[column].dtype in ['int64', 'float64']:
                    cleaned_data = self.remove_outliers(cleaned_data, column)

            # Save the Normalized data with outliers removed
            cleaned_data.to_csv(f'../../data/interim/nba_{self.year}_normalized_or.csv', index=False)
            print(cleaned_data.head())
        else:
            # Save the Normalized data
            cleaned_data.to_csv(f'../../data/interim/nba_{self.year}_normalized.csv', index=False)
            print(cleaned_data.head())