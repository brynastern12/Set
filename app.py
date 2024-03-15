from flask import Flask
import requests
from babel.dates import format_datetime
import datetime
import pytz
from setLogic1 import logic 
from db import create_table

app = Flask(__name__)

TIME_API_URL = 'https://timeapi.io/api/Time/current/zone?timeZone=Israel'

# ##def get_israel_time():
#working code
    # try:
        # response = requests.get(TIME_API_URL)
        # response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        # data = response.json()
        # iso_time = data.get('dateTime', 'Error: Time not available')
        # parsed_time = datetime.datetime.strptime(iso_time, '%Y-%m-%dT%H:%M:%S.%f')
        # return parsed_time.strftime('%Y-%m-%d %H:%M:%S')  # Adjust the format as needed
    # except Exception as e:
        # return f'Error: {e}'
def get_israel_time():
    try:
        response = requests.get(TIME_API_URL)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        data = response.json()
        iso_time = data.get('dateTime', 'Error: Time not available')
        parsed_time = datetime.strptime(iso_time[:-1], '%Y-%m-%dT%H:%M:%S')  # Removing the trailing 'Z'
        return parsed_time, None
    except Exception as e:
        return None, f'Error: {e}'

def get_israel_date():
    try:
        parsed_time, error = get_israel_time()
        if parsed_time:
            formatted_date = parsed_time.strftime('%Y-%m-%d')  # Adjust the format as needed
            return formatted_date, None
        else:
            return None, 'Error: Unable to get the date'
    except Exception as e:
        return None, f'Error: {e}'

@app.route('/')
def hello():
    israel_time = get_israel_time()
    israel_date = get_israel_date()
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Set Game</title>
        


    </head>
    <body>
        <h1>Set Game</h1>
        <p>Current time in Israel: {israel_time[0] if not israel_time[1] else israel_time[1]}</p>
        <p>Current date in Israel: {israel_date[0] if not israel_date[1] else israel_date[1]}</p>
        
        <ul>
            <!-- Hotels list will go here-->
        </ul>
        <h2>Welcome to the fun</h2>
        <form method="POST" action="/add">
            <label for="hotelsCity">City:</label>
            <input type="text" name="hotelsCity" required><br>
            <label for="hotelsName">Name:</label>
            <input type="text" name="hotelsName" required><br>
            <label for="hotelsStars">Amount of Stars:</label>
            <input type="number" name="hotelsStars" value="4" min="0" max="5" step="1" required><br>
            <button type="submit">Add Hotel</button>
        </form>
    </body>
    </html>
    '''

@app.route('/mylogic')
def my_logic():
    return logic()

@app.route('/create_table')
def create_table_route():
    create_table()  # Call the function from db.py to create the table
    return 'Table created successfully!'

if __name__ == '__main__':
    app.run(debug=True)
