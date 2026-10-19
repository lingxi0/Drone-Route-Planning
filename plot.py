import matplotlib.pyplot as plt
import pandas as pd

coord = pd.read_csv('./res/interpolate_cgcs.csv', header=0, index_col=0)
att = pd.read_csv('./res/attribute.csv', header=0, index_col=0)

height = att.loc['height', 'value']

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(coord.iloc[:, 0], coord.iloc[:, 1], height, marker='o')
ax.plot(coord.iloc[:, 2], coord.iloc[:, 3], height, marker='o')

plt.axis('equal')
plt.grid()
plt.tight_layout()
plt.show()
