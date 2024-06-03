#PRATHAMESH CHANDRAKANT CHAUDHARI

import configparser
# Importing database objects from config
config_obj = configparser.ConfigParser()
config_obj.read("config.py")
db_config = config_obj["splitwise"]

consumer_key = db_config["consumer_key"]
consumer_secret = db_config["consumer_secret"]
oauth_token = db_config["oauth_token"]
oauth_verifier = db_config["oauth_verifier"]

from flask import Flask, request, render_template, redirect, url_for
from splitwise import Splitwise
import pandas as pd

app = Flask(__name__)

# Set your redirect URI to the URL where Splitwise will redirect after authorization
redirect_uri = 'http://localhost:5000/auth_callback'

# Flask secret key for session
app.secret_key = 'abc'

# Splitwise object
sObj = Splitwise(consumer_key, consumer_secret)

@app.route('/')
def index():
    # Step 1: Obtain the oauth_token
    request_token = sObj.getRequestToken()
    auth_url = sObj.getAuthorizeURL(request_token)
    return redirect(auth_url)

@app.route('/auth_callback')
def auth_callback():
    oauth_token = request.args.get('oauth_token')
    oauth_token_secret = "https://secure.splitwise.com/oauth/access_token"
    oauth_verifier = request.args.get('oauth_verifier')

    access_token = sObj.getAccessToken(oauth_token, oauth_token_secret, oauth_verifier)
    sObj.setAccessToken(access_token)

    # # Fetch user's expenses
    # expenses = sObj.getExpenses()
    
    # # Convert expenses data to a Pandas DataFrame
    # expenses_data = []
    # for expense in expenses:
    #     expenses_data.append({
    #         'Description': expense.description,
    #         'Amount': expense.cost.amount,
    #         'Currency': expense.cost.currency_code,
    #         'Date': expense.date,
    #         'Category': expense.category.name if expense.category else None
    #     })
    # df = pd.DataFrame(expenses_data)

    # # Save expenses to Excel sheet
    # df.to_excel('user_expenses.xlsx', index=False)

    return 'Expenses fetched and saved to Excel sheet.'

if __name__ == '__main__':
    app.run(debug=True)
