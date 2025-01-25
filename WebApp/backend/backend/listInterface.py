import pyshark

def list_interfaces():
    interfaces = pyshark.LiveCapture.interfaces
    print("Available network interfaces:")
    for interface in interfaces:
        print(interface)

if __name__ == "__main__":
    list_interfaces()