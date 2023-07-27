from decision_tree import DecisionTreeAnalysis
from comparison import Comparison


# Ask the user for menu option
option = input("[1]: Perform Decision Tree Analysis \n[2]: Perform Comparison \nSelect Option: ")


if option == '1':
    print(f"Performing Decision Tree Analysis")
    analysis = DecisionTreeAnalysis(2014, 2022)
    analysis.run()
elif option == '2':
    print(f"Performing Comparison (2023-2022)")
    comparison = Comparison(2023)
    comparison.run()
else:
    print(f"Option not Found.")
    pass

print('Done')