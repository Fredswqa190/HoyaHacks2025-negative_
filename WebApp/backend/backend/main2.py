from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import pyshark
import torch
from inference import load_model
import numpy as np

THRESHOLD = 0.5

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

model = load_model("best_weights.pth")

@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    print("Connect event emitted")
    emit("connect", include_self=False, broadcast=True)

def handle_data(data):
    socketio.emit(
        "wireshark_data",
        {
            "protocol": data["protocol"],
            "source": data["source"],
            "destination": data["destination"],
            "host": data.get("host"),
            "uri": data.get("uri"),
        }
    )

    dangerous = model_quantum(data)
    socketio.emit("dangerous", dangerous)

def model_keras(data):
    data_arr = np.array(
        [[(data["protocol"]), (data["source"]), (data["destination"]), (data["host"]), (data["uri"])]]
    )
    return model.predict(data_arr, verbose=0)[0][0] > THRESHOLD


def model_quantum(data):
    data_arr = torch.tensor(
        [[(data["protocol"]), (data["source"]), (data["destination"]), (data["host"]), (data["uri"])]]
    )
    return model(data_arr)[0][0].item() > THRESHOLD

try:
    capture = pyshark.LiveCapture(interface='Ethernet')
    print("Starting live capture on interface Ethernet...")
    for packet in capture.sniff_continuously():
        protocol = packet.transport_layer
        source = packet.ip.src  # Assuming packet has an IP layer
        destination = packet.ip.dst  # Assuming packet has an IP layer
        host = packet.http.host if 'HTTP' in packet else None  # Assuming packet may have an HTTP layer
        uri = packet.http.request_uri if 'HTTP' in packet else None  # Assuming packet may have an HTTP layer

        data = {
            "protocol": protocol,
            "source": source,
            "destination": destination,
            "host": host,
            "uri": uri,
        }
        handle_data(data)
except AttributeError as e:
    print(f"Packet parsing error: {e}")

if __name__ == "__main__":
    socketio.run(app, debug=True, port=4003)