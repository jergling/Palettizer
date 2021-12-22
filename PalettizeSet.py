from matplotlib.pyplot import getp
from numpy.typing import _80Bit
from PaletteMaker import getPaletteMultiImage, recreate_image
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import os
from skimage import io
from sklearn.cluster import KMeans

corner_values = np.array([[255,255,255], [0,0,0], [0,255,255], [255,0,255], [255,255,0], [0,0,255], [255,0,0], [0,255,0]] , dtype=np.uint8)

palette = np.ndarray(shape=(0,3), dtype=np.uint8)

bitdepth = 8
n_colors = 1 << bitdepth

imageroot = os.getcwd() + "\\trainingImages_night\\"

palette = getPaletteMultiImage(imageroot, bitdepth, n_colors*6)

fig = go.Figure()

limitPalette = np.append(palette.cluster_centers_, corner_values, axis=0)

for di in palette.cluster_centers_:
    colorstring = 'rgb(' + str(int(di[0])) + ',' + str(int(di[1])) + ',' + str(int(di[2])) + ')'
    fig.add_trace(
        go.Scatter3d(
            mode='markers',
            x=[di[0]],
            y=[di[1]],
            z=[di[2]],  
            marker=dict(
                color=colorstring,
                size = 4,
            ),
            showlegend = False
        )
    )

fig.show()

plt.figure(1)
plt.clf()
plt.axis("off")
plt.title(f"Palettized image ({n_colors} colors, Indexed)")
plt.imshow(recreate_image("\\targetImage_7.jpg", palette))
plt.show()