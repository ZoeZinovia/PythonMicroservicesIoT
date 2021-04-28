import paho.mqtt.client as mqtt
import json
import RPi.GPIO as GPIO
import time
import sys

MQTT_SERVER = sys.argv[1]
MQTT_PATH = "LED"
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
num_messages = 0
start = time.time()


def on_connect(client, userdata, flags, rc):
    print("Connected. Result code: "+ str(rc))
    client.subscribe(MQTT_PATH)


# The on_message function runs once a message is received from the broker
def on_message(client, userdata, msg):
    global num_messages
    global start
    num_messages += 1
    if num_messages == 1:
        start = time.time()
    received_json = json.loads(msg.payload) #convert the string to json object
    if "Done" in received_json:
        client.loop_stop()
        client.disconnect()
        end = time.time()
        timer = end - start
        with open("piResultsPython.txt", "a") as myfile:
            myfile.write("LED subscriber runtime = " + str(timer) + "\n")
        print("LED subscriber runtime = " + str(timer) + "\n");
    else:
        led_1_status = received_json["LED_1"]
        led_1_gpio = received_json["GPIO"]
        GPIO.setup(led_1_gpio, GPIO.OUT)
        if led_1_status:
            GPIO.output(led_1_gpio, GPIO.HIGH)
        else:
            GPIO.output(led_1_gpio, GPIO.LOW)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)
client.loop_forever()