import sys
sys.path.insert(0, "..")
import time
import math


from opcua import ua, Server
from opcua.server.history_sql import HistorySQLite


if __name__ == "__main__":

    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://172.21.43.200:4840")

    # setup our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our custom stuff
    objects = server.get_objects_node()

    # populating our address space
    myobj = objects.add_object(idx, "MyObject")
    myvar = myobj.add_variable(idx, "MyVariable", ua.Variant(0, ua.VariantType.Double))
    myvari = myobj.add_variable(idx, "MyVariable1", ua.Variant(0, ua.VariantType.Double))
    myvar.set_writable()  # Set MyVariable to be writable by clients
    myvari.set_writable()  # Set MyVariable to be writable by clients

    # Configure server to use sqlite as history database (default is a simple memory dict)
    # server.iserver.history_manager.set_storage(HistorySQLite("my_datavalue_history11.sql"))

    # starting!
    server.start()

    # enable data change history for this particular node, must be called after start since it uses subscription
    server.historize_node_data_change(myvar, period=None, count=1000)
    server.historize_node_data_change(myvari, period=None, count=1000)

    try:
        count = 0
        while True:
            time.sleep(1)
            count += 0.1
            myvar.set_value(math.sin(count))
            myvari.set_value(math.cos(count))

    finally:
        # close connection, remove subscriptions, etc
        server.stop()