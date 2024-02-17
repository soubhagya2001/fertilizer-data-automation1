from flask import Flask, render_template, jsonify
from opcua import Client
import time
import db

app = Flask(__name__)

pNum = 0

# Establish MySQL connection
connection = db.establish_connection()

@app.route('/')
def index():
    if connection:
        #latest_sensor_data = db.fetch_latest_sensor_data(connection, 10)
        #latest_alarm_data = db.fetch_latest_alarm_data(connection, 10)
        return render_template('index.html')
    else:
        return "Failed to connect to MySQL."

@app.route('/live-data')
def live_data():
    if connection:
        print("sensor data is going to be fetched from DB")
        live_data = db.fetch_latest_sensor_data(connection,10)  # Corrected function name
        # print(live_data)
        return jsonify(live_data)
    else:
        return "Failed to connect to MySQL."

@app.route('/live-alarm')
def live_alarm():
    if connection:
        live_data = db.fetch_latest_alarm_data(connection, 10)  # Fetching latest 10 alarm data
        return jsonify(live_data)
    else:
        return "Failed to connect to MySQL."

def alarmForTemperature(timeValue, temp, pId):
    if connection:
        descr = ""
        if temp >= 40:
            descr = "High High"
        elif temp < 40 and temp >= 30:
            descr = "High"
        elif temp < 30 and temp >= 20:
            descr = "Low"
        elif temp < 20 and temp >= 10:
            descr = "Low Low"
    
        db.alarmDataToDb(connection, alarmId=1, timeStamp=timeValue, description=descr, processId=pId)

def update_sensor_data():
    global pNum
    while True:
        if connection:
            live_data = fetch_live_sensor_data()  # Corrected function name
            db.sensorDataToDb(connection, timeStamp=live_data['time'], temp=live_data['temperature'], 
                               press=live_data['pressure'], humi=live_data['humidity'], 
                               sensorId=1, processId=pNum)
            alarmForTemperature(live_data['time'], live_data['temperature'], pNum)
        else:
            print("Failed to connect to MySQL.")
        time.sleep(4)


def fetch_live_sensor_data():
    try:
        url = "opc.tcp://10.58.2.223:4840"
        client = Client(url)
        client.connect()

        # Get node objects
        temperature_node = client.get_node("ns=2;i=2")
        pressure_node = client.get_node("ns=2;i=3")
        time_node = client.get_node("ns=2;i=4")
        humidity_node = client.get_node("ns=2;i=5")

        # Read current values
        temperature = temperature_node.get_value()
        pressure = pressure_node.get_value()
        time_value = time_node.get_value()
        humidity = humidity_node.get_value()

        # Disconnect from OPC UA server
        client.disconnect()

        # Create a dictionary to store the sensor data
        sensor_data = {
            'temperature': temperature,
            'pressure': pressure,
            'time': time_value,
            'humidity': humidity
        }

        return sensor_data
    except Exception as e:
        print(f"Error fetching live sensor data: {e}")
        return None

if __name__ == '__main__':
    import threading
    update_thread = threading.Thread(target=update_sensor_data)
    update_thread.start()

    app.run(debug=True)
