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

        print(data.monitored_item.Value.ServerTimestamp)
        print(data.monitored_item.Value.SourceTimestamp)
        print(data.monitored_item.Value.StatusCode)
        print("counter", node, val)
        cur.execute(sql,(data.monitored_item.Value.ServerTimestamp, data.monitored_item.Value.SourceTimestamp, data.monitored_item.Value.StatusCode, val))
        con.commit()


    def event_notification(self, event):
        print("New event recived: ", event)


if __name__ == "__main__":


    con = pymysql.connect(host = 'localhost', user = 'root', password='fbtmdals12', db = 'test1', charset='utf8')
    cur = con.cursor()
    sql = "insert into test1(ServerTimestamp,SourceTimestamp,statusCode,value) values(%s,%s,%s,%s)"

    client = Client("opc.tcp://DESKTOP-6SNC49B:53530/OPCUA/SimulationServer")
    client.connect()

    myevent =client.get_node("ns=3;i=1001")
    print("MyFirstEventType is: ", myevent)

    handler = SubHandler()
    sub = client.create_subscription(500, handler)
    handle4 = sub.subscribe_data_change(myevent)

    embed()
    con.close()
    client.disconnect()
