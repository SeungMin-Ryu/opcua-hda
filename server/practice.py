import sys
sys.path.insert(0, "..")
import xmlschema
from pprint import pprint

from opcua import ua, Server, Client

if __name__ == "__main__":

        '''
        server = Server()
        server.set_endpoint("opc.tcp://172.21.43.150:4840")
        server.import_xml("../xml_folder/OhPLCmapCompleted.xml")
        server.start()
   
        # client = Client('opc.tcp://172.21.43.101:53530/OPCUA/SimulationServer')
        client = Client()
        client.import_xml("../xml_folder/OhPLCmapCompleted.xml")
        ns_array = client.get_
        '''
        xml_file = '../xml_folder/OhPLCmapCompleted.xml'
        xsd_file = '../xml_folder/UANodeSet.xsd'
        xs = xmlschema.XMLSchema(xsd_file).create_bindings(xml_file)
        # pprint(xs.to_dict('../xml_folder/OhPLCmapCompleted.xml'))
        # xs.is_valid('../xml_folder/OhPLCmapCompleted.xml')
        # obj = xs.to_objects('../xml_folder/OhPLCmapCompleted.xml')
        #
        # print(obj.namespaces)

        # xmlschema.validate(xml_file,schema=xsd_file)