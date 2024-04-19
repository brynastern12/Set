from flask import Flask
from flask import Flask, render_template
import requests
from babel.dates import format_datetime
import datetime
import pytz
import dateutil.parser
from db import get_db_connection, create_table

app = Flask(__name__)

TIME_API_URL_Israel = 'https://timeapi.io/api/Time/current/zone?timeZone=Israel'
TIME_API_URL_NY = 'https://timeapi.io/api/Time/current/zone?timeZone=America/New_York'

def get_israel_time():
    try:
        response = requests.get(TIME_API_URL_Israel)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        data = response.json()
        iso_time = data.get('dateTime', 'Error: Time not available')

        # Remove the milliseconds and 'T' from the time string
        cleaned_time = iso_time.split('.')[0].replace('T', ' ')

        try:
            parsed_time = datetime.datetime.strptime(cleaned_time, '%Y-%m-%d %H:%M:%S')
            return parsed_time.strftime('%I:%M %p'), None  # Adjust the format to include AM/PM
        except ValueError:
            return None, f'Error: Invalid time format: {iso_time}'
    except Exception as e:
        return None, f'Error: {e}'
        
def get_ny_time():
    try:
        response = requests.get(TIME_API_URL_NY)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        data = response.json()
        iso_time = data.get('dateTime', 'Error: Time not available')

        # Remove the milliseconds and 'T' from the time string
        cleaned_time = iso_time.split('.')[0].replace('T', ' ')

        try:
            parsed_time = datetime.datetime.strptime(cleaned_time, '%Y-%m-%d %H:%M:%S')
            return parsed_time.strftime('%I:%M %p'), None  # Adjust the format to include AM/PM
        except ValueError:
            return None, f'Error: Invalid time format: {iso_time}'
    except Exception as e:
        return None, f'Error: {e}'

def get_israel_date():
    try:
        response = requests.get(TIME_API_URL_Israel)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        data = response.json()
        iso_time = data.get('dateTime', 'Error: Time not available')

        # Extract date from ISO format string
        cleaned_date = iso_time.split('T')[0]

        try:
            parsed_date = datetime.datetime.strptime(cleaned_date, '%Y-%m-%d')
            return parsed_date.strftime('%b %d, %Y'), None  # Adjust the format for month abbreviation
        except ValueError:
            return None, f'Error: Invalid date format: {cleaned_date}'
    except Exception as e:
        return None, f'Error: {e}'

def get_ny_date():
    try:
        response = requests.get(TIME_API_URL_NY)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        data = response.json()
        iso_time = data.get('dateTime', 'Error: Time not available')

        # Extract date from ISO format string
        cleaned_date = iso_time.split('T')[0]

        try:
            parsed_date = datetime.datetime.strptime(cleaned_date, '%Y-%m-%d')
            return parsed_date.strftime('%b %d, %Y'), None  # Adjust the format for month abbreviation
        except ValueError:
            return None, f'Error: Invalid date format: {cleaned_date}'
    except Exception as e:
        return None, f'Error: {e}'


def fetch_user_high_scores():
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch data from the 'Users' table
    cursor.execute('SELECT Name, HighScore FROM Users')
    rows = cursor.fetchall()

    # Close the database connection
    conn.close()

    return rows

@app.route('/')
def hello():
    israel_time = get_israel_time()
    israel_date = get_israel_date()
    ny_time = get_ny_time()
    ny_date = get_ny_date()
    return render_template('home.html', israel_time=israel_time, israel_date=israel_date, ny_time=ny_time, ny_date=ny_date)

    
@app.route('/play')
def play_game():
    # You can render a template for the play page or redirect to another page
    return render_template('play.html') 


# Route for displaying high scores and creating the table
@app.route('/display_high_scores')
def display_high_scores():
    # Fetch user high scores from the database
    rows = fetch_user_high_scores()
    # Sort the rows by the second element (the high score) in descending order
    rows.sort(key=lambda x: x[1], reverse=True)
    # Render the template with the sorted data
    return render_template('high_scores.html', rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
