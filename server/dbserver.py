import sys
sys.path.insert(0, "..")
import time
import pymysql

from opcua import ua, Server


if __name__ == "__main__":
    con = pymysql.connect(host='172.21.43.101', user='seungmin', password='fbtmdals12', db='subclient', charset='utf8')
    cur = con.cursor()
    sql = "select counter from subclient order by id desc limit 1"
    cur.execute(sql)
    result = cur.fetchall()
    for row_data in result:
        print(row_data[0])
    print(type(result))
    print(len(result))
    print(result)
    print(result[0])



    server = Server()
    server.set_endpoint("opc.tcp://172.21.43.200:4840")

    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    objects = server.get_objects_node()

    myobj = objects.add_object(idx, "MyObject")
    myvar = myobj.add_variable(idx, "MyVariable", 20)
    myvar.set_writable()


    server.start()
    server.historize_node_data_change(myvar, period=None, count=100)
    time.sleep(10)
    myvar.set_value(row_data[0])
    con.close()
    # try:
    #     count = 0
    #     while True:
    #         time.sleep(5)
    #         count += 0.1
    #         myvar.set_value(count)
    # finally:
    # server.stop()
