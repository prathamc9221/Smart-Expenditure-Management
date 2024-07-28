#PRATHAMESH CHANDRAKANT CHAUDHARI
#Associated with Binghamton University

import pandas as pd
import my_connection
from datetime import datetime


def get_monthy_cost_distribution(user_email):
    # Get the current date
    current_date = datetime.now()

    # Extract the month from the current date
    current_month = current_date.month

    print("Current Month:", current_month)


    query = "select * from Transactions where customer_id = (select customer_id from Customer where email_address = '" + user_email + "')"
    transactions = my_connection.select_all(query)

    headers = ['Date', 'Description', 'Category', 'Cost', 'Currency', 'customer_id']

    df = pd.DataFrame(transactions, columns=headers)
    print(df)

    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

    # Replace empty strings with NaN in the 'Cost' column
    df['Cost'] = df['Cost'].replace('', pd.NA)

    # Convert the 'Cost' column to float
    df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')

    # Get the current month
    current_month = datetime.now().month

    # Filter the DataFrame for rows in the current month
    filtered_df = df[df['Date'].dt.month == current_month]



    unique_categories = filtered_df['Category'].unique()
    # print(unique_categories)
    total_sum = 0
    categorical_data = {}
    for i in unique_categories:
        cat_df = filtered_df[filtered_df['Category'] == i]
        total_cost_per_cat = cat_df['Cost'].sum()
        total_sum += total_cost_per_cat
        categorical_data[i] = total_cost_per_cat
    
    categorical_data_percentage = {}
    for i in unique_categories:
        total_cost_per_cat = categorical_data[i]
        categorical_data_percentage[i] = (total_cost_per_cat/total_sum) * 100
    
    print("categorical_data=", categorical_data)
    print("categorical_data_percentage=", categorical_data_percentage)

    # # # Display the total cost for each category
    return categorical_data_percentage

def calculate_category_budgets(user_income, unique_categories, savings=0):
    num_categories = len(unique_categories)
    total_budget = (user_income - savings) / num_categories
    category_budgets = {}
    for i in unique_categories:
        category_budgets[i] = total_budget
    return category_budgets

def Expense_management_score(user_email):
    
    query = "select customer_id, Income_amount, Saving_Percentage from Customer where email_address = '" + user_email + "'"
    customer = my_connection.select_all(query)
    
    user_income = float(customer[0][1])
    Saving_Percentage = float(customer[0][2])
    
    # savings = user_income * Saving_Percentage
    
    
    
    query = "select * from Transactions where customer_id = (select customer_id from Customer where email_address = '" + user_email + "')"
    transactions = my_connection.select_all(query)

    headers = ['Date', 'Description', 'Category', 'Cost', 'Currency', 'customer_id']
    df = pd.DataFrame(transactions, columns=headers)
    print("df=", df)

    unique_categories = df['Category'].unique()
    
    # Calculate total expenses for each category
    # category_expenses = df.groupby('Category')['Cost'].sum()

    # Initialize total score
    total_score = 0

    # num_categories = len(unique_categories)
    # print("num_categories=", num_categories)
    # category_budgets = calculate_category_budgets(user_income, unique_categories, savings)
    
    # print("category_budgets=", category_budgets)
    
    # Get the current date
    current_date = datetime.now()

    # Extract the month from the current date
    current_month = current_date.month

    print("Current Month:", current_month)
    
    filtered_df = df[df['Date'].dt.month == current_month]
    print()
    
    total_sum = 0
    categorical_data = {}
    for i in unique_categories:
        cat_df = filtered_df[filtered_df['Category'] == i]
        total_cost_per_cat = cat_df['Cost'].sum()
        total_sum += total_cost_per_cat
        categorical_data[i] = total_cost_per_cat
    
    print("total_sum=", total_sum)
    final_savings = user_income - total_sum
    
    final_savings_percentage = final_savings/user_income
    
    print(final_savings_percentage)

    targeted_saving_percentage = Saving_Percentage  
    # # Iterate over each category
    # for category, budget in category_budgets.items():
    #     # If the category exists in the dataset
    #     if category in unique_categories:
    #         print("total_score= ", total_score)
    #         expenses = category_expenses[category]
    #         # If expenses exceed the budget
    #         if expenses > budget:
    #             # Deduct points (you can adjust this based on your preference)
    #             deduction = (expenses - budget) * 100 / user_income
    #             total_score -= deduction
    #         else:
    #             # Give some positive points for staying within budget
    #             total_score += 10  # You can adjust this as needed
    #     else:
    #         print(f"Category '{category}' not found in the dataset.")
    
    

    return float(final_savings_percentage), targeted_saving_percentage
