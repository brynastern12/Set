from flask import Flask
from flask import Flask, request, jsonify
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
    # Define attributes for each image
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
        'YSS3.jpg': {'number': 1, 'color': 'yellow', 'shape': 'square', 'shading': 'shaded'},
    }

    image_urls = [name for name in all_image_urls]
    image_urls = list(image_attributes.keys())

    # Select a random sample of image URLs and their attributes
    random_images = random.sample(list(image_attributes.items()), 12)
    print(random_images)

    # Now you have a list of random image URLs, and you can access their attributes from the image_attributes dictionary
#    for url in random_image_urls:
 #       attributes = image_attributes[url]
        
    # Pass image urls and attributes to the HTML template
    return render_template('play.html', random_images=random_images)
    
def is_set(card1, card2, card3):
        
        
    def is_property_set(prop1, prop2, prop3):
        return (prop1 == prop2 == prop3) or (prop1 != prop2 != prop3 != prop1)


    is_number_set = is_property_set(card1['number'], card2['number'], card3['number'])
    is_color_set = is_property_set(card1['color'], card2['color'], card3['color'])
    is_shape_set = is_property_set(card1['shape'], card2['shape'], card3['shape'])
    is_shading_set = is_property_set(card1['shading'], card2['shading'], card3['shading'])
        
    # Check if all properties form a Set
    return is_number_set and is_color_set and is_shape_set and is_shading_set
    
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


if __name__ == '__main__':
    app.run(debug=True)
