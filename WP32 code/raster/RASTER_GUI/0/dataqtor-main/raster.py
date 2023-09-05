from glob import glob

import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep

import rasterio as rio
from rasterio.plot import plotting_extent
from rasterio.plot import show
from rasterio.plot import reshape_as_raster, reshape_as_image

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from rasterio.windows import Window

import plotly.graph_objects as go

np.seterr(divide='ignore', invalid='ignore')

def read(a):
    S_sentinel_bands = glob(a)
    S_sentinel_bands.sort()
    print(S_sentinel_bands)
    l = []
    for i in S_sentinel_bands:
        with rio.open(i, 'r') as f:
            l.append(f.read(1, window = Window(0, 0, 1800, 1800)))
            
    return l