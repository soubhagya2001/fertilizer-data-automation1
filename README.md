# Sensor Data Monitoring Web Application

This web application allows users to monitor real-time sensor data through a web interface. Before running the application, ensure that MySQL is installed on your computer. Additionally, install the required Python packages such as Flask, OPCUA, and MySQL connector.

## Installation Instructions

1. **Install MySQL**: If MySQL is not already installed on your system, download and install it from the official MySQL website: [MySQL Downloads](https://dev.mysql.com/downloads/)

2. **Install Required Python Packages**: Install the required Python packages using pip:

    ```bash
    pip install flask opcua mysql-connector-python
    ```

## Usage Instructions

1. **Run `sensors.py`**: This script collects data from sensors and stores it in the MySQL database. Run the following command:

    ```bash
    python sensors.py
    ```

2. **Run `main.py`**: This script initializes the Flask web application and serves the sensor data through a web interface. Run the following command:

    ```bash
    python main.py
    ```

3. **Open Browser**: Open your web browser and navigate to `127.0.0.1:5000` to access the sensor data monitoring web application.

## Files Included

- `sensors.py`: Python script to collect data from sensors and store it in the MySQL database.
- `main.py`: Python script to initialize the Flask web application and serve the sensor data.
- `templates/`: Directory containing HTML templates for the web interface.
- `static/`: Directory containing static files such as CSS stylesheets and JavaScript scripts.
- `README.md`: Markdown file containing installation and usage instructions.

## Requirements

- Python 3.x
- MySQL
- Flask
- OPCUA
- MySQL Connector for Python

