from get_data import GetData
from clean_data import CleanData
from proc_data import ProcData

# Ask the user for the year
year = input("Please enter the year: ")
# Ask the user if they want to graph the visualizations
outliers = input("Do you want to remove outliers (yes/no): ")


# Get the data
get_data = GetData(year)
get_data.run()

# Clean the data
clean_data = CleanData(year, outliers)
clean_data.run()

# Process the data
proc_data = ProcData(year, outliers)
proc_data.run()