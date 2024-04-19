from flask import Flask
import requests
from babel.dates import format_datetime
from flask import Flask, render_template
import datetime
import pytz
import random
import dateutil.parser
from setLogic1 import logic 
#from db import create_table

app = Flask(__name__)

print("Static URL Path:", app.static_url_path)
print("Static Folder:", app.static_folder)



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

# data for card properties
colors = ['red', 'green', 'blue']
shapes = ['diamond', 'squiggle', 'oval']
shadings = ['solid', 'striped', 'outlined']
numbers = [1, 2, 3]

@app.route('/')
def hello():
    israel_time = get_israel_time()
    israel_date = get_israel_date()
    ny_time = get_ny_time()
    ny_date = get_ny_date()
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Set Game</title>
        <!-- CSS link -->
        <link rel="stylesheet" href="{{ url_for('static', filename='cards.css') }}">
    </head>
    <body>
        <h1>Set Game</h1>
        <p>Current time in Israel: {israel_time[0] if not israel_time[1] else israel_time[1]}</p>
        <p>Current date in Israel: {israel_date[0] if not israel_date[1] else israel_date[1]}</p>
        <p>Current time in NY: {ny_time[0] if not ny_time[1] else ny_time[1]}</p>
        <p>Current date in NY: {ny_date[0] if not ny_date[1] else ny_date[1]}</p>
        
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

# Define route to render game page
@app.route('/play')
def my_logic():

   # You will populate image_urls here
    all_image_urls = [
        "BEC1.jpg",
        "BEC2.jpg",
        "BEC3.jpg",
        "BEP1.jpg",
        "BEP2.jpg",
        "BEP3.jpg",
        "BES1.jpg",
        "BES2.jpg",
        "BES3.jpg",
        "BFC1.jpg",
        "BFC2.jpg",
        "BFC3.jpg",
        "BFP1.jpg",
        "BFP2.jpg",
        "BFP3.jpg",
        "BFS1.jpg",
        "BFS2.jpg",
        "BFS3.jpg",
        "BSC1.jpg",
        "BSC2.jpg",
        "BSC3.jpg",
        "BSP1.jpg",
        "BSP2.jpg",
        "BSP3.jpg",
        "BSS1.jpg",
        "BSS2.jpg",
        "BSS3.jpg", 
        "REC1.jpg",
        "REC2.jpg",
        "REC3.jpg",
        "REP1.jpg",
        "REP2.jpg",
        "REP3.jpg",
        "RES1.jpg",
        "RES2.jpg",
        "RES3.jpg",
        "RFC1.jpg",
        "RFC2.jpg",
        "RFC3.jpg",
        "RFP1.jpg",
        "RFP2.jpg",
        "RFP3.jpg",
        "RFS1.jpg",
        "RFS2.jpg",
        "RFS3.jpg",
        "RSC1.jpg",
        "RSC2.jpg",
        "RSC3.jpg",
        "RSP1.jpg",
        "RSP2.jpg",
        "RSP3.jpg",
        "RSS1.jpg",
        "RSS2.jpg",
        "RSS3.jpg",  
        "YEC1.jpg",
        "YEC2.jpg",
        "YEC3.jpg",
        "YEP1.jpg",
        "YEP2.jpg",
        "YEP3.jpg",
        "YES1.jpg",
        "YES2.jpg",
        "YES3.jpg",
        "YFC1.jpg",
        "YFC2.jpg",
        "YFC3.jpg",
        "YFP1.jpg",
        "YFP2.jpg",
        "YFP3.jpg",
        "YFS1.jpg",
        "YFS2.jpg",
        "YFS3.jpg",
        "YSC1.jpg",
        "YSC2.jpg",
        "YSC3.jpg",
        "YSP1.jpg",
        "YSP2.jpg",
        "YSP3.jpg",
        "YSS1.jpg",
        "YSS2.jpg",
        "YSS3.jpg"         
    ]
    image_urls = ['images/' + name for name in all_image_urls]
    # Select a random sample of 12 images
    random_image_urls = random.sample(image_urls, 12)
    return render_template('play.html', image_urls=random_image_urls)
