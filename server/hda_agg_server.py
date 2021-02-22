import sys
sys.path.insert(0, "..")

import time
from hda_agg_clinet_module import *
from opcua import ua, Server
from hda_agg_module import HistorySQLite


if __name__ == "__main__":


        server = Server()
        server.set_endpoint("opc.tcp://172.21.43.150:4840")
        uri = "http://examples.freeopcua.github.io"
        idx = server.register_namespace(uri)
        objects = server.get_objects_node()
        myobj = objects.add_object(idx, "MyObject")
        myvar = myobj.add_variable(idx, "MyVariable", ua.Variant(0, ua.VariantType.Double))
        myvar.set_writable()

        Endpoint_Url = input("Endpoint_Url: ")
        Node_Id = input("Node_Id: ")

        # client = aggclient("opc.tcp://172.21.43.101:53530/OPCUA/SimulationServer", "ns=3;i=1001")
        client = aggclient(Endpoint_Url, Node_Id)
        client.connection()
        # sub = Subscription()
        print(Global.value)
        value1 = Global.value

        server.iserver.history_manager.set_storage(HistorySQLite())
        myvar.set_value(value1)
        server.start()

        server.historize_node_data_change(myvar, period=None, count=100)
        try:
            while server.serverstate == 1:
                value2 = Global.value
                if value1 != value2:
                    myvar.set_value(value2)
                value1 = value2
                    # print(value)
        finally:
            client.disconnection()
            server.stop()
