from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from connect_mqtt import connect_mqtt
import torch
from inference import load_model
import numpy as np
import time
import pyshark
import threading

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

occupancy_model = load_model("best_weights.pth")
OCCUPANCY_THRESHOLD = 0.5

model = load_model("best_weights.pth")
THRESHOLD = 0.5

start = time.time()
packet_count = 0

def rand_float():
    return round(100 * abs(np.random.normal()), 3)

@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    print("Connect event emitted")
    emit("connect", include_self=False, broadcast=True)

def handle_sensor_data(data):
    socketio.emit(
        "sensor_data",
        {
            "temperature": data["temperature"],
            "co2": data["CO2"],
            "humidity": data["humidity"],
            "voc": data["VOC"],
            "pir": data["PIR"],
        },
    )

    occupancy = occupancy_model_quantum(data)
    socketio.emit("occupancy", occupancy)

def occupancy_model_keras(data):
    data_arr = np.array(
        [[float(data["temperature"]), float(data["humidity"]), float(data["CO2"])]]
    )
    return occupancy_model.predict(data_arr, verbose=0)[0][0] > OCCUPANCY_THRESHOLD

def occupancy_model_quantum(data):
    data_arr = torch.tensor(
        [[float(data["temperature"]), float(data["humidity"]), float(data["CO2"])]]
    )
    return occupancy_model(data_arr)[0][0].item() > OCCUPANCY_THRESHOLD

def handle_data_packet(data):
    global packet_count
    socketio.emit(
        "wireshark_data",
        {
            "protocol": data["protocol"],
            #"source": data["source"],
            #"destination": data["destination"],
            #"host": data.get("host"),
            #"uri": data.get("uri"),
        }
    )
    packet_count += 1
    socketio.emit("packet_count", {"count": packet_count})

    #dangerous = model_quantum(data)
    socketio.emit("dangerous", True)

def emit_packet_count():
    global packet_count
    while True:
        time.sleep(10)
        socketio.emit("packet_count", {"count": packet_count})
        packet_count = 0

threading.Thread(target=emit_packet_count).start()

def start_packet_capture():
    try:
        interface = 'Ethernet'
        capture = pyshark.LiveCapture(interface=interface)
        print(f"Starting live capture on interface {interface}...")
        for packet in capture.sniff_continuously():
            protocol = packet.transport_layer
            data = {
                "protocol": protocol,
            }
            handle_data_packet(data)
    except Exception as e:
        print(f"Failed to start live capture: {e}")

capture_thread = threading.Thread(target=start_packet_capture)
capture_thread.start()

try:
    print("Connecting to mqtt...")
    connect_mqtt(handle_data=handle_sensor_data)
except Exception as e:
    print(f"Failed to connect to mqtt: {e}")

if __name__ == "__main__":
    socketio.run(app, debug=True, port=4003)
