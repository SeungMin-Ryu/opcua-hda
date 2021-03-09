import sys


sys.path.insert(0, "..")
import pymysql
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


class SubHandler(object):

    def datachange_notification(self, node, val, data):

        print(data.monitored_item.Value.SourceTimestamp)
        print("counter", node, val,data)


    def event_notification(self, event):
        print("New event recived: ", event)


if __name__ == "__main__":

    client = Client("opc.tcp://172.21.43.101:53530/OPCUA/SimulationServer")
    client.connect()
    myevent =client.get_node("ns=3;i=1001")
    myevent2 = client.get_namespace_array()
    myevent3 = client.get_namespace_index('http://www.prosysopc.com/OPCUA/SimulationServer/')

    print("11111111111111111111111111111111111",myevent2)
    print("2222222222222222222222222222222",myevent3)
    print("MyFirstEventType is: ", myevent)

    handler = SubHandler()
    sub = client.create_subscription(500, handler)
    sub.subscribe_data_change(myevent)
    embed()
    client.disconnect()
