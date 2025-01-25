import paho.mqtt.client as mqtt
import csv
import os
import datetime
from pytz import timezone

MQTT_SERVER = "localhost"
MQTT_FIELDS = ["temperature", "humidity", "VOC", "CO2", "PIR"]
fields = MQTT_FIELDS.copy()
fields.append("time")
filename = "sensordata.csv"
sensorqueue = []
sensorqueuelist = {}

for i in MQTT_FIELDS:
    sensorqueuelist[i] = None


def new_row():
    dicta = {}
    for i in MQTT_FIELDS:
        dicta[i] = ""
    sensorqueue.append(dicta)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    for i in range(len(MQTT_FIELDS)):
        client.subscribe("esp32/" + MQTT_FIELDS[i])


def on_message(client, userdata, msg):
    print(msg.topic + " " + msg.payload.decode("ascii"))
    sensorqueuelist[msg.topic.replace("esp32/", "")] = msg.payload.decode("ascii")
    print("Sending Row: ")
    dictionary = {}
    for key in MQTT_FIELDS:
        dictionary[key] = sensorqueuelist[key]
    with open(filename, "a") as csvfile:
        utc_now = datetime.datetime.now(datetime.UTC)
        dictionary["time"] = utc_now.astimezone(timezone("US/Eastern")).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writerow(dictionary)
    csvfile.close()
    print(str(dictionary))


isExist = os.path.exists(filename)

if not isExist:
    new_row()
    with open(filename, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
    csvfile.close()

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)

client.loop_forever()
