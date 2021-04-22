import sys
# import server.hda_agg_server as ryu
sys.path.insert(0, "..")
try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()
from opcua import Client

class Global(object):
    node = None
    value = None
    vartype = None
    node_display = {}
    node_type = {}


class Subscription(object):
    def __init__(self):
        self.node = {}          #value 노드 아이디, 값 저장
        self.nodetype = {}      #vaule 노드 타입 저장

    def datachange_notification(self, node, val, data):
        self.node[node] = val
        self.nodetype[node] = data.monitored_item.Value.Value.VariantType
        Global.node = list(self.node.keys())
        Global.value = list(self.node.values())
        Global.vartype = list(self.nodetype.values())

class aggclient:

    def __init__(self, uri, node_id):
        self.uri = uri
        self.node_id = node_id
        self.client = Client(self.uri)

    def connection(self):
        self.client.connect()
        mynode = self.client.get_node(self.node_id)
        Node_id = self.node_id
        Display_name = self.client.get_node(self.node_id).get_display_name().Text
        Data_type = self.client.get_node(self.node_id).get_data_type_as_variant_type()
        # print('노드아이디:',Node_id,'이름:',Display_name,'타입:',Data_type)
        Global.node_display[Node_id] = Display_name
        Global.node_type[Node_id] = Data_type
        # print(Global.node_display)
        handler = Subscription()
        sub = self.client.create_subscription(500, handler)
        sub.subscribe_data_change(mynode)

    def disconnection(self):
        self.client.disconnect()

