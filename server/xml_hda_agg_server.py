import sys
sys.path.insert(0, "..")

from xml_module.xml_hda_agg_client_module import *
import xml.etree.ElementTree as ET
from opcua import ua, Server
from hda_agg_module.hda_agg_module import HistorySQLite


if __name__ == "__main__":
        tree = ET.parse('../xml_folder/OhPLCmapCompleted.xml')
        root = tree.getroot()

        namespace_uri = []

        for name in root.iter('{http://opcfoundation.org/UA/2011/03/UANodeSet.xsd}Uri'):
            namespace_uri.append(name.text)

        server = Server()
        server.set_endpoint("opc.tcp://172.21.43.150:4840")
        # uri = "http://examples.freeopcua.github.io"
        idx = server.register_namespace(namespace_uri[-1])

        Global.namespace = namespace_uri[-1]

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

        server.iserver.history_manager.set_storage(HistorySQLite())
        myvar.set_value(Global.value)

        server.start()

        server.historize_node_data_change(myvar, period=None, count=100)
        try:
          while server.serverstate == 1:
              myvar.set_value(Global.value)

        finally:
          client.disconnection()
          server.stop()
