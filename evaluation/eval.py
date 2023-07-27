import numpy as np
import pandas as pd

import getStats
import matplotlib.pyplot as plt

year1 = 2019
year2 = 2023

# list of changes in Win/Loss
def deltaWL(statsA, statsB):
	delta = []
	for team in getStats.NBAteams.values(): # defines order
		delta.append(statsB[team]['stats']['W/L'] - statsA[team]['stats']['W/L'])
	return delta

# list of changes in SRS
def deltaSRS(statsA, statsB):
	delta = []
	for team in getStats.NBAteams.values(): # defines order
		delta.append(statsB[team]['stats']['SRS'] - statsA[team]['stats']['SRS'])
	return delta

# list of team avg of player trade value
def TVavg(stats):
	vals = []
	tvdf = pd.read_csv('../models/data/nba_predicted_trade_values.csv')
	print(tvdf)
	for team in getStats.NBAteams.values(): # defines order
		total = 0
		count = 0
		for player in stats[team]['roster']:
			playerstats = tvdf.loc[tvdf['Player'] == player]
			if len(playerstats) == 0: continue
			count += 1
			total += playerstats.at[playerstats.index[0], 'Trade Value']
		vals.append(total)
	return vals


# list of changes in team averages of player trade value
def deltaTVavg(statsA, statsB):
	avgsA = TVavg(statsA)
	avgsB = TVavg(statsB)
	return np.subtract(avgsB, avgsA)

statsA = getStats.getInfo(year1)
statsB = getStats.getInfo(year2)

tvs = deltaTVavg(statsA, statsB)
wls = deltaWL(statsA, statsB)
srss = deltaSRS(statsA, statsB)

Pcorr = np.corrcoef(tvs, wls)

print(Pcorr)


plt.plot(tvs, wls, 'ro')
plt.show()