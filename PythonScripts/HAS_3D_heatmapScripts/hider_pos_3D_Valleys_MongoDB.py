import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://<USERNAME>:<PASSWORD>@hideandseekdata.nkcn2sb.mongodb.net/?retryWrites=true&w=majority')
db = cluster['HAS-Data']
valleysCollection = db['HAS-Valleys']

hider_Valleys_x = []
hider_Valleys_y = []

#Valleys
for document in valleysCollection.find():
    hider_Valleys_x.append(document['xHider'])
    hider_Valleys_y.append(document['yHider'])

skipped_hider_Valleys_x = [x[20:] for x in hider_Valleys_x]
skipped_hider_Valleys_y = [y[20:] for y in hider_Valleys_y]

# combine separated csv into one giant list for x and y
combine_x = [item for sublist in skipped_hider_Valleys_x for item in sublist]
combine_y = [item for sublist in skipped_hider_Valleys_y for item in sublist]


def rotate_data(x, y, angle_degrees):
    theta = np.radians(angle_degrees)
    x_rot = x * np.cos(theta) - y * np.sin(theta)
    y_rot = x * np.sin(theta) + y * np.cos(theta)
    return -x_rot, y_rot

def rotate_point(x, y, angle_degrees):
    theta = np.radians(angle_degrees)
    x_rot = x * np.cos(theta) - y * np.sin(theta)
    y_rot = x * np.sin(theta) + y * np.cos(theta)
    return -x_rot, y_rot

# point rotation to compensate for UE5 map rotation
angle_degrees = 0
rotated_x, rotated_y = rotate_data(np.array(combine_x), np.array(combine_y), angle_degrees)

# bins
x_bins = np.linspace(min(rotated_x), max(rotated_x), 50)
y_bins = np.linspace(min(rotated_y), max(rotated_y), 50)

# histogram
heatmap_data, xedges, yedges = np.histogram2d(rotated_x, rotated_y, bins=[x_bins, y_bins])
xpos, ypos = np.meshgrid(xedges[:-1] + np.diff(xedges)/2, yedges[:-1] + np.diff(yedges)/2, indexing="ij")

cdict = {
    'red':   ((0.0, 0.0, 0.0),
              (0.25, 0.0, 0.0),
              (0.5, 1.0, 1.0),
              (1.0, 1.0, 1.0)),
    'green': ((0.0, 0.0, 0.0),
              (0.25, 1.0, 1.0),
              (0.75, 1.0, 1.0),
              (1.0, 0.0, 0.0)),
    'blue':  ((0.0, 1.0, 1.0),
              (0.5, 0.0, 0.0),
              (1.0, 0.0, 0.0))
}
custom_cmap = LinearSegmentedColormap('custom_cmap', cdict)

z_min = 0
z_max = np.max(heatmap_data) * 0.5

fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(xpos.reshape(heatmap_data.shape), ypos.reshape(heatmap_data.shape),
                       heatmap_data, cmap=custom_cmap, linewidth=0, antialiased=False, alpha=0.75)

ax.set_zlim(z_min, z_max)

norm = plt.Normalize(heatmap_data.min(), heatmap_data.max())
cbar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=custom_cmap), ax=ax, shrink=0.5, aspect=5)
ticks = [cbar.norm.vmin, cbar.norm.vmax]
cbar.set_ticks(ticks)
cbar.set_ticklabels(['Low', 'High'])
cbar.set_label('Intensity of Positions')

info_text = "Note: Higher elevation indicates more frequent travel."
fig.text(0.15, 0.02, info_text, ha='left', va='center', fontsize=12, 
         bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white', alpha=0.8))

# node numbers labelled on heatmap for better visualization
label_z_pos = 0
letter_color = 'black'
box_color = 'white'
alpha_num = 1
font_size = 10
padding = 2

nodes = {
    1: (10610, 8820),
    2: (7240, 4950),
    3: (5690, -80),
    4: (9920, -6860),
    5: (4320, -11820),
    6: (-3650.0, -11050.0),
    7: (3090.0, -5820.0),
    8: (1050.0, -10.0),
    9: (-4420.0, -5890.0),
    10: (-9810.0, -9130.0),
    11: (-10860.0, 1120.0),
    12: (-7270.0, 3570.0),
    13: (-6340.0, -880.0),
    14: (-10660.0, 10730.0),
    15: (690.0, 9580.0),
}

for num, coords in nodes.items():
    rotated_point = rotate_point(coords[0], coords[1], angle_degrees)
    ax.text(rotated_point[0], rotated_point[1], label_z_pos, str(num), color=letter_color, 
            ha='center', va='center', fontsize=font_size, 
            bbox=dict(facecolor=box_color, alpha=alpha_num, pad=padding), zorder=10)

ax.set_title('3D Heatmap of Hider Player\n Map: Valleys')
ax.set_xlabel('X Coordinates')
ax.set_ylabel('Y Coordinates')
ax.set_zlabel('Intensity (positions per second)')

plt.show()