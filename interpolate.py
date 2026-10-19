import numpy as np
import pandas as pd
from shapely.geometry import LineString
import matplotlib.pyplot as plt


def determine_point(coord: np.array, oblique_on=False):
    # 划分距离间隔（单位米）
    att = pd.read_csv('./res/attribute.csv', index_col=0)
    if oblique_on:
        interval = att.loc['dis', 'value']
    else:
        interval = att.loc['distance', 'value']

    # 构建线
    line = LineString(coord)

    # 整条线长度
    total_length = line.length
    print("整条线长度:", total_length)

    # 按步长生成点
    result_points = []
    current_distance = 0

    while current_distance <= total_length:
        point = line.interpolate(current_distance)  # 获取对应位置坐标
        result_points.append((current_distance, (point.x, point.y)))
        current_distance += interval

    # 按需求：最后不足 interval 的不用插值，而直接使用原最后点
    # 若最后一个点不是终点，则补上终点
    last_point = tuple(coord[-1].tolist())
    if result_points[-1] != last_point:
        result_points.append((total_length, last_point))

    # # ---- 将折线原始点插入 ----
    # for pt in coord:
    #     projected_dist = line.project(Point(pt))  # 正确写法
    #     result_points.append((projected_dist, pt))

    # ---- 去重并排序 ----
    # 用字典按距离存储以避免重复(坐标作为key时需要tuple)
    unique_by_distance = {}

    for d, pt in result_points:
        unique_by_distance[round(d, 6)] = pt  # 四舍五入避免浮点误差

    # 排序
    sorted_point = sorted(unique_by_distance.items(), key=lambda x: x[0])
    # 获取所有点对起点的距离
    sorted_len = np.array([item[0] for item in sorted_point])
    # 转化为各个点之间的距离
    sorted_len_diff = np.diff(sorted_len, 1)
    # 获取两点之间不足指定长度的索引值
    index = np.where(sorted_len_diff <= 18)[0]
    # 去掉指定的点重新构成一个列表
    sorted_pop = [v for i, v in enumerate(sorted_point) if i not in index]
    # 获取新的长度列表
    sorted_pop_len = np.array([item[0] for item in sorted_pop])
    # 重新做差分
    sorted_pop_len_diff = np.diff(sorted_pop_len, 1)
    # 画出原始插值点和新的点之间两点之间距离的变化
    plt.plot(range(0, sorted_len_diff.shape[0]), sorted_len_diff)
    plt.plot(range(0, sorted_pop_len_diff.shape[0]), sorted_pop_len_diff)
    plt.show()

    sorted_point_cood = np.array([a[1] for a in sorted_point])
    point = np.array([a[1] for a in sorted_pop])
    print(point.shape)

    plt.plot(sorted_point_cood[:, 0], sorted_point_cood[:, 1], marker='o')
    plt.plot(point[:, 0], point[:, 1], marker='o')
    plt.axis('equal')
    plt.grid()
    plt.show()
    plt.close('all')

    point = pd.DataFrame(point)
    return point


# 已知点坐标（示例）
coords = pd.read_csv('./res/coord_cgcs.csv', header=0, index_col=0).values
orthophoto = determine_point(coords[0:-2, :])
oblique = determine_point(coords[-2:, :], oblique_on=True)

data = pd.concat([orthophoto, oblique], axis=1, ignore_index=True)
data.to_csv('./res/interpolate_cgcs.csv')
