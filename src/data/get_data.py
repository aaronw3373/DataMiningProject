import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

class GetData:
    def __init__(self, year):
        self.year = year

    def run(self):


        # Define the URL of the page
        url = f"https://www.basketball-reference.com/leagues/NBA_{self.year}_per_game.html"

        # Send a GET request
        response = requests.get(url)

        # If the GET request is successful, the status code will be 200
        if response.status_code == 200:
            # Get the content of the response
            webpage = response.text

            # Create a Beautiful Soup object and specify the parser
            soup = BeautifulSoup(webpage, 'html.parser')

            # Find the table with the stats. You can find these details by inspecting the webpage
            table = soup.find('table', {'id': 'per_game_stats'})

            # Create a data frame by reading the HTML table
            df = pd.read_html(str(table))[0]

            # Print the first 5 rows of the data frame
            #print(df.head())

            # Define path to the directory where you'd like to save the file
            # Make sure the directory exists beforehand, or use os.makedirs() to create it
            raw_data_path = os.path.join('../../data', 'raw')

            # Ensure directory exists, if not, create it
            os.makedirs(raw_data_path, exist_ok=True)

            # Save the data frame to a csv file in the specified directory
            df.to_csv(os.path.join(raw_data_path, f'nba_{self.year}_per_game_raw.csv'), index=False)

            print(f"Data saved to {os.path.join(raw_data_path, f'nba_{self.year}_per_game_raw.csv')}")

        # Respectful crawling by sleeping (this value was gathered by looking up https://www.basketball-reference.com/robots.txt)
        time.sleep(3)


        # Define the URL of the advanced stats page
        url_advanced = f"https://www.basketball-reference.com/leagues/NBA_{self.year}_advanced.html"

        # Send a GET request
        response_advanced = requests.get(url_advanced)

        # If the GET request is successful, the status code will be 200
        if response_advanced.status_code == 200:
            # Get the content of the response
            webpage_advanced = response_advanced.text

            # Create a Beautiful Soup object and specify the parser
            soup_advanced = BeautifulSoup(webpage_advanced, 'html.parser')

            # Find the table with the stats
            table_advanced = soup_advanced.find('table', {'id': 'advanced_stats'})

            # Create a data frame by reading the HTML table
            df_advanced = pd.read_html(str(table_advanced))[0]

            # Print the first 5 rows of the data frame
            #print(df_advanced.head())

            # Save the data frame to a csv file
            df_advanced.to_csv(os.path.join(raw_data_path, f'nba_{self.year}_advanced_raw.csv'), index=False)

            print(f"Data saved to {os.path.join(raw_data_path, f'nba_{self.year}_advanced_raw.csv')}")

        # Respectful crawling by sleeping
        time.sleep(3)


        # Merge the two datasets on 'Player' and 'Tm' columns
        df_final = pd.merge(df, df_advanced, how='inner', on=['Player', 'Tm','Rk','Pos','Age','G'])

        # Print the first 5 rows of the final data frame
        #print(df_final.head())

        # Save the final data frame to a csv file
        df_final.to_csv(os.path.join(raw_data_path, f'nba_{self.year}_final_raw.csv'), index=False)

        print(f"Data saved to {os.path.join(raw_data_path, f'nba_{self.year}_final_raw.csv')}")
