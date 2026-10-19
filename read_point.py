import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import pandas as pd
from math import ceil

tree = ET.parse('res/waylines.wpml')
root = tree.getroot()

# for elem in root.iter():
#     print(elem.tag)

coords_list = []

namespace = {'wpml': 'http://www.dji.com/wpmz/1.0.6', 'kml': 'http://www.opengis.net/kml/2.2'}

for coord in root.findall(".//kml:Placemark//kml:coordinates", namespace):
    raw = coord.text.strip()
    parts = raw.split(',')
    lon = float(parts[0])
    lat = float(parts[1])

    coords_list.append((lon, lat))

coord = pd.DataFrame(coords_list)
coord.to_csv('./res/coord_wgs84.csv')

plt.plot(coord.iloc[:, 0], coord.iloc[:, 1], marker='o')
plt.axis('equal')
plt.grid()
plt.show()

get_height = float(root.findall(".//kml:Placemark//wpml:executeHeight", namespace)[0].text)
get_speed = float(root.findall(".//wpml:autoFlightSpeed", namespace)[0].text)
get_dis = float(root.findall(".//wpml:actionTriggerParam", namespace)[0].text)
get_dis = ceil(get_dis)
print(get_dis)
get_distance = max([get_dis, 42])
# 最小给44m吧，大概5.5s一个点，太快了存储反应不过来导致拍照本身进堆栈，拍不全

data = {'name': ['height', 'speed', 'distance', 'dis'], 'value': [get_height, get_speed, get_distance, get_dis]}
data = pd.DataFrame(data)
data.to_csv('./res/attribute.csv', index=False)

print(coords_list)
print(len(coords_list))
