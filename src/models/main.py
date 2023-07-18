from decision_tree import DecisionTreeAnalysis


# Ask the user for menu option
option = input("[1]: Perform Decision Tree Analysis \nSelect Option: ")


if option == '1':
    print(f"Performing Decision Tree Analysis")
    analysis = DecisionTreeAnalysis(2014, 2023)
    analysis.run()
else:
    print(f"Option not Found.")
    pass

print('Done')