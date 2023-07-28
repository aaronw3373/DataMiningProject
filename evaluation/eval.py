import numpy as np
import pandas as pd

import getStats
import matplotlib.pyplot as plt

year1 = 2022
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
def TVavg(stats, model):
	if model is None:
		feature = 'Trade Value'
	else:
		if not model in ['DecisionTree', 'RandomForest', 'GradientBoosting']:
			raise KeyError(f"Unknown model: '{model}'")
		feature = f'Predicted Trade Value ({model})'
	vals = []
	tvdf = pd.read_csv(f'../models/data/nba_predicted_trade_values_{year1}.csv')
	print(tvdf)
	for team in getStats.NBAteams.values(): # defines order
		total = 0
		count = 0
		for player in stats[team]['roster']:
			playerstats = tvdf.loc[tvdf['Player'] == player]
			if len(playerstats) == 0: continue
			count += 1
			total += playerstats.at[playerstats.index[0], feature]
		vals.append(total)
	return vals


# list of changes in team averages of player trade value
def deltaTVavg(statsA, statsB, model):
	avgsA = TVavg(statsA, model)
	avgsB = TVavg(statsB, model)
	return np.subtract(avgsB, avgsA)

statsA = getStats.getInfo(year1)
statsB = getStats.getInfo(year2)

usemodel = 'RandomForest'

tvs = deltaTVavg(statsA, statsB, usemodel)
wls = deltaWL(statsA, statsB)
srss = deltaSRS(statsA, statsB)

print("W/L%")
Pcorr = np.corrcoef(tvs, wls)
print("SRS")
Pcorr = np.corrcoef(tvs, srss)

print(Pcorr)


plt.plot(tvs, wls, 'ro')
plt.title(f'Team Average Trade Value Change v.s. Team Win/Loss Ratio Change ({year1} - {year2}) ')
plt.xlabel(f'Team Average Trade Value Change ({year1} - {year2})')
plt.ylabel(f'Team Win/Loss Ratio Change ({year1} - {year2})')
plt.show()