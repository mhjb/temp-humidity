# import board
import Adafruit_DHT
# import adafruit_dht
import pymongo
import os
from time import sleep
from datetime import datetime

# print(dir(board))
# dht = adafruit_dht.DHT22(board.D18)
# print(dht.temperature)
# exit()
DHT_SENSOR = Adafruit_DHT.AM2302

DHT_PIN = 18
TEMP_CORRECTION = -2
SENSOR_NAME = 'ex-cai-pi-outside-east'


print('Connecting to database')

client = pymongo.MongoClient(os.environ['mongo_conn_string'])
db = client.temperature_humidity
Measurements = db['measurements']


while True:
#	humidity, temperature = dht_device
	humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
	temperature += TEMP_CORRECTION

	if humidity is not None and temperature is not None:
		print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
		Measurements.insert_one({
			'temperature': round(temperature, 1),
			'humidity': round(humidity, 1),
			'sensor_name': SENSOR_NAME,
            'created_at': datetime.utcnow()
		})
		sleep(60*5)
	else:
		print("Failed to retrieve data from humidity sensor")

