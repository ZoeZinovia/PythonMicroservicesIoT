import time
import paho.mqtt.publish as publish
import json
from gpiozero import MotionSensor
import RPi.GPIO as GPIO
import sys

start = time.time()

MQTT_SERVER = sys.argv[1]
MQTT_PATH = "PIR"

# Initial the pir device, with data pin connected to 17:
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
# pir = MotionSensor(17)
presence = False

count = 0
while count < 20:
    try:
        presence = GPIO.input(17)
        temp_json = {"PIR": presence}
        publish.single(MQTT_PATH, json.dumps(temp_json), port=1883, hostname=MQTT_SERVER)

    except RuntimeError as error:  # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
    count += 1

publish.single(MQTT_PATH, json.dumps({"Done": True}), port=1883, hostname=MQTT_SERVER)
end = time.time()
print("PIR publisher runtime = " + str(end-start))
with open("piResultsPython.txt", "a") as myfile:
    myfile.write("PIR publisher runtime = " + str(end - start) + "\n")
