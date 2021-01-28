import time
from opcua import Client


if __name__ == "__main__":

    client = Client("opc.tcp://172.21.43.101:53530/OPCUA/SimulationServer")

    client.connect()

    while True:

        root = client.get_node("ns=3;i=1001")
        print(root.get_value())
        time.sleep(1)


    client.disconnect()