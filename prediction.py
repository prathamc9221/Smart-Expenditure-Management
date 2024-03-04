import pandas as pd

# file_path = "expense_data_1.csv"
# df = pd.read_csv(file_path)

# df['Currency'] = "USD"
# df['Amount'] = df['Amount']/50

# # Convert 'Date' column to datetime with the desired format
# df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y %H:%M')

# # Extract the date part and update the 'Date' column
# df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

# # Define a function to categorize expenses
# def categorize_expense(description):
#     if description in ["Food"]:
#         return 'Groceries'
#     elif description in ["Apparel", "Beauty"]:
#         return 'Payment'
#     elif description in ["Education"]:
#         return 'Electricity'
#     elif description in ["Household"]:
#         return 'Household supplies'
#     elif description in ["Social Life", "Self-development"]:
#         return 'Dining out'
#     else:
#         return 'General'

# # Apply the categorize_expense function to create a new 'Category' column
# df['Category'] = df['Category'].apply(categorize_expense)


# filtered_df = df[df['Income/Expense'] != 'Income']
# filtered_df = filtered_df.sort_values(by='Date')

# unique_categories = filtered_df['Category'].unique()
# print(unique_categories)

# Groceries == Food
# Payment Transportation
# General  Other, Apparel
# Household supplies == Household
# Electricity
# Dining out == Social Life


# ['Food' 'Other' 'Transportation' 'Social Life' 'Household' 'Apparel'
#  'Education' 'Salary' 'Allowance' 'Self-development' 'Beauty' 'Gift'
#  'Petty cash']
 
#  {'Groceries': 316.38000000000005, 'Payment': 268.24999999999994, 'General': 127.56, 
#   'Household supplies': 50.849999999999994, 'Electricity': 441.39, 'Dining out': 9.4, ' ': 0.0}

# Replace 'your_output_file.csv' with the desired name for the output CSV file
# output_file = 'output.csv'

# # Write the DataFrame to a CSV file
# filtered_df.to_csv(output_file, index=False)

btc = pd.read_csv("output.csv")

groceries_df = btc[btc['Category'] == 'Groceries']

groceries_df.index = pd.to_datetime(groceries_df['Date'], format='%Y-%m-%d')
print(groceries_df)
print(len(groceries_df))

train_data = groceries_df[groceries_df['Date'] <= '2022-02-18']
test_data = groceries_df[groceries_df['Date'] > '2022-02-18']

print(train_data)

# Convert 'Date' column to datetime
train_data['Date'] = pd.to_datetime(train_data['Date'])

# Create a new DataFrame with 'Month' column and sum of amounts grouped by month
df_monthly_train = train_data.groupby(train_data['Date'].dt.to_period("M")).agg({'Amount': 'sum'}).reset_index()

# Rename the columns for clarity
df_monthly_train.columns = ['Month', 'Total_Amount']

# Display the new DataFrame
print(df_monthly_train)


# Convert 'Date' column to datetime
test_data['Date'] = pd.to_datetime(test_data['Date'])

# Create a new DataFrame with 'Month' column and sum of amounts grouped by month
df_monthly_test = test_data.groupby(test_data['Date']).agg({'Amount': 'sum'}).reset_index()

# Rename the columns for clarity
df_monthly_test.columns = ['Month', 'Total_Amount']

# Display the new DataFrame
print(df_monthly_test)



import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.statespace.sarimax import SARIMAX

print(type(df_monthly_train['Total_Amount']))

# plt.plot(df_monthly_train, color = "black")
# plt.plot(df_monthly_test, color = "red")
# plt.ylabel('Total Amount')
# plt.xlabel('Month')
# plt.xticks(rotation=45)
# plt.title("Train/Test split for BTC Data")
# plt.show()


y = df_monthly_train['Total_Amount']
ARMAmodel = SARIMAX(y, order = (1, 0, 1))
ARMAmodel = ARMAmodel.fit()
y_pred  = ARMAmodel.get_forecast(len(df_monthly_test.index))
y_pred_df = y_pred.conf_int(alpha = 0.05) 
y_pred_df["Predictions"] = ARMAmodel.predict(start = y_pred_df.index[0], end = y_pred_df.index[-1])
y_pred_df.index = df_monthly_test.index
y_pred_out = y_pred_df["Predictions"] 

plt.plot(y_pred_out, color='green', label = 'Predictions')
plt.legend()

print(y_pred_out)

# sns.set()
