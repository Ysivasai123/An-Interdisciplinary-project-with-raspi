import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import mysql.connector

# Connect to MySQL server
connection = mysql.connector.connect(
    host=" ",                                       #root address of amazon of RDS
    user="",                                        #user name
    password=" ",                                   #Password
    database=" "                                    #Database name
)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

DHT_PIN=17
MOISTURE_PIN = 18

DHT_SENSOR = Adafruit_DHT.DHT11                     #for DHT pin

GPIO.setmode(GPIO.BCM)                              #Broadcom SOC channel
GPIO.setup(MOISTURE_PIN, GPIO.IN)

try:
    
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        moisture_level = GPIO.input(MOISTURE_PIN)
        
        if humidity is not None and temperature is not None:
        
            insert_query = "INSERT INTO myApp_agriculture (motor, temp, humidity, soil_moisture) VALUES (%s, %s, %s, %s)"
            data_to_insert = ("OFF", temperature, humidity, moisture_level)

            cursor.execute(insert_query, data_to_insert)
            connection.commit()

            print(f'Temperature: {temperature:.2f}  Humidity: {humidity:.2f}  Moisture: {moisture_level:.2f}')
            time.sleep(2)
        else:
            print("failed")

except KeyboardInterrupt:
    print("Existing....")
finally:
    GPIO.cleanup()

cursor.close()
connection.close()

