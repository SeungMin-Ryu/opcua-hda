import sys
from opcua.ua.ua_binary import variant_from_binary, variant_to_binary

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
        print(data.monitored_item.Value.StatusCode.value)
        print(data.monitored_item.Value.Value)
        print(data.monitored_item.Value.Value.VariantType.name)
        print(pymysql.Binary(variant_to_binary(data.monitored_item.Value.Value)))
        # print("counter", node, val)
        cur.execute(sql,(None, data.monitored_item.Value.SourceTimestamp,
                         data.monitored_item.Value.StatusCode.value, data.monitored_item.Value.Value.Value,
                         data.monitored_item.Value.Value.VariantType.name,
                         pymysql.Binary(variant_to_binary(data.monitored_item.Value.Value))))
        con.commit()


    def event_notification(self, event):
        print("New event recived: ", event)


if __name__ == "__main__":


    con = pymysql.connect(host ='172.21.43.101', user ='seungmin', password='fbtmdals12', db ='subclient', charset='utf8')
    cur = con.cursor()
    sql = "insert into test1(ServerTimestamp,SourceTimestamp,StatusCode,Value,VariantType,VariantBinary)" \
          "values(%s, %s, %s, %s, %s, %s)"


    client = Client("opc.tcp://172.21.43.101:53530/OPCUA/SimulationServer")
    client.connect()

    myevent =client.get_node("ns=3;i=1001")

    print("MyFirstEventType is: ", myevent)

    handler = SubHandler()
    sub = client.create_subscription(500, handler)
    handle4 = sub.subscribe_data_change(myevent)

    embed()
    con.close()
    client.disconnect()
