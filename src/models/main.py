from decision_tree import DecisionTreeAnalysis
from association_mining import AssociationRuleMining


# Ask the user for menu option
option = input("[1]: Perform Decision Tree Analysis \n[2]: Perform Association Rule Mining \nSelect Option: ")


if option == '1':
    print(f"Performing Decision Tree Analysis")
    analysis = DecisionTreeAnalysis(2014, 2023)
    analysis.run()
elif option == '2':
    print(f"Performing Association Rule Mining")
    rule_mining = AssociationRuleMining(2023)
    rule_mining.run()
else:
    print(f"Option not Found.")
    pass

print('Done')