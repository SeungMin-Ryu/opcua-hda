import sys
sys.path.insert(0, "..")
mod = sys.modules[__name__]

from hda_agg_module.hda_agg_client_module import *
from opcua import ua, Server
from hda_agg_module.hda_agg_module import HistorySQLite


if __name__ == "__main__":


        server = Server()
        server.set_endpoint("opc.tcp://172.21.43.150:4840")
        uri = "http://examples.freeopcua.github.io"
        idx = server.register_namespace(uri)
        objects = server.get_objects_node()
        myobj = objects.add_object(idx, "MyObject")

        client = aggclient("opc.tcp://172.21.43.101:53530/OPCUA/SimulationServer")
        # client = aggclient("opc.tcp://172.21.50.48:52520")
        client.connection()

        client_display_name = list(client.historizing_node.values())
        client_node_id = list(client.historizing_node.keys())
        client_node_datatype = list(client.historizing_node_datatype.values())

        server.iserver.history_manager.set_storage(HistorySQLite())
        server.start()

        a = 0
        for server_display_name in client_display_name:
            globals()['variable_{}'.format(a)] = myobj.add_variable(client_node_id[a], server_display_name, 0, client_node_datatype[a])
            server.historize_node_data_change(globals()['variable_{}'.format(a)], period=None, count=100)
            a += 1
        try:
            while server.start():
                if Global.node is not None:

                    for num in range(0, len(Global.node)):
                        server.get_node(Global.node[num]).set_value(value=Global.var[num], varianttype=Global.vartype[num])


        finally:
            client.disconnection()
            server.stop()
