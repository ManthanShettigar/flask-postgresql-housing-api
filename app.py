import json
from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# PostgreSQL database connection details
conn = psycopg2.connect(
    host="localhost",
    database="database",
    user=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD']
)
cur = conn.cursor()

# Create the table if it doesn't exist
cur.execute('DROP TABLE IF EXISTS houses;')
cur.execute('CREATE TABLE houses (bedrooms int, bathrooms int, square_footage int, location varchar, sale_price int);')



with open("housing_data.json") as f:
    data = json.load(f)


records = []
for house in data["data"]:
    records.append((house["Bedrooms"], house["Bathrooms"], house["SquareFootage"], house["Location"], house["SalePrice"]))

# Insert the records into the database
cur.executemany("INSERT INTO houses (bedrooms, bathrooms, square_footage, location, sale_price) VALUES (%s, %s, %s, %s, %s)", records)
conn.commit()



@app.route('/avg', methods=['GET'])
def get_average_sale_price():
    """
    Retrieve the average sale price using SQL query
    """
    
    select_query = "SELECT AVG(houses.sale_price) FROM houses"
    cur.execute(select_query)
    result = cur.fetchone()
    average_sale_price = result[0]
    
    if average_sale_price is None:
        # No houses in the database, so return a 404 error
        return jsonify({'error': 'No houses found'}), 404
    else:
        return jsonify({'average_sale_price': average_sale_price})


@app.route('/avglocation', methods=['GET'])
def get_average_sale_price_per_location():
    """
        Retrieve the average sale price per location 
    """
    select_query = "SELECT location, AVG(sale_price) FROM houses GROUP BY location"
    cur.execute(select_query)
    result = cur.fetchall()
    average_sale_prices = {row[0]: row[1] for row in result}

    if len(average_sale_prices) == 0:
        # No houses in the database, so return a 404 error
        return jsonify({'error': 'No houses found'}), 404
    else:
        return jsonify({'average_sale_prices': average_sale_prices})


@app.route('/max', methods=['GET'])
def get_max_sale_price():
    """ 
    Retrieve the maximum sale price

    """

    select_query = "SELECT MAX(sale_price) FROM houses"
    cur.execute(select_query)
    result = cur.fetchone()
    max_sale_price = result[0]


    if max_sale_price is None:
        # No houses in the database, so return a 404 error
        return jsonify({'error': 'No houses found'}), 404
    else:
        return jsonify({'max_sale_price': max_sale_price})


@app.route('/min', methods=['GET'])
def get_min_sale_price():
    """
    Retrieve the minimum sale price 
    """
    select_query = "SELECT MIN(sale_price) FROM houses"
    cur.execute(select_query)
    result = cur.fetchone()
    min_sale_price = result[0]

    if min_sale_price is None:
        # No houses in the database, so return a 404 error
        return jsonify({'error': 'No houses found'}), 404
    else:
        return jsonify({'min_sale_price': min_sale_price})


def handle_error(e):
    """Handles errors and returns a JSON response with the error message."""

    error_message = {'error': str(e)}
    status_code = 500

    if isinstance(e, psycopg2.Error):
        # A database error occurred
        status_code = 500
    elif isinstance(e, KeyError):
        # A key error occurred
        status_code = 404

    return jsonify(error_message), status_code


@app.errorhandler(Exception)
def handle_all_errors(e):
    """Handles all errors and returns a JSON response with the error message."""

    return handle_error(e)


if __name__ == '__main__':
    app.run()