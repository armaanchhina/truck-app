from flask import Flask, request, render_template, send_file, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required

import pymysql.cursors
from trucking_database import insert_new_tractor_info, insert_repair_info, get_repair_info, get_tractor_info
import pandas as pd
import io
app = Flask(__name__, template_folder='public', static_folder='public/static')
# app = Flask(__name__, template_folder='public')

# connection = pymysql.connect(host='localhost',
#                              user='root',
#                              database='tractor_database',
#                              cursorclass=pymysql.cursors.DictCursor)

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

@app.route('/')
def index():
    return render_template("index.html")
# Establish database connection
def connect_to_database():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        database='tractor_database',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


@app.route('/insert_tractor', methods=['POST'])
@login_required
def insert_tractor():
    check_login()
    asset_id = request.form.get('assetID')
    vin = request.form.get('vin')
    inspection_date = request.form.get('inspectionDate')
    licence_plate = request.form.get('licence')
    cvip = request.form.get('cvipDate')
    make = request.form.get('make')
    model = request.form.get('model')
    axle = request.form.get('axle')
    last_tire_replace_date = request.form.get('lastTireReplaceDate')
    print((licence_plate))

    # Connect to the database and insert the new tractor information
    insert_new_tractor_info(asset_id, vin, inspection_date, licence_plate, make, model, axle, last_tire_replace_date, cvip)

    return "Tractor information inserted successfully!", 200

@app.route('/insert_repair', methods=['POST'])
@login_required
def insert_repair():
    check_login()
    repair_id = request.form.get('repairId')
    repair_asset_id = request.form.get('repairAssetID')
    repair_date = request.form.get('repairDate')
    cost = request.form.get('cost')
    repair_type = request.form.get('repairType')
    insert_repair_info(repair_id, repair_asset_id, repair_date, cost, repair_type)
    # Connect to the database and insert the new repair information
    # Be sure to handle errors and edge cases

    return "Repair information inserted successfully!", 200

@app.route('/get_repair', methods=['POST'])
@login_required
def get_repair():
    repair_info_asset_id = request.form.get('repairInfoAssetId')
    repair_year = request.form.get('repairYear')

    # Connect to the database and get the repair information
    # Be sure to handle errors and edge cases
    print(repair_info_asset_id)
    df = get_repair_info(repair_info_asset_id)
    output = io.BytesIO()
    print(df)

    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    output.seek(0)
    return send_file(output, attachment_filename='repair_info.xlsx', as_attachment=True)

    return "Repair information retrieved successfully!", 200

@app.route('/get_tractor_info', methods=['POST'])
@login_required
def get_tractor():

    # Connect to the database and get the repair information
    # Be sure to handle errors and edge cases
    df = get_tractor_info()
    output = io.BytesIO()
    print(df)

    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    output.seek(0)
    return send_file(output, attachment_filename='tractor_info.xlsx', as_attachment=True)

    return "Tractor information retrieved successfully!", 200

@app.route('/login', methods=['GET', 'POST'])
def login():
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

def check_login():
    if 'logged_in' not in session:
        return False
    return True

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)