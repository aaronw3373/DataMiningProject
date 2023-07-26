import requests
from bs4 import BeautifulSoup
import pandas as pd
import pickle
import time
import os

# Static dict of Abbreviation to team names
NBAteams = {'ATL' : 'Atlanta Hawks',
'BOS' : 'Boston Celtics',
'BRK' : 'Brooklyn Nets',
'CHO' : 'Charlotte Hornets',
'CHI' : 'Chicago Bulls',
'CLE' : 'Cleveland Cavaliers',
'DAL' : 'Dallas Mavericks',
'DEN' : 'Denver Nuggets',
'DET' : 'Detroit Pistons',
'GSW' : 'Golden State Warriors',
'HOU' : 'Houston Rockets',
'IND' : 'Indiana Pacers',
'LAC' : 'Los Angeles Clippers',
'LAL' : 'Los Angeles Lakers',
'MEM' : 'Memphis Grizzlies',
'MIA' : 'Miami Heat',
'MIL' : 'Milwaukee Bucks',
'MIN' : 'Minnesota Timberwolves',
'NOP' : 'New Orleans Pelicans',
'NYK' : 'New York Knicks',
'OKC' : 'Oklahoma City Thunder',
'ORL' : 'Orlando Magic',
'PHI' : 'Philadelphia 76ers',
'PHO' : 'Phoenix Suns',
'POR' : 'Portland Trail Blazers',
'SAC' : 'Sacramento Kings',
'SAS' : 'San Antonio Spurs',
'TOR' : 'Toronto Raptors',
'UTA' : 'Utah Jazz',
'WAS' : 'Washington Wizards',}

# Fetching team rosters for given year
def fetchRosters(year):
	rosters = {}
	for abr, name in NBAteams.items():
		# Define the URL of the page
		url = f"https://www.basketball-reference.com/teams/{abr}/{year}.html"
		# Send a GET request
		response = requests.get(url)
		# If the GET request is successful, the status code will be 200
		if response.status_code == 200:
			# Get the content of the response
			webpage = response.text
			# Create a Beautiful Soup object and specify the parser
			soup = BeautifulSoup(webpage, 'html.parser')
			# Find the table with the stats. You can find these details by inspecting the webpage
			table = soup.find('table', {'id': 'roster'})
			# Create a data frame by reading the HTML table
			ros_df = pd.read_html(str(table))[0]
			# save roster to dict
			rosters[name] = []
			for index, row in ros_df.iterrows():
				rosters[name].append(row['Player'].rstrip('(TW)'))
		else:
			print(f"Error fetching {name} roster: {response.status_code} : {response.reason}")
			print(f"  {url}")
		# Respectful crawling by sleeping (this value was gathered by looking up https://www.basketball-reference.com/robots.txt)
		time.sleep(3)
	# return roster
	return rosters

# Fetching team Win/Loss and SRS
def fetchStats(year):
	stats = {}
	# Define the URL of the page
	url = f"https://www.basketball-reference.com/leagues/NBA_{year}.html"
	# Send a GET request
	response = requests.get(url)
	# If the GET request is successful, the status code will be 200
	if response.status_code == 200:
		# Get the content of the response
		webpage = response.text
		# Create a Beautiful Soup object and specify the parser
		soup = BeautifulSoup(webpage, 'html.parser')
		# Find the table with the stats. You can find these details by inspecting the webpage
		Etable = soup.find('table', {'id': 'confs_standings_E'})
		Wtable = soup.find('table', {'id': 'confs_standings_W'})
		# Create a data frame by reading the HTML table
		E_df = pd.read_html(str(Etable))[0]
		W_df = pd.read_html(str(Wtable))[0]
		# save W/L and SRS to dict
		for index, row in E_df.iterrows():
			stats[row[0].rstrip('*')] = {'W/L': float(row[3]), 'SRS': float(row[7])}
		for index, row in W_df.iterrows():
			stats[row[0].rstrip('*')] = {'W/L': float(row[3]), 'SRS': float(row[7])}
	else:
		print(f"Error fetching stats: {response.status_code} : {response.reason}")
	# return stats
	return stats

# Get team rosters and w/l for given year from storage or remote
def getInfo(year):
	# try local storage first
	# Ensure directory exists, if not, create it
    os.makedirs('./data', exist_ok=True)
    # check if file exits for year
    statPath = f"./data/team_stats_{year}.pkl"
    if os.path.isfile(statPath):
    	# load local data
    	with open(statPath, 'rb') as inFile:
    		info = pickle.load(inFile)
    	return info
    else:
    	info = {}
    	# not local, fetch from remote
    	rosters = fetchRosters(year)
    	stats = fetchStats(year)
    	for teamName, stat in stats.items():
    		if not teamName in rosters.keys():
    			print(f"Roster not found for {teamName}")
    			continue
    		#load structure
    		info[teamName] = {'roster': rosters[teamName], 'stats': stat}
    	# save loacaly
    	with open(statPath, 'wb') as outfile:
    		pickle.dump(info, outfile)
    	return info


