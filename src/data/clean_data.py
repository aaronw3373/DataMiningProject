import pandas as pd

team_data = {
    'MIL': {'W/L%': .707, 'SRS': 3.61},
    'BOS': {'W/L%': .695, 'SRS': 6.38},
    'PHI': {'W/L%': .659, 'SRS': 4.37},
    'CLE': {'W/L%': .622, 'SRS': 5.23},
    'NYK': {'W/L%': .573, 'SRS': 2.99},
    'BRK': {'W/L%': .549, 'SRS': 1.03},
    'MIA': {'W/L%': .537, 'SRS': -0.13},
    'ATL': {'W/L%': .500, 'SRS': 0.32},
    'TOR': {'W/L%': .500, 'SRS': 1.59},
    'CHI': {'W/L%': .488, 'SRS': 1.37},
    'IND': {'W/L%': .427, 'SRS': -2.91},
    'WAS': {'W/L%': .427, 'SRS': -1.06},
    'ORL': {'W/L%': .415, 'SRS': -2.39},
    'CHO': {'W/L%': .329, 'SRS': -5.89},
    'CHA': {'W/L%': .329, 'SRS': -5.89},
    'DET': {'W/L%': .207, 'SRS': -7.73},
    'DEN': {'W/L%': .646, 'SRS': 3.04},
    'MEM': {'W/L%': .622, 'SRS': 3.60},
    'SAC': {'W/L%': .585, 'SRS': 2.30},
    'PHO': {'W/L%': .549, 'SRS': 2.08},
    'LAC': {'W/L%': .537, 'SRS': 0.31},
    'GSW': {'W/L%': .537, 'SRS': 1.66},
    'LAL': {'W/L%': .524, 'SRS': 0.43},
    'MIN': {'W/L%': .512, 'SRS': -0.22},
    'NOP': {'W/L%': .512, 'SRS': 1.63},
    'OKC': {'W/L%': .488, 'SRS': 0.96},
    'DAL': {'W/L%': .463, 'SRS': -0.14},
    'UTA': {'W/L%': .451, 'SRS': -1.03},
    'POR': {'W/L%': .402, 'SRS': -3.96},
    'HOU': {'W/L%': .268, 'SRS': -7.62},
    'SAS': {'W/L%': .268, 'SRS': -9.82},
}

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

        i = 0
        while i < len(cleaned_data):
            if cleaned_data.loc[i, 'Tm'] == 'TOT':
                cleaned_data = cleaned_data.drop(i).reset_index(drop=True)
                
            i += 1

        i = 0
        while i < len(cleaned_data):
            if cleaned_data.loc[i, 'Tm'] == 'TOT':
                cleaned_data = cleaned_data.drop(i)
                
            i += 1




            


        
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
        #print(cleaned_data.head())



        for col in cleaned_data.columns:
            # Normalize the data if the column isn't in these columns
            if col not in ['Rk','Age','Player', 'Pos','Tm', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%','PER','BPM','VORP','FTr','FG%','3P%','2P%','eFG%', 'TS%','3PAr','OWS','DWS','WS','WS/48','OBPM',	'DBPM','WLp','SRS']:
                cleaned_data[col] = pd.to_numeric(cleaned_data[col], errors='coerce')
                cleaned_data[col] = (cleaned_data[col] - cleaned_data[col].min()) / (cleaned_data[col].max() - cleaned_data[col].min())

        cleaned_data['WLp'] = cleaned_data['Tm'].map(lambda x: team_data[x]['W/L%'])
        cleaned_data['SRS'] = cleaned_data['Tm'].map(lambda x: team_data[x]['SRS'])

        i = 0
        while i < len(cleaned_data):
            if cleaned_data.loc[i, 'MP'] <= 0.05:
                cleaned_data = cleaned_data.drop(i).reset_index(drop=True)
                #print('removed', i)
            i += 1

        i = 0
        while i < len(cleaned_data):
            if cleaned_data.loc[i, 'MP'] <= 0.05:
                cleaned_data = cleaned_data.drop(i)
                #print('removed', i)
            i += 1
        
        if self.outliers.lower() == 'yes':
            for column in cleaned_data.columns:
                if cleaned_data[column].dtype in ['int64', 'float64']:
                    cleaned_data = self.remove_outliers(cleaned_data, column)

            # Save the Normalized data with outliers removed
            cleaned_data.to_csv(f'../../data/interim/nba_{self.year}_normalized_or.csv', index=False)
            #print(cleaned_data.head())
        else:
            # Save the Normalized data
            cleaned_data.to_csv(f'../../data/interim/nba_{self.year}_normalized.csv', index=False)
            #print(cleaned_data.head())