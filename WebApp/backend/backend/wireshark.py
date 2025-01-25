import pyshark

def analyze_live_traffic(interface):
    capture = pyshark.LiveCapture(interface=interface)

    print(f"Starting live capture on interface {interface}...")

    for packet in capture.sniff_continuously():
        try:
            print(f"Packet: {packet}")
            
            if 'IP' in packet:
                ip_layer = packet['IP']
                print(f"Source IP: {ip_layer.src}")
                print(f"Destination IP: {ip_layer.dst}")
            
            if 'TCP' in packet:
                tcp_layer = packet['TCP']
                print(f"Source Port: {tcp_layer.srcport}")
                print(f"Destination Port: {tcp_layer.dstport}")
            
            if 'HTTP' in packet:
                http_layer = packet['HTTP']
                print(f"HTTP Host: {http_layer.host}")
                print(f"HTTP URI: {http_layer.request_uri}")
            
            if 'UDP' in packet:
                udp_layer = packet['UDP']
                print(f"Source Port: {udp_layer.srcport}")
                print(f"Destination Port: {udp_layer.dstport}")

        except AttributeError as e:
            print(f"Packet parsing error: {e}")

if __name__ == "__main__":
    analyze_live_traffic('Ethernet')