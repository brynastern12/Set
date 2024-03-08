from flask import Flask
from setLogic1 import logic 
from db import create_table

app = Flask(__name__)

@app.route('/')
def hello():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Set Game</title>
        <style>
            body {
                font-family: Arial, sans-serif;
            }

            ul {
                list-style-type: none;
                padding: 0;
            }

            li {
                margin-bottom: 10px;
                border: 1px solid #ddd;
                padding: 5px;
            }

            form {
                margin-top: 20px;
            }

            label {
                display: block;
                margin-bottom: 5px;
            }

            input {
                width: 100%;
                padding: 5px;
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <h1>Set Game</h1>
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
