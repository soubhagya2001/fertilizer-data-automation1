import mysql.connector

def establish_connection():
    try:
        connection = mysql.connector.connect(host="localhost", user="root", password="root", database="fertilizer")
        print("Connected successfully")
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def sensorDataToDb(connection, timeStamp, temp, press, humi, sensorId, processId):
    try:
        if connection.is_connected():
            mycursor = connection.cursor()
            insert_sql = "INSERT INTO sensorsdata (timeStamp, temp, press, humi, sensorId, processId) VALUES (%s, %s, %s, %s, %s, %s)"
            insert_value = (timeStamp, temp, press, humi, sensorId, processId)
            mycursor.execute(insert_sql, insert_value)
            connection.commit()
            print("Sensor value inserted in database")
    except mysql.connector.Error as e:
        print(f"Error inserting sensor data: {e}")
    # finally:
    #     if connection.is_connected():
    #         mycursor.close()

def alarmDataToDb(connection, alarmId, timeStamp, description, processId):
    try:
        if connection.is_connected():
            mycursor = connection.cursor()
            mycursor.execute("USE fertilizer")
            insert_sql = "INSERT INTO alarmdata (alarmId, timestamp, description, processId) VALUES (%s, %s, %s, %s)"
            insert_value = (alarmId, timeStamp, description, processId)
            mycursor.execute(insert_sql, insert_value)
            connection.commit()
            print("Alarm data value inserted in database")
    except mysql.connector.Error as e:
        print(f"Error inserting alarm data: {e}")
    # finally:
    #     if connection.is_connected():
    #         mycursor.close()

def fetch_latest_alarm_data(connection, limit):
    try:
        if connection.is_connected():
            mycursor = connection.cursor()
            query = "SELECT * FROM alarmdata ORDER BY timestamp DESC LIMIT %s"
            mycursor.execute(query, (limit,))
            latest_data = mycursor.fetchall()

            data_list = []
            for row in latest_data:
                data_dict = {
                    'timestamp': row[1],
                    'description': row[2],
                    'processId': row[3]
                }
                data_list.append(data_dict)

            return data_list
    except mysql.connector.Error as e:
        print(f"Error fetching latest alarm data: {e}")
    # finally:
    #     if connection.is_connected():
    #         mycursor.close()



def fetch_latest_sensor_data(connection, limit):
    try:
        if connection.is_connected():
            mycursor = connection.cursor()
            query = "SELECT * FROM sensorsdata ORDER BY timeStamp DESC LIMIT %s"
            mycursor.execute(query, (limit,))
            # mycursor.execute(query)
            print("Sensor data retrieval query executed successfully\n\n")
            latest_data = mycursor.fetchall()

            # Convert fetched data to a list of dictionaries
            data_list = []
            for row in latest_data:
                print(row)
                data_dict = {
                    'timestamp': row[0],
                    'temperature': row[1],
                    'pressure': row[2],
                    'humidity': row[3],
                    'sensorId': row[4],
                    'processId': row[5]
                }
                
                data_list.append(data_dict)

            return data_list
    except mysql.connector.Error as e:
        print(f"Error fetching latest sensor data: {e}")
    # finally:
    #     if connection.is_connected():
    #         mycursor.close()