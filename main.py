from flask import Flask, request, render_template, send_file, session, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from dotenv import load_dotenv
import pymysql.cursors
from trucking_database import insert_new_tractor_info, insert_repair_info, get_repair_info, get_tractor_info
import pandas as pd
import io
import os
app = Flask(__name__, template_folder='public', static_folder='public/static')
DB_PASSWORD = password = os.environ.get('MYSQL_PASSWORD')

app.secret_key = 'love'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user


# The @login_manager.unauthorized_handler decorator indicates that the 
# following function should be called when a user tries to access a 
# protected endpoint but isn't authorized (i.e., not logged in).
@login_manager.unauthorized_handler
def unauthorized():
    '''
    Handle unauthorized access attempts.

    If the access attempt is made via an AJAX request, it returns a JSON error.
    Otherwise, it redirects the user to the login page.
    '''

    # Check if the request is an AJAX request (usually made via JavaScript on the front-end)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # If it's an AJAX request, return a JSON error response with a 401 Unauthorized status code
        return jsonify(error="auth required"), 401
    else:
        # If it's not an AJAX request, redirect the user to the login page
        return redirect(url_for('login'))

    
@app.route('/')
def index():
    return render_template("index.html")

# Establish database connection
def connect_to_database():
    connection = pymysql.connect(
        host='truckingdatabase.mysql.database.azure.com',
        user='thriftyuser',
        password=DB_PASSWORD,
        database='truck_database',
        ssl={"ca": "DigiCertGlobalRootCA.crt.pem"},
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


@app.route('/insert_tractor', methods=['POST'])
@login_required  # Ensure the user is logged in before accessing this route
def insert_tractor():
    '''
    Endpoint to handle the insertion of new tractor information into the database.
    Retrieves tractor details from a POST request, calls an external function
    to insert these details into the database, and then returns a response based on 
    the insertion result.
    '''

    # Retrieve tractor details from the form data
    asset_id = request.form.get('assetID')
    vin = request.form.get('vin')
    inspection_date = request.form.get('inspectionDate')
    licence_plate = request.form.get('licence')
    cvip = request.form.get('cvipDate')
    make = request.form.get('make')
    model = request.form.get('model')
    axle = request.form.get('axle')
    last_tire_replace_date = request.form.get('lastTireReplaceDate')
    year = request.form.get('year')

    # Debugging: Print the license plate value to the server console
    print((licence_plate))

    # Verify the provided axle type. If it's not "Single" or "Tandem", return an error
    if axle not in ['Single', 'Tandem']:
        return jsonify(status="Error", message="Invalid axle type provided. It should be either 'Single' or 'Tandem'.")

    # Call the function to insert new tractor info into the database.
    # This function should handle the actual database operations and
    # return a status (True/False) and a corresponding message.
    status, msg = insert_new_tractor_info(asset_id, vin, inspection_date, licence_plate, make, model, axle, last_tire_replace_date, cvip, year)

    # If the insertion was successful (status is True)
    if status:
        # Return a success message in JSON format with a 200 HTTP status code
        return jsonify({"message": msg}), 200
    else:
        # If there was an error (status is False)
        # Return an error message in JSON format with a 400 HTTP status code
        return jsonify


@app.route('/insert_repair', methods=['POST'])
@login_required  # Ensure the user is logged in before accessing this route
def insert_repair():
    '''
    Endpoint to handle the insertion of repair information into the database.
    This function retrieves repair details from a POST request, calls an 
    external function to insert the details into the database, and then returns
    a response based on the insertion result.
    '''

    # Debugging: Print "hi" to the server console
    print("hi")

    # Retrieve repair details from the form data
    repair_id = request.form.get('repairId')
    repair_asset_id = request.form.get('repairAssetID')
    repair_date = request.form.get('repairDate')
    cost = request.form.get('cost')
    repair_type = request.form.get('repairType')

    # Call the function to insert repair info into the database.
    # This function should handle the actual database operations and
    # return a status (True/False) and a corresponding message.
    status, msg = insert_repair_info(repair_id, repair_asset_id, repair_date, cost, repair_type)

    # If the insertion was successful (status is True)
    if status:
        # Return a success message in JSON format with a 200 HTTP status code
        return jsonify({"message": msg}), 200
    else:
        # If there was an error (status is False)
        # Return an error message in JSON format with a 400 HTTP status code
        return jsonify({"error": msg}), 400


@app.route('/get_repair', methods=['POST'])
@login_required  # Ensure the user is logged in before accessing this route
def get_repair():
    """
    Endpoint to fetch repair information for a given asset ID and year from the database 
    and return it as an Excel file.
    """

    # Retrieve the asset ID and year from the form data
    repair_info_asset_id = request.form.get('repairInfoAssetId')
    repair_year = request.form.get('repairYear')



    # Connect to the database and get the repair information based on provided criteria
    df = get_repair_info(repair_info_asset_id, repair_year)

    # Create an in-memory binary stream to hold the Excel file data
    output = io.BytesIO()

    # Print the dataframe to the server console (useful for debugging purposes)
    print(df)

    # Create an Excel writer object and write the dataframe to it
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)

    # Save the Excel file data to the in-memory binary stream
    writer.save()

    # Reset the stream's position to the start
    output.seek(0)

    # Send the in-memory binary stream as a downloadable Excel file to the client
    return send_file(output, download_name='repair_info.xlsx', as_attachment=True)


@app.route('/get_tractor_info', methods=['POST'])
@login_required  # Ensure the user is logged in before accessing this route
def get_tractor():
    """
    Endpoint to fetch tractor information from the database and return it as an Excel file.
    """
    # Retrieve the asset ID
    tractor_info_asset_id = request.form.get('tractorInfoAssetId')
    # Connect to the database and retrieve the tractor information
    df = get_tractor_info(tractor_info_asset_id)

    # Create an in-memory binary stream to hold the Excel file data
    output = io.BytesIO()

    # Create an Excel writer object and write the dataframe to it
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    
    # Save the Excel file data to the in-memory binary stream
    writer.save()
    
    # Reset the stream's position to the start
    output.seek(0)

    # Send the in-memory binary stream as a downloadable Excel file to the client
    return send_file(output, download_name='tractor_info.xlsx', as_attachment=True)



@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    GET
        First returns a login page for user
        User inserts login info
    POST
        Backend recieves users info
        Validates user info
        If success
            Returns back to home page
        Else
            Returns login page again

    '''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Establish database connection
        connection = connect_to_database()

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE username = %s AND password = %s"
                cursor.execute(sql, (username, password))
                user = cursor.fetchone()

                if user:
                    user = User()
                    user.id = username
                    login_user(user)
                    session['logged_in'] = True
                    return render_template("index.html")

                else:
                    return render_template('login.html', error='Invalid credentials')
        finally:
            connection.close()

    # GET request, render the login form
    return render_template('login.html')



@app.route('/logout')
@login_required  # Ensures only logged-in users can access this route
def logout():
    '''
    Log out the current user and redirect them to the login page.
    '''
    
    # This function logs out the user, effectively removing their session
    logout_user()
    
    # Redirects the user to the login page after successful logout
    return render_template('login.html')


