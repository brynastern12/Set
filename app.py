from flask import Flask, request, jsonify, render_template
from datetime import datetime as dt
import random
import datetime
import requests
import pymysql
import pytz
import dateutil.parser

app = Flask(__name__)

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'mazaliLAZAR8'
DB_NAME = 'SET_DATABASE_REAL' 
# Define your card deck
card_deck = [
    {'image_url': 'BEC1.jpg', 'attributes': {'number': 1, 'color': 'blue', 'shape': 'circle', 'shading': 'empty'}},
    {'image_url': 'BEC2.jpg', 'attributes': {'number': 2, 'color': 'blue', 'shape': 'circle', 'shading': 'empty'}},    {'image_url': 'BEC3.jpg', 'attributes': {'number': 3, 'color': 'blue', 'shape': 'circle', 'shading': 'empty'}},
    {'image_url': 'BEP1.jpg', 'attributes': {'number': 1, 'color': 'blue', 'shape': 'pentagon', 'shading': 'empty'}},
    {'image_url': 'BEP2.jpg', 'attributes': {'number': 2, 'color': 'blue', 'shape': 'pentagon', 'shading': 'empty'}},
    {'image_url': 'BEP3.jpg', 'attributes': {'number': 3, 'color': 'blue', 'shape': 'pentagon', 'shading': 'empty'}},
    {'image_url': 'BES1.jpg', 'attributes': {'number': 1, 'color': 'blue', 'shape': 'square', 'shading': 'empty'}},        {'image_url': 'BES2.jpg', 'attributes': {'number': 2, 'color': 'blue', 'shape': 'square', 'shading': 'empty'}},
    {'image_url': 'BES3.jpg', 'attributes': {'number': 3, 'color': 'blue', 'shape': 'square', 'shading': 'empty'}},
    {'image_url': 'BFC1.jpg', 'attributes': {'number': 1, 'color': 'blue', 'shape': 'circle', 'shading': 'solid'}},
    {'image_url': 'BFC2.jpg', 'attributes': {'number': 2, 'color': 'blue', 'shape': 'circle', 'shading': 'solid'}},
    {'image_url': 'BFC3.jpg', 'attributes': {'number': 3, 'color': 'blue', 'shape': 'circle', 'shading': 'solid'}},
    {'image_url': 'BFP1.jpg', 'attributes': {'number': 1, 'color': 'blue', 'shape': 'pentagon', 'shading': 'solid'}},
    {'image_url': 'BFP2.jpg', 'attributes': {'number': 2, 'color': 'blue', 'shape': 'pentagon', 'shading': 'solid'}},
    {'image_url': 'BFP3.jpg', 'attributes': {'number': 3, 'color': 'blue', 'shape': 'pentagon', 'shading': 'solid'}},
    {'image_url': 'BFS1.jpg', 'attributes': {'number': 1, 'color': 'blue', 'shape': 'square', 'shading': 'solid'}},
    {'image_url': 'BFS2.jpg', 'attributes': {'number': 2, 'color': 'blue', 'shape': 'square', 'shading': 'solid'}},
    {'image_url': 'BFS3.jpg', 'attributes': {'number': 3, 'color': 'blue', 'shape': 'square', 'shading': 'solid'}},
    {'image_url': 'BSC1.jpg', 'attributes': {'number': 1, 'color': 'blue', 'shape': 'circle', 'shading': 'shaded'}},
    {'image_url': 'BSC2.jpg', 'attributes': {'number': 2, 'color': 'blue', 'shape': 'circle', 'shading': 'shaded'}},
    {'image_url': 'BSC3.jpg', 'attributes': {'number': 3, 'color': 'blue', 'shape': 'circle', 'shading': 'shaded'}},
    {'image_url': 'BSP1.jpg', 'attributes': {'number': 1, 'color': 'blue', 'shape': 'pentagon', 'shading': 'shaded'}},
    {'image_url': 'BSP2.jpg', 'attributes': {'number': 2, 'color': 'blue', 'shape': 'pentagon', 'shading': 'shaded'}},
    {'image_url': 'BSP3.jpg', 'attributes': {'number': 3, 'color': 'blue', 'shape': 'pentagon', 'shading': 'shaded'}},
    {'image_url': 'BSS1.jpg', 'attributes': {'number': 1, 'color': 'blue', 'shape': 'square', 'shading': 'shaded'}},
    {'image_url': 'BSS2.jpg', 'attributes': {'number': 2, 'color': 'blue', 'shape': 'square', 'shading': 'shaded'}},
    {'image_url': 'BSS3.jpg', 'attributes': {'number': 3, 'color': 'blue', 'shape': 'square', 'shading': 'shaded'}}, 
    {'image_url': 'REC1.jpg', 'attributes': {'number': 1, 'color': 'red', 'shape': 'circle', 'shading': 'empty'}},
    {'image_url': 'REC2.jpg', 'attributes': {'number': 2, 'color': 'red', 'shape': 'circle', 'shading': 'empty'}},
    {'image_url': 'REC3.jpg', 'attributes': {'number': 3, 'color': 'red', 'shape': 'circle', 'shading': 'empty'}},
    {'image_url': 'REP1.jpg', 'attributes': {'number': 1, 'color': 'red', 'shape': 'pentagon', 'shading': 'empty'}},
    {'image_url': 'REP2.jpg', 'attributes': {'number': 2, 'color': 'red', 'shape': 'pentagon', 'shading': 'empty'}},
    {'image_url': 'REP3.jpg', 'attributes': {'number': 3, 'color': 'red', 'shape': 'pentagon', 'shading': 'empty'}},
    {'image_url': 'RES1.jpg', 'attributes': {'number': 1, 'color': 'red', 'shape': 'square', 'shading': 'empty'}},
    {'image_url': 'RES2.jpg', 'attributes': {'number': 2, 'color': 'red', 'shape': 'square', 'shading': 'empty'}},
    {'image_url': 'RES3.jpg', 'attributes': {'number': 3, 'color': 'red', 'shape': 'square', 'shading': 'empty'}},
    {'image_url': 'RFC1.jpg', 'attributes': {'number': 1, 'color': 'red', 'shape': 'circle', 'shading': 'solid'}},
    {'image_url': 'RFC2.jpg', 'attributes': {'number': 2, 'color': 'red', 'shape': 'circle', 'shading': 'solid'}},
    {'image_url': 'RFC3.jpg', 'attributes': {'number': 3, 'color': 'red', 'shape': 'circle', 'shading': 'solid'}},
    {'image_url': 'RFP1.jpg', 'attributes': {'number': 1, 'color': 'red', 'shape': 'pentagon', 'shading': 'solid'}},
    {'image_url': 'RFP2.jpg', 'attributes': {'number': 2, 'color': 'red', 'shape': 'pentagon', 'shading': 'solid'}},
    {'image_url': 'RFP3.jpg', 'attributes': {'number': 3, 'color': 'red', 'shape': 'pentagon', 'shading': 'solid'}},
    {'image_url': 'RFS1.jpg', 'attributes': {'number': 1, 'color': 'red', 'shape': 'square', 'shading': 'solid'}},
    {'image_url': 'RFS2.jpg', 'attributes': {'number': 2, 'color': 'red', 'shape': 'square', 'shading': 'solid'}},
    {'image_url': 'RFS3.jpg', 'attributes': {'number': 3, 'color': 'red', 'shape': 'square', 'shading': 'solid'}},
    {'image_url': 'RSC1.jpg', 'attributes': {'number': 1, 'color': 'red', 'shape': 'circle', 'shading': 'shaded'}},
    {'image_url': 'RSC2.jpg', 'attributes': {'number': 2, 'color': 'red', 'shape': 'circle', 'shading': 'shaded'}},
    {'image_url': 'RSC3.jpg', 'attributes': {'number': 3, 'color': 'red', 'shape': 'circle', 'shading': 'shaded'}},
    {'image_url': 'RSP1.jpg', 'attributes': {'number': 1, 'color': 'red', 'shape': 'pentagon', 'shading': 'shaded'}},
    {'image_url': 'RSP2.jpg', 'attributes': {'number': 2, 'color': 'red', 'shape': 'pentagon', 'shading': 'shaded'}},
    {'image_url': 'RSP3.jpg', 'attributes': {'number': 3, 'color': 'red', 'shape': 'pentagon', 'shading': 'shaded'}},
    {'image_url': 'RSS1.jpg', 'attributes': {'number': 1, 'color': 'red', 'shape': 'square', 'shading': 'shaded'}},
    {'image_url': 'RSS2.jpg', 'attributes': {'number': 2, 'color': 'red', 'shape': 'square', 'shading': 'shaded'}},
    {'image_url': 'RSS3.jpg', 'attributes': {'number': 3, 'color': 'red', 'shape': 'square', 'shading': 'shaded'}},  
    {'image_url': 'YEC1.jpg', 'attributes': {'number': 1, 'color': 'yellow', 'shape': 'circle', 'shading': 'empty'}},
    {'image_url': 'YEC2.jpg', 'attributes': {'number': 2, 'color': 'yellow', 'shape': 'circle', 'shading': 'empty'}},
    {'image_url': 'YEC3.jpg', 'attributes': {'number': 3, 'color': 'yellow', 'shape': 'circle', 'shading': 'empty'}},
    {'image_url': 'YEP1.jpg', 'attributes': {'number': 1, 'color': 'yellow', 'shape': 'pentagon', 'shading': 'empty'}},
    {'image_url': 'YEP2.jpg', 'attributes': {'number': 2, 'color': 'yellow', 'shape': 'pentagon', 'shading': 'empty'}},
    {'image_url': 'YEP3.jpg', 'attributes': {'number': 3, 'color': 'yellow', 'shape': 'pentagon', 'shading': 'empty'}},
    {'image_url': 'YES1.jpg', 'attributes': {'number': 1, 'color': 'yellow', 'shape': 'square', 'shading': 'empty'}},
    {'image_url': 'YES2.jpg', 'attributes': {'number': 2, 'color': 'yellow', 'shape': 'square', 'shading': 'empty'}},
    {'image_url': 'YES3.jpg', 'attributes': {'number': 3, 'color': 'yellow', 'shape': 'square', 'shading': 'empty'}},
    {'image_url': 'YFC1.jpg', 'attributes': {'number': 1, 'color': 'yellow', 'shape': 'circle', 'shading': 'solid'}},
    {'image_url': 'YFC2.jpg', 'attributes': {'number': 2, 'color': 'yellow', 'shape': 'circle', 'shading': 'solid'}},
    {'image_url': 'YFC3.jpg', 'attributes': {'number': 3, 'color': 'yellow', 'shape': 'circle', 'shading': 'solid'}},
    {'image_url': 'YFP1.jpg', 'attributes': {'number': 1, 'color': 'yellow', 'shape': 'pentagon', 'shading': 'solid'}},
    {'image_url': 'YFP2.jpg', 'attributes': {'number': 2, 'color': 'yellow', 'shape': 'pentagon', 'shading': 'solid'}},
    {'image_url': 'YFP3.jpg', 'attributes': {'number': 3, 'color': 'yellow', 'shape': 'pentagon', 'shading': 'solid'}},
    {'image_url': 'YFS1.jpg', 'attributes': {'number': 1, 'color': 'yellow', 'shape': 'square', 'shading': 'solid'}},
    {'image_url': 'YFS2.jpg', 'attributes': {'number': 2, 'color': 'yellow', 'shape': 'square', 'shading': 'solid'}},
    {'image_url': 'YFS3.jpg', 'attributes': {'number': 3, 'color': 'yellow', 'shape': 'square', 'shading': 'solid'}},
    {'image_url': 'YSC1.jpg', 'attributes': {'number': 1, 'color': 'yellow', 'shape': 'circle', 'shading': 'shaded'}},
    {'image_url': 'YSC2.jpg', 'attributes': {'number': 2, 'color': 'yellow', 'shape': 'circle', 'shading': 'shaded'}},
    {'image_url': 'YSC3.jpg', 'attributes': {'number': 3, 'color': 'yellow', 'shape': 'circle', 'shading': 'shaded'}},
    {'image_url': 'YSP1.jpg', 'attributes': {'number': 1, 'color': 'yellow', 'shape': 'pentagon', 'shading': 'shaded'}},
    {'image_url': 'YSP2.jpg', 'attributes': {'number': 2, 'color': 'yellow', 'shape': 'pentagon', 'shading': 'shaded'}},
    {'image_url': 'YSP3.jpg', 'attributes': {'number': 3, 'color': 'yellow', 'shape': 'pentagon', 'shading': 'shaded'}},
    {'image_url': 'YSS1.jpg', 'attributes': {'number': 1, 'color': 'yellow', 'shape': 'square', 'shading': 'shaded'}},
    {'image_url': 'YSS2.jpg', 'attributes': {'number': 1, 'color': 'yellow', 'shape': 'square', 'shading': 'shaded'}},
    {'image_url': 'YSS3.jpg', 'attributes': {'number': 1, 'color': 'yellow', 'shape': 'square', 'shading': 'shaded'}}
]



TIME_API_URL_Israel = 'https://timeapi.io/api/Time/current/zone?timeZone=Israel'
TIME_API_URL_NY = 'https://timeapi.io/api/Time/current/zone?timeZone=America/New_York'
# Function to get a database connection
def get_db_connection():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME, cursorclass=pymysql.cursors.DictCursor)

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


def format_time(time):
    try:
        # Split the time string into components
        components = time.split(':')
        # Extract minutes and seconds
        minutes = int(components[1])
        seconds = int(components[2].split('.')[0])  # Extract seconds and remove milliseconds
        # Return formatted time as 'MM:SS'
        return f"{minutes:02d}:{seconds:02d}"
    except (ValueError, IndexError):
        return '00:00'  # Return default value if time format is invalid or incomplete



@app.route('/')
def hello():
    create_table()
    israel_time = get_israel_time()
    israel_date = get_israel_date()
    ny_time = get_ny_time()
    ny_date = get_ny_date()
    return render_template('home.html', israel_time=israel_time, israel_date=israel_date, ny_time=ny_time, ny_date=ny_date)

# Define route to render game page
@app.route('/play')
def my_logic():
    global card_deck #declare card_deck as a global variable

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
    image_attributes = {
    'BEC1.jpg': {'number': 1, 'color': 'blue', 'shape': 'circle', 'shading': 'empty'},
    'BEC2.jpg': {'number': 2, 'color': 'blue', 'shape': 'circle', 'shading': 'empty'},
    'BEC3.jpg': {'number': 3, 'color': 'blue', 'shape': 'circle', 'shading': 'empty'},
    'BEP1.jpg': {'number': 1, 'color': 'blue', 'shape': 'pentagon', 'shading': 'empty'},
    'BEP2.jpg': {'number': 2, 'color': 'blue', 'shape': 'pentagon', 'shading': 'empty'},
    'BEP3.jpg': {'number': 3, 'color': 'blue', 'shape': 'pentagon', 'shading': 'empty'},
    'BES1.jpg': {'number': 1, 'color': 'blue', 'shape': 'square', 'shading': 'empty'},
    'BES2.jpg': {'number': 2, 'color': 'blue', 'shape': 'square', 'shading': 'empty'},
    'BES3.jpg': {'number': 3, 'color': 'blue', 'shape': 'square', 'shading': 'empty'},
    'BFC1.jpg': {'number': 1, 'color': 'blue', 'shape': 'circle', 'shading': 'solid'},
    'BFC2.jpg': {'number': 2, 'color': 'blue', 'shape': 'circle', 'shading': 'solid'},
    'BFC3.jpg': {'number': 3, 'color': 'blue', 'shape': 'circle', 'shading': 'solid'},
    'BFP1.jpg': {'number': 1, 'color': 'blue', 'shape': 'pentagon', 'shading': 'solid'},
    'BFP2.jpg': {'number': 2, 'color': 'blue', 'shape': 'pentagon', 'shading': 'solid'},
    'BFP3.jpg': {'number': 3, 'color': 'blue', 'shape': 'pentagon', 'shading': 'solid'},
    'BFS1.jpg': {'number': 1, 'color': 'blue', 'shape': 'square', 'shading': 'solid'},
    'BFS2.jpg': {'number': 2, 'color': 'blue', 'shape': 'square', 'shading': 'solid'},
    'BFS3.jpg': {'number': 3, 'color': 'blue', 'shape': 'square', 'shading': 'solid'},
    'BSC1.jpg': {'number': 1, 'color': 'blue', 'shape': 'circle', 'shading': 'shaded'},
    'BSC2.jpg': {'number': 2, 'color': 'blue', 'shape': 'circle', 'shading': 'shaded'},
    'BSC3.jpg': {'number': 3, 'color': 'blue', 'shape': 'circle', 'shading': 'shaded'},
    'BSP1.jpg': {'number': 1, 'color': 'blue', 'shape': 'pentagon', 'shading': 'shaded'},
    'BSP2.jpg': {'number': 2, 'color': 'blue', 'shape': 'pentagon', 'shading': 'shaded'},
    'BSP3.jpg': {'number': 3, 'color': 'blue', 'shape': 'pentagon', 'shading': 'shaded'},
    'BSS1.jpg': {'number': 1, 'color': 'blue', 'shape': 'square', 'shading': 'shaded'},
    'BSS2.jpg': {'number': 2, 'color': 'blue', 'shape': 'square', 'shading': 'shaded'},
    'BSS3.jpg': {'number': 3, 'color': 'blue', 'shape': 'square', 'shading': 'shaded'},
    'REC1.jpg': {'number': 1, 'color': 'red', 'shape': 'circle', 'shading': 'empty'},
    'REC2.jpg': {'number': 2, 'color': 'red', 'shape': 'circle', 'shading': 'empty'},
    'REC3.jpg': {'number': 3, 'color': 'red', 'shape': 'circle', 'shading': 'empty'},
    'REP1.jpg': {'number': 1, 'color': 'red', 'shape': 'pentagon', 'shading': 'empty'},
    'REP2.jpg': {'number': 2, 'color': 'red', 'shape': 'pentagon', 'shading': 'empty'},
    'REP3.jpg': {'number': 3, 'color': 'red', 'shape': 'pentagon', 'shading': 'empty'},
    'RES1.jpg': {'number': 1, 'color': 'red', 'shape': 'square', 'shading': 'empty'},
    'RES2.jpg': {'number': 2, 'color': 'red', 'shape': 'square', 'shading': 'empty'},
    'RES3.jpg': {'number': 3, 'color': 'red', 'shape': 'square', 'shading': 'empty'},
    'RFC1.jpg': {'number': 1, 'color': 'red', 'shape': 'circle', 'shading': 'solid'},
    'RFC2.jpg': {'number': 2, 'color': 'red', 'shape': 'circle', 'shading': 'solid'},
    'RFC3.jpg': {'number': 3, 'color': 'red', 'shape': 'circle', 'shading': 'solid'},
    'RFP1.jpg': {'number': 1, 'color': 'red', 'shape': 'pentagon', 'shading': 'solid'},
    'RFP2.jpg': {'number': 2, 'color': 'red', 'shape': 'pentagon', 'shading': 'solid'},
    'RFP3.jpg': {'number': 3, 'color': 'red', 'shape': 'pentagon', 'shading': 'solid'},
    'RFS1.jpg': {'number': 1, 'color': 'red', 'shape': 'square', 'shading': 'solid'},
    'RFS2.jpg': {'number': 2, 'color': 'red', 'shape': 'square', 'shading': 'solid'},
    'RFS3.jpg': {'number': 3, 'color': 'red', 'shape': 'square', 'shading': 'solid'},
    'RSC1.jpg': {'number': 1, 'color': 'red', 'shape': 'circle', 'shading': 'shaded'},
    'RSC2.jpg': {'number': 2, 'color': 'red', 'shape': 'circle', 'shading': 'shaded'},
    'RSC3.jpg': {'number': 3, 'color': 'red', 'shape': 'circle', 'shading': 'shaded'},
    'RSP1.jpg': {'number': 1, 'color': 'red', 'shape': 'pentagon', 'shading': 'shaded'},
    'RSP2.jpg': {'number': 2, 'color': 'red', 'shape': 'pentagon', 'shading': 'shaded'},
    'RSP3.jpg': {'number': 3, 'color': 'red', 'shape': 'pentagon', 'shading': 'shaded'},
    'RSS1.jpg': {'number': 1, 'color': 'red', 'shape': 'square', 'shading': 'shaded'},
    'RSS2.jpg': {'number': 2, 'color': 'red', 'shape': 'square', 'shading': 'shaded'},
    'RSS3.jpg': {'number': 3, 'color': 'red', 'shape': 'square', 'shading': 'shaded'},  
    'YEC1.jpg': {'number': 1, 'color': 'yellow', 'shape': 'circle', 'shading': 'empty'},
    'YEC2.jpg': {'number': 2, 'color': 'yellow', 'shape': 'circle', 'shading': 'empty'},
    'YEC3.jpg': {'number': 3, 'color': 'yellow', 'shape': 'circle', 'shading': 'empty'},
    'YEP1.jpg': {'number': 1, 'color': 'yellow', 'shape': 'pentagon', 'shading': 'empty'},
    'YEP2.jpg': {'number': 2, 'color': 'yellow', 'shape': 'pentagon', 'shading': 'empty'},
    'YEP3.jpg': {'number': 3, 'color': 'yellow', 'shape': 'pentagon', 'shading': 'empty'},
    'YES1.jpg': {'number': 1, 'color': 'yellow', 'shape': 'square', 'shading': 'empty'},
    'YES2.jpg': {'number': 2, 'color': 'yellow', 'shape': 'square', 'shading': 'empty'},
    'YES3.jpg': {'number': 3, 'color': 'yellow', 'shape': 'square', 'shading': 'empty'},
    'YFC1.jpg': {'number': 1, 'color': 'yellow', 'shape': 'circle', 'shading': 'solid'},
    'YFC2.jpg': {'number': 2, 'color': 'yellow', 'shape': 'circle', 'shading': 'solid'},
    'YFC3.jpg': {'number': 3, 'color': 'yellow', 'shape': 'circle', 'shading': 'solid'},
    'YFP1.jpg': {'number': 1, 'color': 'yellow', 'shape': 'pentagon', 'shading': 'solid'},
    'YFP2.jpg': {'number': 2, 'color': 'yellow', 'shape': 'pentagon', 'shading': 'solid'},
    'YFP3.jpg': {'number': 3, 'color': 'yellow', 'shape': 'pentagon', 'shading': 'solid'},
    'YFS1.jpg': {'number': 1, 'color': 'yellow', 'shape': 'square', 'shading': 'solid'},
    'YFS2.jpg': {'number': 2, 'color': 'yellow', 'shape': 'square', 'shading': 'solid'},
    'YFS3.jpg': {'number': 3, 'color': 'yellow', 'shape': 'square', 'shading': 'solid'},
    'YSC1.jpg': {'number': 1, 'color': 'yellow', 'shape': 'circle', 'shading': 'shaded'},
    'YSC2.jpg': {'number': 2, 'color': 'yellow', 'shape': 'circle', 'shading': 'shaded'},
    'YSC3.jpg': {'number': 3, 'color': 'yellow', 'shape': 'circle', 'shading': 'shaded'},
    'YSP1.jpg': {'number': 1, 'color': 'yellow', 'shape': 'pentagon', 'shading': 'shaded'},
    'YSP2.jpg': {'number': 2, 'color': 'yellow', 'shape': 'pentagon', 'shading': 'shaded'},
    'YSP3.jpg': {'number': 3, 'color': 'yellow', 'shape': 'pentagon', 'shading': 'shaded'},
    'YSS1.jpg': {'number': 1, 'color': 'yellow', 'shape': 'square', 'shading': 'shaded'},
    'YSS2.jpg': {'number': 1, 'color': 'yellow', 'shape': 'square', 'shading': 'shaded'},
    'YSS3.jpg': {'number': 1, 'color': 'yellow', 'shape': 'square', 'shading': 'shaded'}
    }

    # Get all image URLs
    all_image_urls = list(image_attributes.keys())

    # Shuffle deck
    random.shuffle(all_image_urls)

    # Select the first twelve cards from the deck
    random_image_urls = all_image_urls[:12]

    # Structure random_images correctly
    random_images = [(filename, image_attributes[filename]) for filename in random_image_urls]

    # Pass random_images to the template
    return render_template('play.html', random_images=random_images)
        
def is_set(card1, card2, card3):
    def is_property_set(prop1, prop2, prop3):
        return (prop1 == prop2 == prop3) or (prop1 != prop2 != prop3 != prop1)

    # Check if all required attributes are present in the card dictionaries
    if all(attr in card1 and attr in card2 and attr in card3 for attr in ['number', 'color', 'shape', 'shading']):
        is_number_set = is_property_set(card1['number'], card2['number'], card3['number'])
        is_color_set = is_property_set(card1['color'], card2['color'], card3['color'])
        is_shape_set = is_property_set(card1['shape'], card2['shape'], card3['shape'])
        is_shading_set = is_property_set(card1['shading'], card2['shading'], card3['shading'])
        
        # Check if all properties form a Set
        return is_number_set and is_color_set and is_shape_set and is_shading_set
    else:
        # If any required attribute is missing, return False
        return False

@app.route('/check_set', methods=['POST'])
def check_set():
    # Receive the attributes of the three selected cards from the frontend
    data = request.get_json()
    if isinstance(data, list) and len(data) == 3:
        card1 = data[0]
        card2 = data[1]
        card3 = data[2]

        # Check if the selected cards form a set
        if is_set(card1, card2, card3):
            # If a set is found, return 'set' to the frontend
            return jsonify({'message': 'set'})
        else:
            # If no set is found, return 'not_set' to the frontend
            return jsonify({'message': 'not_set'})
    else:
        # If the data is not in the expected format, return an error message
        return jsonify({'message': 'invalid_data_format'})
@app.route('/get_random_cards', methods=['GET'])
def get_random_cards():
    global card_deck
    #Select the next three  cards from the deck
    random_cards = card_deck[:3]
    #remove selected cards from deck
    card_deck = card_deck[3:]
    # Return the random cards as JSON
    return jsonify(random_cards)
    
@app.route('/display_high_scores')
def display_high_scores():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Users ORDER BY Number_Of_Sets DESC")
    rows = cursor.fetchall()
    print("Fetched Rows:", rows)
    conn.close()
    
    # Render the template with the retrieved data
    return render_template('high_scores.html', rows=rows)

# Route to save game data
@app.route('/save_game_data', methods=['POST'])
def save_game_data():
    data = request.json  # Get the JSON data sent from the client
    # Extract data from the JSON request
    user_name = data['user_name']
    date = data['date']
    date_str = data['date']
    date_only_str = date_str.split('T')[0]
    time_elapsed = data['time_elapsed']
    sets_found = data['sets_found']

    conn = get_db_connection()  # Connect to the database
    cursor = conn.cursor()  # Create a cursor object

    # Insert the game data into the 'Users' table
    cursor.execute("INSERT INTO Users (Name, Date, Time, Number_Of_Sets) VALUES (%s, %s, %s, %s)", (user_name, date_only_str, time_elapsed, sets_found))

    conn.commit()  # Commit the transaction
    conn.close()  # Close the database connection

    return jsonify({'message': 'Game data saved successfully'})


def create_table():
    conn = get_db_connection()
    print("Database connection created successfully!")  # Debug statement
    cursor = conn.cursor()

    # Check if the 'Users' table already exists
    cursor.execute("SHOW TABLES LIKE 'Users'")
    table_exists = cursor.fetchone() is not None

    if not table_exists:
        # Create the 'Users' table if it doesn't exist
        cursor.execute('''
            CREATE TABLE Users (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(255),
                Date DATE,
                Time TIME,
                Number_Of_Sets INT
            )
        ''')
        print("Table 'Users' created successfully!")
    else:
        print("Table 'Users' already exists. No action taken.")

    conn.commit()
    conn.close()
    

if __name__ == '__main__':
    app.run(debug=True)

