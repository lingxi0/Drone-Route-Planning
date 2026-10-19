import numpy as np
import pandas as pd
from pyproj import Transformer  # 坐标转换核心类


if __name__ == "__main__":
    tmep = False
    if tmep:
        wgs84_to_cgcs2000_3_40 = Transformer.from_crs("epsg:4326", 'epsg:4528', always_xy=True)
        # longitude经度, latitude

        data = pd.read_csv('./res/coord_wgs84.csv', header=0, index_col=0)
        trans_point = wgs84_to_cgcs2000_3_40.transform(data.iloc[:, 0], data.iloc[:, 1])
        trans_point = np.array(trans_point).T

        trans_point_cood = pd.DataFrame(trans_point)
        trans_point_cood.to_csv('./res/coord_cgcs.csv')
    else:
        cgcs2000_3_40_to_wgs84 = Transformer.from_crs("epsg:4528", 'epsg:4326', always_xy=True)

        data = pd.read_csv('res/interpolate_cgcs.csv', header=0, index_col=0)
        trans_point_orthophoto = cgcs2000_3_40_to_wgs84.transform(data.iloc[:, 0], data.iloc[:, 1])
        trans_point_orthophoto = pd.DataFrame(trans_point_orthophoto).T

        trans_point_oblique = cgcs2000_3_40_to_wgs84.transform(data.iloc[:, 2], data.iloc[:, 3])
        trans_point_oblique = pd.DataFrame(trans_point_oblique).T

        trans_point_cood = pd.concat([trans_point_orthophoto, trans_point_oblique], axis=1, ignore_index=True)
        trans_point_cood.to_csv('./res/interpolate_wgs84.csv')
