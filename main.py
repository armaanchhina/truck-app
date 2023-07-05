from flask import Flask, request, render_template, send_file
import pymysql.cursors
from trucking_database import insert_new_tractor_info, insert_repair_info, get_repair_info
import pandas as pd
import io
app = Flask(__name__, template_folder='public', static_folder='public/static')
# app = Flask(__name__, template_folder='public')



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/insert_tractor', methods=['POST'])
def insert_tractor():
    asset_id = request.form.get('assetID')
    vin = request.form.get('vin')
    inspection_date = request.form.get('inspectionDate')
    licence_plate = request.form.get('licencePlate')
    make = request.form.get('make')
    model = request.form.get('model')
    axle = request.form.get('axle')
    last_tire_replace_date = request.form.get('lastTireReplaceDate')
    print(type(last_tire_replace_date))

    # Connect to the database and insert the new tractor information
    insert_new_tractor_info(asset_id, vin, inspection_date, licence_plate, make, model, axle, last_tire_replace_date)

    return "Tractor information inserted successfully!", 200

@app.route('/insert_repair', methods=['POST'])
def insert_repair():
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

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    connection = pymysql.connect(host='localhost',
                                 user=username,
                                 password=password,
                                 database='tractor_database',
                                 cursorclass=pymysql.cursors.DictCursor)
    # Here you could run queries against the database
    # And return a response
    # For simplicity, let's just return a success message
    return "Successfully connected to the database!", 200

if __name__ == "__main__":
    app.run(debug=True)
