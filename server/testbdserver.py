import sys
sys.path.insert(0, "..")

import time
import pymysql

from opcua import ua, Server
from myhistory import HistorySQLite


if __name__ == "__main__":
    con = pymysql.connect(host='172.21.43.101', user='seungmin', password='fbtmdals12', db='subclient', charset='utf8')
    cur = con.cursor()
    sql = "select value from test1 order by _id desc limit 1"
    cur.execute(sql)
    result1 = cur.fetchone()
    con.commit()
    print(result1[0])


    # print(type(row_data[0]))

    server = Server()
    server.set_endpoint("opc.tcp://172.21.43.150:4840")

    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    objects = server.get_objects_node()

    myobj = objects.add_object(idx, "MyObject")
    myvar = myobj.add_variable(idx, "MyVariable", ua.Variant(0, ua.VariantType.Double))
    myvar.set_writable()
    myvar.set_value(result1[0])
    server.iserver.history_manager.set_storage(HistorySQLite("my_datavalue_history11.sql"))
    print("111111111", server.serverstate)
    server.start()
    print("222222222", server.serverstate)
    server.historize_node_data_change(myvar, period=None, count=20)
    x = list(result1)
    while server.serverstate == 1:
        # print("111111111111111", x[0])
        cur.execute(sql)
        result2 = cur.fetchone()
        con.commit()
        # print("222222222222222", result2[0])
        if x[0] != result2[0]:
            myvar.set_value(result2[0])
        x[0] = result2[0]
        # time.sleep(1)

    con.close()
    server.stop()
