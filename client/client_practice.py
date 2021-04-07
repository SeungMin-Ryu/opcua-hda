import sys

sys.path.insert(0, "..")

from opcua import Client,Node
from opcua import ua

def find_history_node(n):
    for node1 in n.get_children():
        if node1.get_node_class() == ua.NodeClass.Variable and node1.get_attribute(ua.AttributeIds.Historizing).Value.Value == True:
            historizing_node[node1.nodeid.to_string()] = node1.get_display_name().Text
            print('들어감')
        else:
            find_history_node(node1)

if __name__ == "__main__":
    client = Client("opc.tcp://172.21.43.101:53530/OPCUA/SimulationServer")
    # client = Client("opc.tcp://172.21.42.31:4840")
    # client = Client("opc.tcp://172.21.42.201:4871")
    # client = Client("opc.tcp://172.21.50.48:52520")

    historizing_node = {}

    try:
        client.connect()
        object = client.get_objects_node()
        find_history_node(object)
        print(historizing_node)
        '''
        for node1 in object.get_children():
            print(node1)
            if node1.get_node_class() == ua.NodeClass.Variable and node1.get_attribute(ua.AttributeIds.Historizing).Value.Value == True:
                historizing_node[node1.get_display_name().Text] = node1.nodeid.to_string()

            else:
                for node2 in node1.get_children():
                    if node2.get_node_class() == ua.NodeClass.Variable and node2.get_attribute(ua.AttributeIds.Historizing).Value.Value == True:
                        historizing_node[node2.get_display_name().Text] = node2.nodeid.to_string()

                    else:
                        for node3 in node2.get_children():
                            if node3.get_node_class() == ua.NodeClass.Variable and node3.get_attribute(ua.AttributeIds.Historizing).Value.Value == True:
                                historizing_node[node3.get_display_name().Text] = node3.nodeid.to_string()

                            else:
                                for node4 in node3.get_children():
                                    if node4.get_node_class() == ua.NodeClass.Variable and node4.get_attribute(ua.AttributeIds.Historizing).Value.Value == True:
                                        historizing_node[node4.get_display_name().Text] = node4.nodeid.to_string()
        '''
    finally:
        client.disconnect()