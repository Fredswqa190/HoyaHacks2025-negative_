import asyncio
import pyshark
import threading

def capture_packets():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    interface = "Wi-Fi"
    capture = pyshark.LiveCapture(interface=interface)
    capture.sniff(timeout=5)
    print(len(capture))
    return(len(capture))

def emit_packet_count(socketio):
    """Emit packet count to the client"""
    while True:
        packet_count = capture_packets()
        socketio.emit("packet_count", packet_count)

# Create and start your thread
thread = threading.Thread(target=capture_packets)
thread.start()
thread.join() 