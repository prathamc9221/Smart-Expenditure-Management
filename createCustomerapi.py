from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/database_name'  # Replace with your database URI
db = SQLAlchemy(app)

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    Full_Name = db.Column(db.String(255), nullable=False)
    email_address = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    Income_amount = db.Column(db.Float)
    Saving_Percentage = db.Column(db.Float)

@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.form
    full_name = data.get('Full_Name')
    email = data.get('email_address')
    password = data.get('password')
    income_amount = data.get('Income_amount')
    saving_percentage = data.get('Saving_Percentage')

    try:
        new_customer = Customer(Full_Name=full_name, email_address=email, password=password,
                                Income_amount=income_amount, Saving_Percentage=saving_percentage)
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'message': 'Account created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
