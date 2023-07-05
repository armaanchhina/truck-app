import pymysql.cursors
import pandas as pd
import io

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             database='tractor_database',
                             cursorclass=pymysql.cursors.DictCursor)


def get_db_connection(username, password):
    connection = pymysql.connect(host='localhost',
                                 user=username,
                                 password=password,
                                 database='tractor_database',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def insert_new_tractor_info(assetId: int, vin: int, inspection_date: str, licence_plate: str, make: str, model: str, axle: str, last_tire_replace_date: str):
    try:
        with connection.cursor() as cursor:
            # Check if the assetId already exists
            sql = "SELECT * FROM tractor_info WHERE assetId = %s"
            cursor.execute(sql, (assetId,))
            result = cursor.fetchone()

            if result:
                # If the assetId exists, perform an UPDATE
                sql = """
                UPDATE tractor_info 
                SET vin = %s, inspection_date = %s, licence_plate = %s, make = %s, model = %s, axle = %s, last_tire_replace_date = %s
                WHERE assetId = %s
                """
                cursor.execute(sql, (vin, inspection_date, licence_plate, make, model, axle, last_tire_replace_date, assetId))
            else:
                # If the assetId does not exist, perform an INSERT
                sql = "INSERT INTO tractor_info (assetId, vin, inspection_date, licence_plate, make, model, axle, last_tire_replace_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (assetId, vin, inspection_date, licence_plate, make, model, axle, last_tire_replace_date))
            
            connection.commit()
    except Exception as e:
        return(f"An error occurred: {e}")
    finally:
        connection.close()


def delete_tractor_info(assetId: int):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM tractor_info WHERE assetId = %s"
            cursor.execute(sql, (assetId,))
            connection.commit()
    except Exception as e:
        return(f"An error occurred: {e}")
    finally:
        connection.close()

def insert_repair_info(repair_id: int, assetId: int, repair_date: str, cost: float, repair_type: str):
    # Connect to the database
    try:
        with connection.cursor() as cursor:
            # First, check if the assetId exists in the tractor_info table
            sql = "SELECT * FROM tractor_info WHERE assetId = %s"
            cursor.execute(sql, (assetId,))
            result = cursor.fetchone()

            # If the assetId does not exist in the tractor_info table, insert it
            if result is None:
                sql = "INSERT INTO tractor_info (assetId) VALUES (%s)"
                cursor.execute(sql, (assetId,))
                connection.commit()

            # Now you can insert into the Repairs table
            sql = "INSERT INTO Repairs (repairId, assetId, Repair_Date, Cost, Repair_Type) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (repair_id, assetId, repair_date, cost, repair_type))
            connection.commit()
    except Exception as e:
        return(f"An error occurred: {e}")
    finally:
        connection.close()


def get_repair_info(assetId: int):
    try:
        with connection.cursor() as cursor:
            if(assetId):
                sql = """SELECT r.*, t.* FROM Repairs r 
                         JOIN tractor_info t ON r.assetID = t.assetId 
                         WHERE r.assetID  = %s"""
                cursor.execute(sql, (assetId,))
            else:
                sql = """SELECT r.*, t.* FROM Repairs r 
                         JOIN tractor_info t ON r.assetID = t.assetId"""
                cursor.execute(sql)
            result = cursor.fetchall()
            df = pd.DataFrame(result)
    finally:
        connection.close()
        return df



# insert_new_tractor_info(3)
# delete_tractor_info(3)
# delete_tractor_info(1)
