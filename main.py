import time
import board
import adafruit_dht
import paho.mqtt as mqtt
import json

#Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D4)

count = 0
while count<20:
    try:
         # Print the values to the serial port
         temperature = dhtDevice.temperature
         humidity = dhtDevice.humidity
         print("Temp: {:.1f} C    Humidity: {}% "
               .format(temperature, humidity))

    except RuntimeError as error:     # Errors happen fairly often, DHT's are hard to read, just keep going
         print(error.args[0])
    count += 1