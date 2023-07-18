from decision_tree import DecisionTreeAnalysis

# Ask the user for the year
year = input("Please enter the year: ")

# Ask the user for menu option
option = input("[1]: Perform Decision Tree Analysis \nSelect Option: ")


if option == '1':
    print(f"Performing Decision Tree Analysis")
    decision_tree = DecisionTreeAnalysis(year)
    decision_tree.run()
else:
    print(f"Option not Found.")
    pass

print('Done')