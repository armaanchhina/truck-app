import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             database='tractor_database',
                             cursorclass=pymysql.cursors.DictCursor)


# try:
#     with connection.cursor() as cursor:
#         sql = "INSERT INTO tractor_info (assetId, vin, total_repair_costs, inspection_date) VALUES (%s, %s, %s, %s)"
#         cursor.execute(sql, (1, 123456, 1000, '2023-05-30'))
        
        

#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()


# finally:
#     connection.close()


def insert_new_tractor_info(assetId: int, inspection_date: str = None, vin: int = 0, total_repair_costs: int = 0 ):
    # SQL query to insert into tractor_info table
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO tractor_info (assetId, vin, total_repair_costs, inspection_date) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (assetId, vin, total_repair_costs, inspection_date))
            connection.commit()
    finally:
            connection.close()

def delete_tractor_info(assetId: int):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM tractor_info WHERE assetId = %s"
            cursor.execute(sql, (assetId,))
            connection.commit()
    finally:
            connection.close()


def insert_repair_info(repair_id: int, assetId: int, repair: str, repair_date: str, cost: float, repair_type: str):
    # SQL query to insert into Repairs table
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Repairs (repairId, assetId, Repair_Date, Cost, Repair_Type) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (repair_id, assetId, repair_date, cost, repair_type))
            connection.commit()
    finally:
        connection.close()

def get_repair_info(assetId: int):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Repairs WHERE assetID  = %s"
            cursor.execute(sql, (assetId,))
    finally:
        result = cursor.fetchall()
        connection.close()


# insert_new_tractor_info(3)
# delete_tractor_info(3)
# delete_tractor_info(1)
