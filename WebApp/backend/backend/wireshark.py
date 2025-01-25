import pyshark
import threading
import time
import asyncio

packet_count = 0

def emit_packet_count(socketio):
    global packet_count
    while True:
        time.sleep(10)
        print("packets", packet_count)
        socketio.emit("packet_count", {"count": packet_count})
        packet_count = 0

async def capture_packets(socketio):
    global packet_count
    try:
        interface = 'Wi-Fi'
        capture = pyshark.LiveCapture(interface=interface, output_file='capture.pcap')
        print(f"Starting live capture on interface {interface}...")

        while True:
            capture.sniff(timeout=10)
            packet_count += len(capture)
            print(f"Captured {len(capture)} packets")
            capture.clear()
            socketio.emit("wireshark_data", {"packet_count": packet_count})
            await asyncio.sleep(0)  

    except Exception as e:
        print(f"Failed to start live capture: {e}")

def start_packet_capture(socketio):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(capture_packets(socketio))

if __name__ == "__main__":
    from flask_socketio import SocketIO
    from flask import Flask

    app = Flask(__name__)
    socketio = SocketIO(app, cors_allowed_origins="*")

    capture_thread = threading.Thread(target=start_packet_capture, args=(socketio,))
    capture_thread.start()

    emit_thread = threading.Thread(target=emit_packet_count, args=(socketio,))
    emit_thread.start()

    socketio.run(app, debug=True, port=4003)