import sys
import server.hda_agg_server as ryu
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
    value = 0.0

class Subscription(object):

    def datachange_notification(self, node, val, data):
        Global.value = data.monitored_item.Value.Value.Value
        print("counter=", Global.value)
        print(type(Global.value))
        # return value

class aggclient:

    def __init__(self, uri, node_id):
        self.uri = uri
        self.node_id = node_id
        self.client = Client(self.uri)
    def connection(self):
        # client = Client(self.uri)
        self.client.connect()
        mynode = self.client.get_node(self.node_id)
        print(mynode)

        handler = Subscription()
        sub = self.client.create_subscription(500, handler)
        sub.subscribe_data_change(mynode)

    def disconnection(self):
        self.client.disconnect()

