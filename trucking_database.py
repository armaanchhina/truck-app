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

import pymysql
from typing import Tuple, Any

def insert_new_tractor_info(
    assetId: int, vin: str, inspection_date: str, licence_plate: str,
    make: str, model: str, axle: str, last_tire_replace_date: str,
    cvip: str,  year: str
) -> Tuple[bool, str]:
    """
    Inserts or updates tractor information based on the provided asset ID.

    If an asset ID is found in the database, the information is updated.
    Otherwise, a new record is inserted.

    Parameters:
        - assetId (int): Unique identifier for the tractor.
        - vin (str): Vehicle Identification Number.
        - inspection_date (str): Date of last inspection.
        - licence_plate (str): Licence plate number.
        - make (str): Make/Brand of the tractor.
        - model (str): Model of the tractor.
        - axle (str): Axle type, typically 'Single' or 'Tandem'.
        - last_tire_replace_date (str): Date when tires were last replaced.
        - cvip (str): Commercial Vehicle Inspection Program date.
        - year (str): Year of manufacture.

    Returns:
        Tuple[bool, str]: Operation success status and a corresponding message.
    """
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Check if assetId already exists in the database
            sql = "SELECT * FROM tractor_info WHERE assetId = %s"
            cursor.execute(sql, (assetId,))
            result = cursor.fetchone()
            
            if result:
                # If assetId exists, update the corresponding record
                sql = """
                UPDATE tractor_info 
                SET vin = %s, inspection_date = %s, licence_plate = %s, make = %s, 
                    model = %s, axle = %s, last_tire_replace_date = %s, 
                    cvip_date = %s, year = %s
                WHERE assetId = %s
                """
                cursor.execute(sql, (vin, inspection_date, licence_plate, make, model, axle, last_tire_replace_date, cvip, year, assetId))
                msg = f"Tractor information updated successfully for {assetId}!"
            else:
                # If assetId does not exist, insert a new record
                sql = "INSERT INTO tractor_info (assetId, vin, inspection_date, licence_plate, make, model, axle, last_tire_replace_date, cvip_date, year) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (assetId, vin, inspection_date, licence_plate, make, model, axle, last_tire_replace_date, cvip, year))
                msg = f"Tractor information inserted successfully for assetId: {assetId}!"
            
            connection.commit()
            return True, msg

    except pymysql.MySQLError as e:
        # Handle database-related errors
        print(f"Database error occurred: {e}")
        return False, str(e)

    except Exception as e:
        # Handle general errors
        print(f"An error occurred: {e}")
        return False, str(e)

    finally:
        # Close the database connection
        connection.close()





def delete_tractor_info(assetId: int) -> Tuple[bool, str]:
    """
    Deletes tractor information based on the provided asset ID.

    Parameters:
        - assetId (int): Unique identifier for the tractor.

    Returns:
        Tuple[bool, str]: Operation success status and a corresponding message.
    """
    
    connection = get_db_connection()
    
    try:
        with connection.cursor() as cursor:
            # Prepare SQL statement to delete a tractor record by assetId
            sql = "DELETE FROM tractor_info WHERE assetId = %s"
            cursor.execute(sql, (assetId,))
            # Check if any record was deleted
            if cursor.rowcount == 0:
                return True, f"No tractor information found for assetId: {assetId}"
            
            connection.commit()
            return True, f"Tractor information deleted successfully for assetId: {assetId}"

    except pymysql.MySQLError as e:
        # Handle database-related errors
        print(f"Database error occurred: {e}")
        return False, str(e)

    except Exception as e:
        # Handle general errors
        print(f"An error occurred: {e}")
        return False, str(e)

    finally:
        # Close the database connection
        connection.close()


def insert_repair_info(repair_id: int, assetId: int, repair_date: str, cost: float, repair_type: str) -> Tuple[bool, str]:
    '''
    Inserts repair information based on asset.

    Parameters:
    - repair_id (int): Unique identifier for the repair.
    - assetId (int): Unique identifier for the tractor.
    - repair_date (str): Date the repair was done.
    - cost (float): Cost of the repair.
    - repair_type (str): Type of repair (Example: Oil Change).

    Returns:
    Tuple[bool, str]: Operation success status and a corresponding message.
    '''

    # Connect to the database
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            # Check if the assetId exists in the tractor_info table
            sql = "SELECT * FROM tractor_info WHERE assetId = %s"
            cursor.execute(sql, (assetId,))
            result = cursor.fetchone()

            # If the assetId does not exist in the tractor_info table, insert it
            if result is None:
                print("Asset does not exist in tractor_info.")
                sql = "INSERT INTO tractor_info (assetId) VALUES (%s)"
                cursor.execute(sql, (assetId,))
                connection.commit()

            # Prepare and execute SQL statement to insert into the Repairs table
            sql = "INSERT INTO Repairs (repairId, assetId, Repair_Date, Cost, Repair_Type) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (repair_id, assetId, repair_date, cost, repair_type))

            msg = f"Repair information inserted successfully for assetId: {assetId}!"
            connection.commit()
            return True, msg

    except pymysql.MySQLError as e:
        # Handle database-related errors
        print(f"Database error occurred: {e}")
        return False, str(e)

    except Exception as e:
        # Handle general errors
        print(f"An error occurred: {e}")
        return False, str(e)

    finally:
        # Close the database connection
        connection.close()


def get_repair_info(assetId: str, repair_year: str) -> Union[pd.DataFrame, Tuple[bool, str]]:
    """
    Retrieves repair information based on assetId and repair_year from the database.

    Parameters:
    - assetId (str): Unique identifier for the tractor.
    - repair_year (str): Year when the repair took place.

    Returns:
    - pd.DataFrame: DataFrame containing the repair details if successful.
    - Tuple[bool, str]: Operation status and error message if there's a failure.
    """

    # Connect to the database
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:

            # Both assetId and repair_year are provided
            if assetId and repair_year:
                sql = """SELECT r.repairId, r.assetId, r.Repair_Date, r.Cost, r.Repair_Type, 
                         t.vin, t.inspection_date, t.licence_plate, t.make, t.model, t.axle, t.last_tire_replace_date
                         FROM Repairs r 
                         JOIN tractor_info t ON r.assetID = t.assetId 
                         WHERE r.assetID  = %s AND EXTRACT(YEAR FROM r.Repair_Date) = %s"""
                cursor.execute(sql, (assetId, repair_year))

            # Only assetId is provided
            elif assetId:
                sql = """SELECT r.repairId, r.assetId, r.Repair_Date, r.Cost, r.Repair_Type, 
                         t.vin, t.inspection_date, t.licence_plate, t.make, t.model, t.axle, t.last_tire_replace_date
                         FROM Repairs r 
                         JOIN tractor_info t ON r.assetID = t.assetId 
                         WHERE r.assetID  = %s"""
                cursor.execute(sql, (assetId,))

            # Only repair_year is provided
            elif repair_year:
                sql = """SELECT r.repairId, r.assetId, r.Repair_Date, r.Cost, r.Repair_Type, 
                         t.vin, t.inspection_date, t.licence_plate, t.make, t.model, t.axle, t.last_tire_replace_date
                         FROM Repairs r 
                         JOIN tractor_info t ON r.assetID = t.assetId 
                         WHERE EXTRACT(YEAR FROM r.Repair_Date) = %s"""
                cursor.execute(sql, (repair_year,))

            # Neither assetId nor repair_year is provided
            else:
                sql = """SELECT r.*, t.* FROM Repairs r 
                         JOIN tractor_info t ON r.assetID = t.assetId"""
                cursor.execute(sql)

            # Fetch the result and convert it into a DataFrame
            result = cursor.fetchall()
            df = pd.DataFrame(result)

    except pymysql.MySQLError as e:
        # Handle database-related errors
        print(f"Database error occurred: {e}")
        return False, str(e)

    except Exception as e:
        # Handle general errors
        print(f"An error occurred: {e}")
        return False, str(e)

    finally:
        # Close the database connection
        connection.close()
        return df
    

def get_tractor_info(assetId: str = "") -> pd.DataFrame:
    """
    Fetch tractor information from the database for the provided asset ID.
    If no asset ID is provided, fetch information for all tractors.

    Parameters:
    - asetId: ID of the tractor to fetch information for.
    Returns:
    - A pandas DataFrame containing tractor information.
    """
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            # If no assetId is provided, fetch information for all tractors
            if not assetId:
                sql = """SELECT t.*, SUM(r.Cost) as total_repair_costs
                FROM tractor_info t 
                LEFT JOIN Repairs r ON t.assetId = r.assetId 
                GROUP BY t.assetId"""
                cursor.execute(sql)
            # If an assetId is provided, fetch information only for that tractor
            else:
                sql = """SELECT t.*, SUM(r.Cost) as total_repair_costs
                FROM tractor_info t 
                LEFT JOIN Repairs r ON t.assetId = r.assetId 
                WHERE t.assetId = %s
                GROUP BY t.assetId
                """
                cursor.execute(sql, (assetId,))

            # Fetch the results and convert them into a pandas DataFrame
            result = cursor.fetchall()
            df = pd.DataFrame(result)
    except pymysql.MySQLError as e:
        print(f"Database error occurred: {e}")
        return pd.DataFrame()  # return an empty dataframe in case of error
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()  # return an empty dataframe in case of error
    finally:
        connection.close()
        return df
    

def delete_tractor(assetId: str) -> (bool, str):
    """
    Deletes tractor information from the database for the provided asset ID.
    
    Parameters:
    - assetId: ID of the tractor to delete.
    Returns:
    - A tuple containing a boolean indicating the success status and a message string.
    """
    
    # Connect to the database
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            # Delete tractor information based on assetId
            sql = "DELETE FROM tractor_info WHERE assetId = %s"
            cursor.execute(sql, (assetId,))

            # Commit the transaction
            connection.commit()
            
            # Return a success message
            msg = f"Deleted tractor information successfully for assetId: {assetId}!"
            return True, msg

    except pymysql.MySQLError as e:
        print(f"Database error occurred: {e}")
        return False, str(e)
    except Exception as e:
        print(f"An error occurred: {e}")
        return False, str(e) 
    finally:
        connection.close()
    





