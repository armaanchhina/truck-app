import pymysql.cursors
import pandas as pd
import io
from dotenv import load_dotenv
import os

# load_dotenv()
# DB_PASSWORD = os.getenv('db_pass')
DB_PASSWORD = password = os.environ.get('MYSQL_PASSWORD')


def get_db_connection():
    connection = pymysql.connect(
        host='truckingdatabase.mysql.database.azure.com',
        user='thriftyuser',
        password=DB_PASSWORD,
        database='truck_database',
        ssl={"ca": "DigiCertGlobalRootCA.crt.pem"},
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

def insert_new_tractor_info(assetId: int, vin: str, inspection_date: str, licence_plate: str, make: str, model: str, axle: str, last_tire_replace_date: str, cvip: str,  year:str):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Check if the assetId already exists
            sql = "SELECT * FROM tractor_info WHERE assetId = %s"
            cursor.execute(sql, (assetId,))
            result = cursor.fetchone()
            print(licence_plate)
            if result:
                # If the assetId exists, perform an UPDATE
                sql = """
                UPDATE tractor_info 
                SET vin = %s, inspection_date = %s, licence_plate = %s, make = %s, model = %s, axle = %s, last_tire_replace_date = %s, cvip_date = %s, year = %s
                WHERE assetId = %s
                """
                cursor.execute(sql, (vin, inspection_date, licence_plate, make, model, axle, last_tire_replace_date,cvip,year,assetId))
                msg = f"Tractor information updated successfully for {assetId}!"
            else:
                # If the assetId does not exist, perform an INSERT
                sql = "INSERT INTO tractor_info (assetId, vin, inspection_date, licence_plate, make, model, axle, last_tire_replace_date, cvip_date, year) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (assetId, vin, inspection_date, licence_plate, make, model, axle, last_tire_replace_date, cvip, year))
                msg = f"Tractor information inserted successfully for {assetId}!"
            
            connection.commit()
            return True, msg
    except pymysql.MySQLError as e:
        print(f"Database error occurred: {e}")
        return False, str(e)
    except Exception as e:
        print(f"An error occurred: {e}")
        return False, str(e)
    finally:
        connection.close()


def delete_tractor_info(assetId: int):
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM tractor_info WHERE assetId = %s"
            cursor.execute(sql, (assetId,))
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Database error occurred: {e}")
        return False, str(e)
    except Exception as e:
        print(f"An error occurred: {e}")
        return False, str(e)
    finally:
        connection.close()

def insert_repair_info(repair_id: int, assetId: int, repair_date: str, cost: float, repair_type: str):
    # Connect to the database
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            # First, check if the assetId exists in the tractor_info table
            sql = "SELECT * FROM tractor_info WHERE assetId = %s"
            cursor.execute(sql, (assetId,))
            result = cursor.fetchone()

            # If the assetId does not exist in the tractor_info table, insert it
            if result is None:
                print("does not exist")
                sql = "INSERT INTO tractor_info (assetId) VALUES (%s)"
                cursor.execute(sql, (assetId,))
                connection.commit()

            # Now you can insert into the Repairs table
            sql = "INSERT INTO Repairs (repairId, assetId, Repair_Date, Cost, Repair_Type) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (repair_id, assetId, repair_date, cost, repair_type))
            msg = f"Repair information inserted successfully for {assetId}!"
            
            connection.commit()
            return True, msg
    except pymysql.MySQLError as e:
        print(f"Database error occurred: {e}")
        return False, str(e)
    except Exception as e:
        print(f"An error occurred: {e}")
        return False, str(e) 
    finally:
        connection.close()


def get_repair_info(assetId: str, repair_year: str):
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            if(assetId!=''):
                # sql = """SELECT r.*, t.* FROM Repairs r 
                #          JOIN tractor_info t ON r.assetID = t.assetId 
                #          WHERE r.assetID  = %s"""
                sql = """SELECT r.repairId, r.assetId, r.Repair_Date, r.Cost, r.Repair_Type, 
                t.vin, t.inspection_date, t.licence_plate, t.make, t.model, t.axle, t.last_tire_replace_date
                FROM Repairs r 
                JOIN tractor_info t ON r.assetID = t.assetId 
                WHERE r.assetID  = %s"""

                cursor.execute(sql, (assetId,))
            else:
                sql = """SELECT r.*, t.* FROM Repairs r 
                         JOIN tractor_info t ON r.assetID = t.assetId"""
                cursor.execute(sql)
            result = cursor.fetchall()
            df = pd.DataFrame(result)
    except pymysql.MySQLError as e:
        print(f"Database error occurred: {e}")
        return False, str(e)
    except Exception as e:
        print(f"An error occurred: {e}")
        return False, str(e)
    finally:
        connection.close()
        return df
    

def get_tractor_info():
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            sql = """SELECT t.*, SUM(r.Cost) as total_repair_costs
            FROM tractor_info t 
            LEFT JOIN Repairs r ON t.assetId = r.assetId 
            GROUP BY t.assetId"""

            cursor.execute(sql)

            result = cursor.fetchall()
            df = pd.DataFrame(result)
    except pymysql.MySQLError as e:
        print(f"Database error occurred: {e}")
        return False, str(e)
    except Exception as e:
        print(f"An error occurred: {e}")
        return False, str(e)
    finally:
        connection.close()
        return df
    





