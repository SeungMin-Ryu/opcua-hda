import sys
sys.path.insert(0, "..")
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse

tree = ET.parse('../OhPLCmapCompleted.xml')
root = tree.getroot()

ns = {'default':'http://opcfoundation.org/UA/2011/03/UANodeSet.xsd',
      'xsi':'http://www.w3.org/2001/XMLSchema-instance',
      'uax':'http://opcfoundation.org/UA/2008/02/Types.xsd',
      'si':'http://www.siemens.com/OPCUA/2017/SimaticNodeSetExtensions',
      'xsd':'http://www.w3.org/2001/XMLSchema',
      's1':'http://www.smic.kr/SMIC_PDT_v01/Types.xsd',
      'ua':'http://unifiedautomation.com/Configuration/NodeSet.xsd'}
namespace = []
varname = []



for name in root.iter('{http://opcfoundation.org/UA/2011/03/UANodeSet.xsd}Uri'):
    # print(name.text)
    namespace.append(name.text)
print(namespace[-1])
# namespaceuri


for find in root.iter('{http://opcfoundation.org/UA/2008/02/Types.xsd}String'):
    if find.text.startswith('opc.tcp'):
        ip = find.text
        print(ip)
        # print(type(ip))
# ip주소

for var in root.findall('{http://opcfoundation.org/UA/2011/03/UANodeSet.xsd}UAVariable'):
    if "Historizing" in var.attrib:
        # print(var.findtext('{http://opcfoundation.org/UA/2011/03/UANodeSet.xsd}DisplayName'))
        varname.append(var.findtext('{http://opcfoundation.org/UA/2011/03/UANodeSet.xsd}DisplayName'))
print(varname)
# variable이름
