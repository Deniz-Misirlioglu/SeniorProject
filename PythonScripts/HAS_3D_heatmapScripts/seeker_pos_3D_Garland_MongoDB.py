import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from pymongo import MongoClient

cluster = MongoClient('mongodb+srv://<USERNAME>:<PASSWORD>@hideandseekdata.nkcn2sb.mongodb.net/?retryWrites=true&w=majority')
db = cluster['HAS-Data']
garlandCollection = db['HAS-Garland']

seeker_Garland_x = []
seeker_Garland_y = []

#Garland
for document in garlandCollection.find():
    seeker_Garland_x.append(document['xSeeker'])
    seeker_Garland_y.append(document['ySeeker'])
    
skipped_seeker_Garland_x = [x[52:] for x in seeker_Garland_x]
skipped_seeker_Garland_y = [y[52:] for y in seeker_Garland_y]

# combine separated csv into one giant list for x and y
combine_x = [item for sublist in skipped_seeker_Garland_x for item in sublist]
combine_y = [item for sublist in skipped_seeker_Garland_y for item in sublist]
    
def rotate_point(x, y, angle_degrees):
    theta = np.radians(angle_degrees)
    x_rot = x * np.cos(theta) - y * np.sin(theta)
    y_rot = -(x * np.sin(theta) + y * np.cos(theta))
    return x_rot, y_rot


def rotate_data(x, y, angle_degrees):
    theta = np.radians(angle_degrees)
    x_rot = x * np.cos(theta) - y * np.sin(theta)
    y_rot = -(x * np.sin(theta) + y * np.cos(theta))
    return x_rot, y_rot

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
z_max = np.max(heatmap_data) * 1

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

label_z_pos = 0
letter_color = 'black'
box_color = 'white'
alpha_num = 1
font_size = 8
padding = 1.2

nodes = {
    1: (-11396, 7443),
    2: (-7596, 11683),
    3: (-4236, 11663),
    4: (-1276, 11712),
    5: (1734, 11842),
    6: (5284, 5842),
    7: (484, 4982),
    8: (-3006, 1022),
    9: (-8976, -438),
    10: (-3006, -3048),
    11: (-8096, -3968),
    12: (-7216, -7358),
    13: (-6106, -7288),
    14: (-5016, -7248),
    15: (-4016, -7168),
    16: (-3026, -7148),
    17: (-1956, -7068),
    18: (-8616, -8998),
    19: (-8616, -10438),
    20: (1044, -7168),
    21: (2354, -7018),
    22: (3814, -6798),
    23: (5194, -6578),
    24: (1804, -8878),
    25: (3444, -10428),
    26: (5094, -14148),
    27: (6924, -15228),
    28: (-886, -13898),
    29: (244, -13758),
    30: (1444, -13618),
    31: (-4666, -11748),
    32: (-3576, -15708),
    33: (-2436, -17528),
    34: (-7006, -14858),
    35: (-7196, -17968),
    36: (-6806, -20838),
    37: (-10706, -15688),
}

for num, coords in nodes.items():
    rotated_point = rotate_point(coords[0], coords[1], angle_degrees)
    ax.text(rotated_point[0], rotated_point[1], label_z_pos, str(num), color=letter_color, 
            ha='center', va='center', fontsize=font_size, 
            bbox=dict(facecolor=box_color, alpha=alpha_num, pad=padding), zorder=10)

ax.set_title('3D Heatmap of Seeker Player\n Map: Garland')
ax.set_xlabel('X Coordinates')
ax.set_ylabel('Y Coordinates')
ax.set_zlabel('Intensity (positions per second)')

plt.show()
