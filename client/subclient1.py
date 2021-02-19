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
    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """

    def datachange_notification(self, node, val, data):

        print(data.monitored_item.Value.SourceTimestamp)
        print("counter", node, val)


    def event_notification(self, event):
        print("New event recived: ", event)


if __name__ == "__main__":

    client = Client("opc.tcp://172.21.43.101:53530/OPCUA/SimulationServer")
    client.connect()
    myevent =client.get_node("ns=3;i=1001")
    print("MyFirstEventType is: ", myevent)

    handler = SubHandler()
    sub = client.create_subscription(500, handler)
    print("11111111111111")
    sub.subscribe_data_change(myevent)
    print("22222222222222")
    embed()
    print("33333333333333")
    client.disconnect()
