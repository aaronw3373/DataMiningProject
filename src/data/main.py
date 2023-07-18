from get_data import GetData
from clean_data import CleanData
from proc_data import ProcData
from plot_compare import PlotCompare

# Ask the user for the year
year = input("Please enter the year: ")



# Ask the user for option
option = input("Do you want to gather, clean, and process data? (yes/no): ")


if option.lower() == 'yes':
    # Ask the user if they want remove outliers
    outliers = input("Do you want to remove outliers? (yes/no): ")

    # Get the data
    print('gathering data from year: ', year)
    get_data = GetData(year)
    get_data.run()
    print('data successfully retrieved... ')

    # Clean the data
    print('cleaning data... ')
    clean_data = CleanData(year, outliers)
    clean_data.run()
    print('data washed and is ready to dry... ')

    # Process the data
    print('processing data... ')
    proc_data = ProcData(year, outliers)
    proc_data.run()
    print('data successfully processed... ')

else:
    # Ask the user if they want to perform the comparison
    compare = input("Do you want to perform a plot comparison? (yes/no): ")
    save_fig = input("Do you want to save the figures? (yes/no): ")
    plot_compare = PlotCompare(year, compare, save_fig)
    plot_compare.run()

print('Done')