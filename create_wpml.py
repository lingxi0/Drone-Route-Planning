import xml.etree.ElementTree as ET
from xml.dom import minidom
import pandas as pd

# dji kml 命名空间
kml_ns = "http://www.opengis.net/kml/2.2"
wpml_ns = "http://www.dji.com/wpmz/1.0.2"

ET.register_namespace("", kml_ns)
ET.register_namespace("wpml", wpml_ns)

cood = pd.read_csv('res/interpolate_wgs84.csv', header=0, index_col=0)
orthophoto = cood.iloc[:, 0:2]
oblique = cood.iloc[:, 2:].dropna()

att = pd.read_csv('./res/attribute.csv', index_col=0)
height = att.loc['height', 'value']
speed = att.loc['speed', 'value']

kml = ET.Element(f"{{{kml_ns}}}kml")
doc = ET.SubElement(kml, f"{{{kml_ns}}}Document")

# dji 固定配置部分
mission_config = ET.SubElement(doc, f"{{{wpml_ns}}}missionConfig")
ET.SubElement(mission_config, f"{{{wpml_ns}}}flyToWaylineMode").text = "safely"
ET.SubElement(mission_config, f"{{{wpml_ns}}}finishAction").text = "goHome"
ET.SubElement(mission_config, f"{{{wpml_ns}}}exitOnRCLost").text = "executeLostAction"
ET.SubElement(mission_config, f"{{{wpml_ns}}}executeRCLostAction").text = "goBack"
ET.SubElement(mission_config, f"{{{wpml_ns}}}takeOffSecurityHeight").text = str(height)
ET.SubElement(mission_config, f"{{{wpml_ns}}}globalTransitionalSpeed").text = str(speed)
# dji 机型配置部分
droneInfo = ET.SubElement(mission_config, f"{{{wpml_ns}}}droneInfo")
ET.SubElement(droneInfo, f"{{{wpml_ns}}}droneEnumValue").text = "68"
ET.SubElement(droneInfo, f"{{{wpml_ns}}}droneSubEnumValue").text = "0"
# dji 负载配置部分
payloadInfo = ET.SubElement(mission_config, f"{{{wpml_ns}}}payloadInfo")
payloadEnumValue = ET.SubElement(payloadInfo, f"{{{wpml_ns}}}payloadEnumValue")
payloadEnumValue.text = ""
ET.SubElement(payloadInfo, f"{{{wpml_ns}}}payloadSubEnumValue").text = "0"
ET.SubElement(payloadInfo, f"{{{wpml_ns}}}payloadPositionIndex").text = "0"

# folder
folder = ET.SubElement(doc, f"{{{kml_ns}}}Folder")
ET.SubElement(folder, f"{{{wpml_ns}}}templateId").text = "0"
ET.SubElement(folder, f"{{{wpml_ns}}}waylineId").text = "0"
ET.SubElement(folder, f"{{{wpml_ns}}}autoFlightSpeed").text = str(speed)
ET.SubElement(folder, f"{{{wpml_ns}}}executeHeightMode").text = "relativeToStartPoint"
payloadParam = ET.SubElement(folder, f"{{{wpml_ns}}}payloadParam")
ET.SubElement(payloadParam, f"{{{wpml_ns}}}payloadPositionIndex").text = "0"
ET.SubElement(payloadParam, f"{{{wpml_ns}}}imageFormat").text = "wide"

n_point = orthophoto.shape[0]
# 添加航点
for n in range(0, n_point):
    placemark = ET.SubElement(folder, "Placemark")
    # 航点坐标
    point = ET.SubElement(placemark, "Point")
    ET.SubElement(point, "coordinates").text = str(orthophoto.iloc[n, 0]) + ',' + str(orthophoto.iloc[n, 1])
    ET.SubElement(placemark, f"{{{wpml_ns}}}index").text = str(n)
    ET.SubElement(placemark, f"{{{wpml_ns}}}executeHeight").text = str(height)
    ET.SubElement(placemark, f"{{{wpml_ns}}}waypointSpeed").text = str(speed)
    # 航向
    waypointHeadingParam = ET.SubElement(placemark, f"{{{wpml_ns}}}waypointHeadingParam")
    ET.SubElement(waypointHeadingParam, f"{{{wpml_ns}}}waypointHeadingMode").text = "followWayline"
    ET.SubElement(waypointHeadingParam, f"{{{wpml_ns}}}waypointHeadingAngle").text = "0"
    ET.SubElement(waypointHeadingParam, f"{{{wpml_ns}}}waypointHeadingPathMode").text = "followBadArc"
    # 转弯
    waypointTurnParam = ET.SubElement(placemark, f"{{{wpml_ns}}}waypointTurnParam")
    ET.SubElement(waypointTurnParam, f"{{{wpml_ns}}}waypointTurnMode").text = \
        "toPointAndStopWithDiscontinuityCurvature"
    ET.SubElement(waypointTurnParam, f"{{{wpml_ns}}}waypointTurnDampingDist").text = "1"

    ET.SubElement(placemark, f"{{{wpml_ns}}}useStraightLine").text = "0"
    if n == 0:
        actionGroup0 = ET.SubElement(placemark, f"{{{wpml_ns}}}actionGroup")
        ET.SubElement(actionGroup0, f"{{{wpml_ns}}}actionGroupId").text = "0"
        ET.SubElement(actionGroup0, f"{{{wpml_ns}}}actionGroupStartIndex").text = "0"
        ET.SubElement(actionGroup0, f"{{{wpml_ns}}}actionGroupEndIndex").text = "0"
        ET.SubElement(actionGroup0, f"{{{wpml_ns}}}actionGroupMode").text = "sequence"
        # 触发器
        actionTrigger = ET.SubElement(actionGroup0, f"{{{wpml_ns}}}actionTrigger")
        ET.SubElement(actionTrigger, f"{{{wpml_ns}}}actionTriggerType").text = "reachPoint"
        # 动作0
        action = ET.SubElement(actionGroup0, f"{{{wpml_ns}}}action")
        ET.SubElement(action, f"{{{wpml_ns}}}actionId").text = "0"
        ET.SubElement(action, f"{{{wpml_ns}}}actionActuatorFunc").text = "gimbalRotate"
        actionActuatorFuncParam = ET.SubElement(action, f"{{{wpml_ns}}}actionActuatorFuncParam")
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}payloadPositionIndex").text = "0"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalHeadingYawBase").text = "aircraft"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalRotateMode").text = "absoluteAngle"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalPitchRotateEnable").text = "1"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalPitchRotateAngle").text = "-90"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalRollRotateEnable").text = "0"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalRollRotateAngle").text = "0"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalYawRotateEnable").text = "0"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalYawRotateAngle").text = "0"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalRotateTimeEnable").text = "0"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalRotateTime").text = "0"
        # 动作1
        action = ET.SubElement(actionGroup0, f"{{{wpml_ns}}}action")
        ET.SubElement(action, f"{{{wpml_ns}}}actionId").text = "1"
        ET.SubElement(action, f"{{{wpml_ns}}}actionActuatorFunc").text = "hover"
        actionActuatorFuncParam = ET.SubElement(action, f"{{{wpml_ns}}}actionActuatorFuncParam")
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}hoverTime").text = "1"
        # 动作2
        action = ET.SubElement(actionGroup0, f"{{{wpml_ns}}}action")
        ET.SubElement(action, f"{{{wpml_ns}}}actionId").text = "2"
        ET.SubElement(action, f"{{{wpml_ns}}}actionActuatorFunc").text = "takePhoto"
        actionActuatorFuncParam = ET.SubElement(action, f"{{{wpml_ns}}}actionActuatorFuncParam")
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}payloadPositionIndex").text = "0"
    elif n > 0:
        actionGroup0 = ET.SubElement(placemark, f"{{{wpml_ns}}}actionGroup")
        ET.SubElement(actionGroup0, f"{{{wpml_ns}}}actionGroupId").text = str(n)
        ET.SubElement(actionGroup0, f"{{{wpml_ns}}}actionGroupStartIndex").text = str(n)
        ET.SubElement(actionGroup0, f"{{{wpml_ns}}}actionGroupEndIndex").text = str(n)
        ET.SubElement(actionGroup0, f"{{{wpml_ns}}}actionGroupMode").text = "sequence"
        # 触发器
        actionTrigger = ET.SubElement(actionGroup0, f"{{{wpml_ns}}}actionTrigger")
        ET.SubElement(actionTrigger, f"{{{wpml_ns}}}actionTriggerType").text = "reachPoint"
        # 动作0
        action = ET.SubElement(actionGroup0, f"{{{wpml_ns}}}action")
        ET.SubElement(action, f"{{{wpml_ns}}}actionId").text = "0"
        ET.SubElement(action, f"{{{wpml_ns}}}actionActuatorFunc").text = "takePhoto"
        actionActuatorFuncParam = ET.SubElement(action, f"{{{wpml_ns}}}actionActuatorFuncParam")
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}payloadPositionIndex").text = "0"
        # 动作1
        action = ET.SubElement(actionGroup0, f"{{{wpml_ns}}}action")
        ET.SubElement(action, f"{{{wpml_ns}}}actionId").text = "1"
        ET.SubElement(action, f"{{{wpml_ns}}}actionActuatorFunc").text = "gimbalRotate"
        actionActuatorFuncParam = ET.SubElement(action, f"{{{wpml_ns}}}actionActuatorFuncParam")
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}payloadPositionIndex").text = "0"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalHeadingYawBase").text = "aircraft"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalRotateMode").text = "absoluteAngle"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalPitchRotateEnable").text = "1"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalPitchRotateAngle").text = "-90"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalRollRotateEnable").text = "0"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalRollRotateAngle").text = "0"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalYawRotateEnable").text = "0"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalYawRotateAngle").text = "0"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalRotateTimeEnable").text = "0"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalRotateTime").text = "0"

n_point_1 = oblique.shape[0]
# 添加航点
for p in range(0, n_point_1):
    placemark = ET.SubElement(folder, "Placemark")
    # 航点坐标
    point = ET.SubElement(placemark, "Point")
    ET.SubElement(point, "coordinates").text = str(oblique.iloc[p, 0]) + ',' + str(oblique.iloc[p, 1])
    ET.SubElement(placemark, f"{{{wpml_ns}}}index").text = str(n + 1 + p)
    ET.SubElement(placemark, f"{{{wpml_ns}}}executeHeight").text = str(height)
    ET.SubElement(placemark, f"{{{wpml_ns}}}waypointSpeed").text = str(speed)
    # 航向
    waypointHeadingParam = ET.SubElement(placemark, f"{{{wpml_ns}}}waypointHeadingParam")
    ET.SubElement(waypointHeadingParam, f"{{{wpml_ns}}}waypointHeadingMode").text = "followWayline"
    ET.SubElement(waypointHeadingParam, f"{{{wpml_ns}}}waypointHeadingAngle").text = "0"
    ET.SubElement(waypointHeadingParam, f"{{{wpml_ns}}}waypointHeadingPathMode").text = "followBadArc"
    # 转弯
    waypointTurnParam = ET.SubElement(placemark, f"{{{wpml_ns}}}waypointTurnParam")
    ET.SubElement(waypointTurnParam, f"{{{wpml_ns}}}waypointTurnMode").text = \
        "toPointAndStopWithDiscontinuityCurvature"
    ET.SubElement(waypointTurnParam, f"{{{wpml_ns}}}waypointTurnDampingDist").text = "1"

    ET.SubElement(placemark, f"{{{wpml_ns}}}useStraightLine").text = "0"
    if p == 0:
        actionGroup0 = ET.SubElement(placemark, f"{{{wpml_ns}}}actionGroup")
        ET.SubElement(actionGroup0, f"{{{wpml_ns}}}actionGroupId").text = str(n + 1)
        ET.SubElement(actionGroup0, f"{{{wpml_ns}}}actionGroupStartIndex").text = str(n + 1)
        ET.SubElement(actionGroup0, f"{{{wpml_ns}}}actionGroupEndIndex").text = str(n + 1)
        ET.SubElement(actionGroup0, f"{{{wpml_ns}}}actionGroupMode").text = "sequence"
        # 触发器
        actionTrigger = ET.SubElement(actionGroup0, f"{{{wpml_ns}}}actionTrigger")
        ET.SubElement(actionTrigger, f"{{{wpml_ns}}}actionTriggerType").text = "reachPoint"
        # 动作0
        action = ET.SubElement(actionGroup0, f"{{{wpml_ns}}}action")
        ET.SubElement(action, f"{{{wpml_ns}}}actionId").text = "0"
        ET.SubElement(action, f"{{{wpml_ns}}}actionActuatorFunc").text = "gimbalRotate"
        actionActuatorFuncParam = ET.SubElement(action, f"{{{wpml_ns}}}actionActuatorFuncParam")
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}payloadPositionIndex").text = "0"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalHeadingYawBase").text = "aircraft"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalRotateMode").text = "absoluteAngle"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalPitchRotateEnable").text = "1"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalPitchRotateAngle").text = "-45"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalRollRotateEnable").text = "0"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalRollRotateAngle").text = "0"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalYawRotateEnable").text = "0"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalYawRotateAngle").text = "0"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalRotateTimeEnable").text = "1"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalRotateTime").text = "2"
        # 动作1
        action = ET.SubElement(actionGroup0, f"{{{wpml_ns}}}action")
        ET.SubElement(action, f"{{{wpml_ns}}}actionId").text = "1"
        ET.SubElement(action, f"{{{wpml_ns}}}actionActuatorFunc").text = "hover"
        actionActuatorFuncParam = ET.SubElement(action, f"{{{wpml_ns}}}actionActuatorFuncParam")
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}hoverTime").text = "1"
        # 动作2
        action = ET.SubElement(actionGroup0, f"{{{wpml_ns}}}action")
        ET.SubElement(action, f"{{{wpml_ns}}}actionId").text = "2"
        ET.SubElement(action, f"{{{wpml_ns}}}actionActuatorFunc").text = "takePhoto"
        actionActuatorFuncParam = ET.SubElement(action, f"{{{wpml_ns}}}actionActuatorFuncParam")
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}payloadPositionIndex").text = "0"
    elif p > 0:
        actionGroup0 = ET.SubElement(placemark, f"{{{wpml_ns}}}actionGroup")
        ET.SubElement(actionGroup0, f"{{{wpml_ns}}}actionGroupId").text = str(n + 1 + p)
        ET.SubElement(actionGroup0, f"{{{wpml_ns}}}actionGroupStartIndex").text = str(n + 1 + p)
        ET.SubElement(actionGroup0, f"{{{wpml_ns}}}actionGroupEndIndex").text = str(n + 1 + p)
        ET.SubElement(actionGroup0, f"{{{wpml_ns}}}actionGroupMode").text = "sequence"
        # 触发器
        actionTrigger = ET.SubElement(actionGroup0, f"{{{wpml_ns}}}actionTrigger")
        ET.SubElement(actionTrigger, f"{{{wpml_ns}}}actionTriggerType").text = "reachPoint"
        # 动作0
        action = ET.SubElement(actionGroup0, f"{{{wpml_ns}}}action")
        ET.SubElement(action, f"{{{wpml_ns}}}actionId").text = "0"
        ET.SubElement(action, f"{{{wpml_ns}}}actionActuatorFunc").text = "takePhoto"
        actionActuatorFuncParam = ET.SubElement(action, f"{{{wpml_ns}}}actionActuatorFuncParam")
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}payloadPositionIndex").text = "0"
        # 动作1
        action = ET.SubElement(actionGroup0, f"{{{wpml_ns}}}action")
        ET.SubElement(action, f"{{{wpml_ns}}}actionId").text = "1"
        ET.SubElement(action, f"{{{wpml_ns}}}actionActuatorFunc").text = "gimbalRotate"
        actionActuatorFuncParam = ET.SubElement(action, f"{{{wpml_ns}}}actionActuatorFuncParam")
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}payloadPositionIndex").text = "0"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalHeadingYawBase").text = "aircraft"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalRotateMode").text = "absoluteAngle"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalPitchRotateEnable").text = "1"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalPitchRotateAngle").text = "-45"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalRollRotateEnable").text = "0"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalRollRotateAngle").text = "0"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalYawRotateEnable").text = "0"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalYawRotateAngle").text = "0"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalRotateTimeEnable").text = "1"
        ET.SubElement(actionActuatorFuncParam, f"{{{wpml_ns}}}gimbalRotateTime").text = "2"

# ======= 写入文件 =======
xml_str = ET.tostring(kml, encoding='utf-8')
parsed = minidom.parseString(xml_str)
with open("wpmz/waylines.wpml", "wb") as f:
    f.write(parsed.toprettyxml(indent="    ", encoding="UTF-8"))
