from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from connect_mqtt import connect_mqtt
import torch
from inference import load_model
import numpy as np
import time
import threading
from wireshark import start_packet_capture, emit_packet_count

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

occupancy_model = load_model("best_weights.pth")
OCCUPANCY_THRESHOLD = 0.5

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
            "soundlevel": data["soundlevel"],
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

try:
    print("Connecting to mqtt...")
    connect_mqtt(handle_data=handle_sensor_data)
except Exception as e:
    print(f"Failed to connect to mqtt: {e}")

capture_thread = threading.Thread(target=start_packet_capture, args=(socketio,))
capture_thread.start()

emit_thread = threading.Thread(target=emit_packet_count, args=(socketio,))
emit_thread.start()

if __name__ == "__main__":
    socketio.run(app, debug=True, port=4003)