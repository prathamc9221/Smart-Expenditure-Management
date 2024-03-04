import configparser
import my_connection
import preprocessing
from datetime import datetime
# Importing database objects from config
config_obj = configparser.ConfigParser()
config_obj.read("config.py")
db_config = config_obj["splitwise"]

consumer_key = db_config["consumer_key"]
consumer_secret = db_config["consumer_secret"]
oauth_token = db_config["oauth_token"]
oauth_verifier = db_config["oauth_verifier"]

from flask import Flask, jsonify, render_template, redirect, request, url_for, session
import secrets
from splitwise import Splitwise
import pandas as pd
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)

# Replace these with your actual Splitwise credentials
callback_url = "http://localhost:5050/callback"

splitwise = Splitwise(consumer_key, consumer_secret)
url, secret = splitwise.getAuthorizeURL()
# splitwise.set_callback_url(callback_url)

app.secret_key = "abc"


@app.route('/')
def index():
    # Get request token and its secret
    request_token, request_token_secret = splitwise.get_request_token()
    
    print("request_token= ", request_token)
    print("request_token_secret= ", request_token_secret)

    # Store request_token_secret in the Flask session
    session['request_token_secret'] = request_token_secret

    # Save the request_token for later use
    # (This is a simplified example; you might need to store it securely)
    session['request_token'] = request_token

    # Redirect the user to the authorization URL
    auth_url = splitwise.build_authorize_url(request_token, oauth_callback=callback_url)
    return f'<a href="{auth_url}">Authorize with Splitwise</a>'


@app.route('/callback2')
def callback2():
    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')
    
    print("oauth_token= ", oauth_token)
    print("oauth_verifier= ", oauth_verifier)

    # Retrieve the request_token and request_token_secret saved during the initial authorization
    request_token = session.pop('request_token', None)
    request_token_secret = session.pop('request_token_secret', None)

    if request_token is None or request_token_secret is None:
        return 'Error: Missing request_token or request_token_secret'

    # Use the request token and verifier to get the access token
    access_token = splitwise.getAccessToken(oauth_token,request_token_secret,oauth_verifier)
    
    
    # access_token = splitwise.getAccessToken(oauth_verifier)

    # Use the access_token to fetch user expenses
    expenses = splitwise.getExpenses()

    # Convert expenses to a Pandas DataFrame
    
    expense_data = []
    for expense in expenses:
        expense_data.append({
            'Description': expense.description,
            'Amount': expense.cost.amount,
            'Currency': expense.cost.currency_code,
            'Date': expense.date,
            'Category': expense.category.name if expense.category else None
        })

    df = pd.DataFrame(expense_data)

    # Save the DataFrame to an Excel sheet
    df.to_excel('user_expenses.xlsx', index=False)

    return 'Expenses fetched and saved to Excel sheet successfully!'


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data['email']
        password = data['password'] 
        
        query = "SELECT customer_id,Full_Name FROM Customer WHERE email_address = '" + email + "' AND password = '" + password + "'"
        customer = my_connection.select_all(query)
       
        if customer[0][0]:            
            # cur = mysql.connection.cursor()
            # cur.execute("SELECT Category, SUM(Cost) Expense FROM transactions WHERE customer_id = %s GROUP BY category", (customer[0]))
            # customer = cur.fetchone()
            # cur.close()
            # customer_data = {
            #     'Category': customer[0],
            #     'Expense': customer[1],
            # }
            return jsonify({"success": "success", 
                            "name": customer[0][1],
                            "email": email}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.json
    full_name = data['name']
    email = data['email_address']
    password = data['password']
    income_amount = str(data['Income_amount'])
    saving_percentage = str(data['Saving_Percentage'])
    print(saving_percentage)

    try:
        # data = ('Anagha', 'aghate@gmail.com', 'newpassword', 6000.00, 10.75)
        new_customer = (full_name, email, password, income_amount, saving_percentage)
        # new_customer = Customer(Full_Name=full_name, email_address=email, password=password,
        #                         Income_amount=income_amount, Saving_Percentage=saving_percentage)
        
        my_connection.insert_into_customer(new_customer)
        return jsonify({'message': 'Account created successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@app.route('/pie_chart', methods=['POST'])
def pie_chart(): 
    try:
        data = request.json
        email = data['email_address']
        categorical_data_percentage = preprocessing.get_monthy_cost_distribution(email)
        print("categorical_data_percentage=", categorical_data_percentage)
        return jsonify({'categorical_data_percentage': categorical_data_percentage}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/expense_management_score', methods=['POST'])
def Expense_management_score(): 
    try:
        data = request.json
        email = data['email_address']
        final_savings_percentage, targeted_saving_percentage = preprocessing.Expense_management_score(email)
        return jsonify({'final_savings_percentage': final_savings_percentage,
                        "targeted_saving_percentage": targeted_saving_percentage,
                        "email": email}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/add_expense', methods=['POST'])
def add_expense(): 
    try:
        data = request.json
        # current_date = data['date']
        user_email = data['email_address']
        description = data['description']
        category = data["category"]
        cost = data["cost"]
        currency = data["currency"]
        
        query = "select customer_id from Customer where email_address = '" + user_email + "'"
        customer = my_connection.select_all(query)
        customer_id = customer[0][0]
        # Get the current date
        current_date = datetime.now()
        
        data = (current_date, description, category, cost, currency, customer_id)
        my_connection.insert_into_transactions(data)        
        
        return jsonify({"sucess": "Expenses added!"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5050)