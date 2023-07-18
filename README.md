# DataMiningProject

CSCI 5502/4502 Data Mining Summer 23' Project


	NBA_Trade_Value_Project/

	|

	|--- data/

	|     |--- raw/ (contains the initial scraped data)

	|     |--- interim/ (contains data that is in the middle of processing)

	|     |--- processed/ (contains clean, processed data ready for analysis)

	|

	|--- models/ 
 
	|     |--- data/ (test and train data for the models)

	|

	|--- src/ (source code for use in this project)

	|     |--- data/ (scripts to download or generate data)

	|     |--- features/ (scripts to turn processed data into features for modeling)

	|     |--- models/ (scripts to train models and then use trained models to make predictions)

	|

	|--- output/

	      |--- figures/ (graphs, plots for reporting)
       
	      |     |--- year/ 
       
	      |     |     |--- outliers/ 
	      
	      |     |     |--- outliers_removed/ 
	      
	      |     |     |--- comparison/ (comparison between data with outliers and data with outliers removed)
      
	      |--- models/ (trained and serialized models, model predictions, or model summaries)

## How to Run Data Collection/ Compare Figures
Go to the right directory

	cd \src\data

run

 	python main.py

The User will be asked which year they are interested in.


The User will then be given an option to gather, clean, and process data (yes/no)


If yes, the User will be asked if they want to remove outliers (yes/no)

If no, the User will be asked if they want to compare data (yes/no) 

-- **[Both saved graphs for outliers and outliers removed for that year must exist]**


## Authors
Tristan Swanson - tristan.swanson@colorado.edu
Demetrius Ross - dero0816@colorado.edu
Aaron Weinberg - aaron.weinberg@colorado.edu
