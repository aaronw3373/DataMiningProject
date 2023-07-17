import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Define the URL of the page
url = "https://www.basketball-reference.com/leagues/NBA_2023_per_game.html"

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
    print(df.head())

    # Define path to the directory where you'd like to save the file
    # Make sure the directory exists beforehand, or use os.makedirs() to create it
    raw_data_path = os.path.join('DataMiningProject', 'data', 'raw')

    # Ensure directory exists, if not, create it
    os.makedirs(raw_data_path, exist_ok=True)

    # Save the data frame to a csv file in the specified directory
    df.to_csv(os.path.join(raw_data_path, 'nba_2023_per_game_raw.csv'), index=False)

    print(f"Data saved to {os.path.join(raw_data_path, 'nba_2023_per_game_raw.csv')}")

# Respectful crawling by sleeping (this value was gathered by looking up https://www.basketball-reference.com/robots.txt)
time.sleep(3)
