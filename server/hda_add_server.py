import sys
sys.path.insert(0, "..")
mod = sys.modules[__name__]

from hda_agg_module.hda_agg_clinet_module import *
from opcua import ua, Server
from hda_agg_module.hda_agg_module import HistorySQLite


if __name__ == "__main__":


        server = Server()
        server.set_endpoint("opc.tcp://172.21.43.150:4840")
        uri = "http://examples.freeopcua.github.io"
        idx = server.register_namespace(uri)
        objects = server.get_objects_node()
        myobj = objects.add_object(idx, "MyObject")

        count = 0
        count_client = int(input("Number of clients: "))


        for num_clients in range(0, count_client):
            Endpoint_Url = input("Endpoint_Url: ")
            Node_Id = input("Node_Id: ")
            globals()['variable_{}'.format(num_clients)] = aggclient(Endpoint_Url, Node_Id)
            globals()['variable_{}'.format(num_clients)].connection()


        # client = aggclient("opc.tcp://172.21.43.101:53530/OPCUA/SimulationServer", "ns=3;i=1001")
        # client = aggclient("opc.tcp://172.21.42.31:4840", "ns=5;i=6023")

        client_node_id = list(Global.node_display.keys())
        client_display_name = list(Global.node_display.values())
        client_variable_type = list(Global.node_type.values())


        server.iserver.history_manager.set_storage(HistorySQLite())
        server.start()
        for server_display_name in client_display_name:
            print('노드생성')
            globals()['node_{}'.format(count)] = myobj.add_variable(client_node_id[count],
                                                                          server_display_name,
                                                                          0,
                                                                          client_variable_type[count])
            server.historize_node_data_change(globals()['node_{}'.format(count)], period=None, count=100)
            count += 1
        try:
            while server.serverstate == 1:
                if Global.value and Global.node and Global.vartype is not None:
                    for num in range(0, len(Global.node)):
                        print(num)
                        server.get_node(Global.node[num]).set_value(value=Global.value[num], varianttype=Global.vartype[num])
        finally:
            # client.disconnection()
            server.stop()
