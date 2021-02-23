import sys
sys.path.insert(0, "..")
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse

tree = ET.parse('../OhPLCmapCompleted.xml')
root = tree.getroot()

ns = {'default':'http://opcfoundation.org/UA/2011/03/UANodeSet.xsd'}
# print(root)
print(root.find("default:NamespaceUris", ns))
child = root.find("default:NamespaceUris", ns)
print(child.text)
# for child in root.find('default:NamespaceUris',ns):
#     print(child.text)
# print(root.find('Model').tag,"and",root.find('Model').attrib)