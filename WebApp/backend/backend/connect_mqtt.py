import paho.mqtt.client as mqtt
import datetime
import threading
from pytz import timezone

MQTT_SERVER = "192.168.97.182"
MQTT_FIELDS = ["temperature", "humidity", "VOC", "CO2", "PIR"]
fields = MQTT_FIELDS.copy()
fields.append("time")
filename = "sensordata.csv"
sensorqueue = []
sensorqueuelist = {}
sensorqueuechange = {}

for i in MQTT_FIELDS:
    sensorqueuelist[i] = None
    sensorqueuechange[i] = 0


def new_row():
    dicta = {}
    for i in MQTT_FIELDS:
        dicta[i] = ""
    sensorqueue.append(dicta)

def reset_change():
    for i in sensorqueuechange:
        sensorqueuechange[i] = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    for i in range(len(MQTT_FIELDS)):
        client.subscribe("esp32/" + MQTT_FIELDS[i])


def on_message(client, userdata, msg, handle_data):
    sensorqueuelist[msg.topic.replace("esp32/", "")] = msg.payload.decode('ascii')
    sensorqueuechange[msg.topic.replace("esp32/", "")] = 1
    if all(value == 1 for value in sensorqueuechange.values()):
        dictionary = {}
        for key in MQTT_FIELDS:
            dictionary[key] = sensorqueuelist[key]

        utc_now = datetime.datetime.utcnow()
        dictionary["time"] = utc_now.astimezone(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')

        handle_data(dictionary)

        reset_change()

def connect_mqtt(handle_data):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    client.on_connect = on_connect
    client.on_message = lambda client, userdata, msg: on_message(client, userdata, msg, handle_data)
    client.connect(MQTT_SERVER, 1883, 60)

    thread = threading.Thread(target=client.loop_forever)
    thread.start()
