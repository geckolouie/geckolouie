''' Task : create a program that allows users to access
two different financial calculators: investment and home loan repayment.'''

import math


# This first section of my code asks the user to input either a value of 1 or 2.
# This coincides with either Bond or Investment, and proceeds to execute a message correlating with user choice.

print("Hello! \n Which services would you like to use?")
print("Investment: to calculate the amount of interest you'll earn on your investment.")
print("Bond: to calculate the amount you'll have to pay on a home loan.")

user_input = int(input("Enter 1 for 'Bond' or 2 for 'Investment' to proceed: "))

if user_input == 1:
    print("You have selected to calculate: Bond Repayment")     # The first section of my code determines what the programme will execute if the user chooses 'Bond'. The user will be instructed to input values for: house value, interest rate, and months of repayment - where then the programme will calculate the user's monthly repayment cost and output the answer.
    print("Please input the following: ")
    house_val = float(input("House Value: "))
    bond_int_rate = float(input("Interest Rate (%): "))
    num_mos = float(input("Number of repayments (mos): "))
    mos_int_rate = (bond_int_rate /100) /12
    repayment = (mos_int_rate * house_val)/(1 - (1+mos_int_rate)**(-num_mos))
     
    print("Your total repayment each month = " + (str(repayment)))
elif user_input == 2:
        print("You have selected to calculate: Investment")     # This final section of my code determines what the programme will execute if the user chooses 'Investment'. Similarly, the user will be instructed to input values for: investment, interest rate, years of investment, and whether they want to calculate simple or compound interest.
        print("Please input the following: ")
        inv_deposit = float(input("Deposit: "))
        inv_int_rate = float(input("Interest Rate (%): "))
        inv_years = float(input("Years of Investment: "))
        user_interest = int(input("Enter 1 for 'Simple' or 2 'Compound' Interest: "))

    # This section calculates either 'simple' or 'compund' interest, depending on the user's input.
        if user_interest == 1:
            print("You have chosen to calculate: 'Simple Interest'")
            interest_depo = inv_deposit /100
            simple_total = inv_deposit*(1 + interest_depo*inv_years)
            print("Your total simple interest = " + (str(simple_total)))
        
        elif user_interest == 2:
            print("You have chosen to calculate: 'Compound Interest'")
            interest_depo = inv_deposit /100
            compound_total = inv_deposit  * math.pow((1+interest_depo), inv_years)
            print("Your total compund interest = " + (str(compound_total)))
else:
    print("Error: You have not selected a service.")
