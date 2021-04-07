import sys
mod = sys.modules[__name__]
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
from opcua import Client, ua

class Global(object):
    """
    main으로 넘겨줄 전역 변수 노드아이디, 값, 값의 type
    """
    node = None
    var = None
    vartype = None

class Subscription(object):
    def __init__(self):
        self.node = {}          #value 노드 아이디, 값 저장
        self.nodetype = {}      #vaule 노드 타입 저장

    def datachange_notification(self, node, val, data):
        """

        튜플로 노드아이디:값, 노드아이디: variable type
        리스트화 시켜서 각각의 변수를 전역변수에 넣어준다.

        :param node: subscription 의 노드아이디
        :param val: subscription 되고있는 노드의 value값
        :param data: 데이터의 타입등 저장되는값
        """
        self.node[node] = val
        self.nodetype[node] = data.monitored_item.Value.Value.VariantType
        Global.node = list(self.node.keys())
        Global.var = list(self.node.values())
        Global.vartype = list(self.nodetype.values())

class aggclient:

    def __init__(self, uri):
        self.uri = uri
        self.client = Client(self.uri)
        self.historizing_node = {}
        self.historizing_node_datatype = {}

    def find_history_node(self, n):
        """
        client로서 agg server에 붙어서 변수의 클래스가 variable이면서 historizing이 true일 경우
        historizing_node라는 튜플에다가 nodeid:display name을 넣고
        historizing_node_datatype이라는 튜플에다가 nodeid:variant_type을 넣어준다.
        """
        for node1 in n.get_children():
            if node1.get_node_class() == ua.NodeClass.Variable and node1.get_attribute(ua.AttributeIds.Historizing).Value.Value == True:
                self.historizing_node[node1.nodeid.to_string()] = node1.get_display_name().Text
                self.historizing_node_datatype[node1.nodeid.to_string()] = node1.get_data_type_as_variant_type()
                print('find historizing node:',node1.nodeid.to_string())
            else:
                self.find_history_node(node1)       #자식노드 끝까지 들어가서 확인해준다.

    def connection(self):
        """
        main에서 호출되는 함수
        agg서버에 접속하도 find_history_node를 이용하여 서버의 address space에서
        historizing 변수를 빼온후 mynode라는 리스트에 쌓아준다.

        """
        self.client.connect()
        object_node = self.client.get_objects_node()
        aggclient.find_history_node(self, object_node)

        mynode = []
        for nodeid in self.historizing_node.keys():
            mynode.append(self.client.get_node(nodeid))


        handler = Subscription()
        sub = self.client.create_subscription(500, handler)
        sub.subscribe_data_change(mynode)               #mynode라는 노드아이디가 담긴 리스트를 subscription 메소드에 넣어준다.

    def disconnection(self):
        self.client.disconnect()

