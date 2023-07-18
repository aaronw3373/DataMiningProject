from get_data import GetData
from clean_data import CleanData
from proc_data import ProcData
from plot_compare import PlotCompare
from cor_analysis import CorrelationAnalysis
from cor_analysis_player import PlayerCorrelationAnalysis

# Ask the user for the year
year = input("Please enter the year: ")

# Ask the user for menu option
option = input("[1]: Gather, clean, and process data \n[2]: Compare Boxcharts \n[3]: Analyze Data \nSelect Option: ")


if option == '1':
    # Ask the user if they want remove outliers
    print('Selected Gather, clean, and process data')
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

elif option == '2':
    print('Selected Comparing Boxcharts')
    # Ask the user if they want to perform the comparison
    compare = input("Do you want to perform a plot comparison? (yes/no): ")
    save_fig = input("Do you want to save the figures? (yes/no): ")
    plot_compare = PlotCompare(year, compare, save_fig)
    plot_compare.run()

elif option == '3':
    print('Selected Analyze Data')
    option1 = input("[1]: League Analysis \n[2]: Player Analysis (Still in Progress) \nSelect Option: ")
    if option1 == '1':
        print('Selected League Analysis')
        outliers = input("Perform Analysis on data with outliers removed? (yes/no): ")
        simple = input("Would you like to see the simple view? (yes/no): ")
        cor_analysis = CorrelationAnalysis(year, outliers,simple)
        cor_analysis.run()
    else:
        print('Selected Player Analysis')
        players = ['Jamal Murray', 'Cole Anthony', 'Patrick Beverley', 'Chris Paul', 'Jordan Poole', 'Gabe Vincent', 'Russell Westbrook' , 'Trae Young', 'Marcus Smart','Collin Sexton']
        print('Analyzing Players: ',players)
        analysis = PlayerCorrelationAnalysis(year, outliers='no', players=players)
        analysis.run()


else:
    print(f"Option not Found.")
    pass

print('Done')