import xml.etree.ElementTree as ET
from xml.dom import minidom
import time

# dji kml 命名空间
kml_ns = "http://www.opengis.net/kml/2.2"
wpml_ns = "http://www.dji.com/wpmz/1.0.2"

ET.register_namespace("", kml_ns)
ET.register_namespace("wpml", wpml_ns)

speed = 10.0
now = str(int(time.time() * 1000))

kml = ET.Element(f"{{{kml_ns}}}kml")
doc = ET.SubElement(kml, "Document")
ET.SubElement(doc, f"{{{wpml_ns}}}author").text = "lx"
ET.SubElement(doc, f"{{{wpml_ns}}}createTime").text = now
ET.SubElement(doc, f"{{{wpml_ns}}}updateTime").text = now

# dji 固定配置部分
mission_config = ET.SubElement(doc, f"{{{wpml_ns}}}missionConfig")
ET.SubElement(mission_config, f"{{{wpml_ns}}}flyToWaylineMode").text = "safely"
ET.SubElement(mission_config, f"{{{wpml_ns}}}finishAction").text = "goHome"
ET.SubElement(mission_config, f"{{{wpml_ns}}}exitOnRCLost").text = "executeLostAction"
ET.SubElement(mission_config, f"{{{wpml_ns}}}executeRCLostAction").text = "goBack"
ET.SubElement(mission_config, f"{{{wpml_ns}}}globalTransitionalSpeed").text = str(speed)
# dji 机型配置部分
droneInfo = ET.SubElement(mission_config, f"{{{wpml_ns}}}droneInfo")
ET.SubElement(droneInfo, f"{{{wpml_ns}}}droneEnumValue").text = "68"
ET.SubElement(droneInfo, f"{{{wpml_ns}}}droneSubEnumValue").text = "0"

# ======= 写入文件 =======
xml_str = ET.tostring(kml, encoding='utf-8')
parsed = minidom.parseString(xml_str)
with open("wpmz/template.kml", "wb") as f:
    f.write(parsed.toprettyxml(indent="    ", encoding="UTF-8"))
