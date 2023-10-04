from glob import glob

import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import streamlit as st

import rasterio as rio
from rasterio.plot import plotting_extent
from rasterio.plot import show
from rasterio.plot import reshape_as_raster, reshape_as_image

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from rasterio.windows import Window

import plotly.graph_objects as go
import cv2
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error as mse
from skimage.metrics import normalized_root_mse as nmse
import math

np.seterr(divide='ignore', invalid='ignore')

def read_sen(a):
    S_sentinel_bands = glob(a)
    S_sentinel_bands.sort()
    print(S_sentinel_bands)
    l = []
    
    for i in S_sentinel_bands:
        with rio.open(i, 'r') as f:
            l.append(f.read(1, window = Window(0, 0, 1800, 1800)))
            
    return l

def read_land(a):
    S_sentinel_bands = glob(a)
    S_sentinel_bands.sort()
    print(S_sentinel_bands)
    l = []
    for i in S_sentinel_bands:
        with rio.open(i, 'r') as f:
            l.append(f.read(1))
            
    return l

def veg_classification(ndvi1):
    # Create classes and apply to NDVI results
    ndvi_class_bins = [-1, 0, 0.1, 0.25, 0.4, 1]
    ndvi_landsat_class = np.digitize(ndvi1, ndvi_class_bins)

    # Apply the nodata mask to the newly classified NDVI data
    ndvi_landsat_class = np.ma.masked_where(
        np.ma.getmask(ndvi1), ndvi_landsat_class
    )
    # Define color map
    nbr_colors = ["gray", "y", "yellowgreen", "g", "darkgreen"]
    nbr_cmap = ListedColormap(nbr_colors)

    # Define class names
    ndvi_cat_names = [
        "No Vegetation",
        "Bare Area",
        "Low Vegetation",
        "Moderate Vegetation",
        "High Vegetation",
    ]

    # Get list of classes
    classes,m  = np.unique(ndvi_landsat_class,return_counts=True)
    classes = classes.tolist()
    # The mask returns a value of none in the classes. remove that
    classes = classes[0:5]

    # Plot your data
    fig, ax = plt.subplots(figsize=(12, 12))
    im = ax.imshow(ndvi_landsat_class, cmap=nbr_cmap)

    ep.draw_legend(im_ax=im, classes=classes, titles=ndvi_cat_names)
    ax.set_title(
        "Vegetation Classes",
        fontsize=14,
    )
    ax.set_axis_off()

    # Auto adjust subplot to fit figure size
    plt.tight_layout()
    st.pyplot()
    return m

def basic_classification(ndvi1):
    # Create classes and apply to NDVI results
    #ndvi_class_bins = [-1, 0, 0.1, 0.25, 0.4, 1]
    ndvi_class_bins = [-1, 0, 0.2, 1]
    ndvi_landsat_class = np.digitize(ndvi1, ndvi_class_bins)

    # Apply the nodata mask to the newly classified NDVI data
    ndvi_landsat_class = np.ma.masked_where(
        np.ma.getmask(ndvi1), ndvi_landsat_class
    )
    print(np.unique(ndvi_landsat_class))


    # Define color map
    #nbr_colors = [ "y", "yellowgreen", "g", "darkgreen","blue"]
    nbr_colors = [ "y","g","blue"]
    nbr_cmap = ListedColormap(nbr_colors)

    # Define class names
    ndvi_cat_names = [
        "Concrete",
        "green",
        "water"
        
    ]

    # Get list of classes
    classes, m = np.unique(ndvi_landsat_class,return_counts=True)
    print(classes)
    print(m)
    classes = classes.tolist()
    # The mask returns a value of none in the classes. remove that
    classes = classes[0:3]
    
    return m

def all_classifications(ndvi1):
    # Create classes and apply to NDVI results
    #ndvi_class_bins = [-1, 0, 0.1, 0.25, 0.4, 1]
    ndvi_class_bins = [-1, 0, 0.03,0.3, 0.5, 1]
    ndvi_landsat_class = np.digitize(ndvi1, ndvi_class_bins)

    # Apply the nodata mask to the newly classified NDVI data
    ndvi_landsat_class = np.ma.masked_where(
        np.ma.getmask(ndvi1), ndvi_landsat_class
    )
    print(np.unique(ndvi_landsat_class))


    # Define color map
    #nbr_colors = [ "y", "yellowgreen", "g", "darkgreen","blue"]
    nbr_colors = ["y", "yellowgreen", "g", "darkgreen","blue"]
    nbr_cmap = ListedColormap(nbr_colors)

    # Define class names
    ndvi_cat_names = [
        "Bare soil",
        "Sparse vegetation",
        "Moderate Vegitation",
        "Dence Vegetation",
        "Water"
        
    ]

    # Get list of classes
    classes, m = np.unique(ndvi_landsat_class,return_counts=True)
    print(classes)
    print(m)
    classes = classes.tolist()
    # The mask returns a value of none in the classes. remove that
    classes = classes[0:5]

    # Plot your data
    fig, ax = plt.subplots(figsize=(12, 12))
    im = ax.imshow(ndvi_landsat_class, cmap=nbr_cmap)

    ep.draw_legend(im_ax=im, classes=classes, titles=ndvi_cat_names)
    ax.set_title(
        "All Classes",
        fontsize=14,
    )
    ax.set_axis_off()

    # Auto adjust subplot to fit figure size
    plt.tight_layout()
    st.pyplot()
    return m





def b_classification(ndvi1,m):
    # Calculate forest and water masks based on the thresholds
    total_mask = ndvi1.size

    concrete_percentage     =(m[0]/total_mask) * 100
    green_percentage    	=(m[1]/ total_mask) * 100
    water_percentage        =(m[2] / total_mask) * 100

    print("sssss")
    print(f"Concrete Percentage:{concrete_percentage:.2f}%")
    print(f"Green Percentage: {green_percentage:.2f}%")
    print(f"Water Percentage: {water_percentage:.2f}%")
    print("sssss")

def v_classification(ndvi1,m):
    # Calculate forest and water masks based on the thresholds
    total_mask = ndvi1.size

    c1=(m[0]/total_mask) * 100
    c2=(m[1]/ total_mask) * 100
    c3=(m[2] / total_mask) * 100
    c4=(m[3] / total_mask) * 100
    c5=(m[4] / total_mask) * 100

    st.write(f"No Vegetatio Percentage:{c1:.2f}%")
    st.write(f"Bare Area Percentage: {c2:.2f}%")
    st.write(f"Low Vegetation Percentage: {c3:.2f}%")
    st.write(f"Moderate Vegetation Percentage: {c4:.2f}%")
    st.write(f"High Vegetation Percentage: {c5:.2f}%")


def all_classification(ndvi1,m):
    # Calculate forest and water masks based on the thresholds
    total_mask = ndvi1.size
    c1  =(m[0]/total_mask) * 100
    c2  =(m[1]/ total_mask) * 100
    c3  =(m[2] / total_mask) * 100
    c4  =(m[3] / total_mask) * 100
    c5  =(m[4] / total_mask) * 100
    st.write(f"Bare Soil Percentage: {c1:.2f}%")
    st.write(f"Sparse Vegetation Percentage: {c2:.2f}%")
    st.write(f"Moderate Vegetation Percentage: {c3:.2f}%")
    st.write(f"Dence Vegetation Percentage: {c4:.2f}%")
    st.write(f"Water Percentage: {c5:.2f}%")

def accuracy_s(s1,s2):
    arr_st1 = np.stack(read_sen(s1))
    arr_st2 = np.stack(read_sen(s2))
    st.header("Peak Signal-to-Noise Ratio (PSNR)")
    for i in range(0,len(arr_st1)-1):
        st.caption("Noise Data 1 -Data 2")
        st.write("Noise Band "+str(i)+": "+str(cv2.PSNR(arr_st1[i],arr_st2[i]))+"%")
        st.caption("Noise Data 2 -Data 1")
        st.write("Noise Band "+str(i)+": "+str(cv2.PSNR(arr_st2[i],arr_st1[i]))+"%")

    st.divider()
    st.header("Structural Similarity Index Measure (SSIM)") 
    for i in range(0,len(arr_st1)-1):    
        st.caption("SSIM Data 1 -Data 2")
        st.write("SSIM Band "+str(i)+": "+str(ssim(arr_st1[i],arr_st2[i]))+"%")
        st.caption("SSIM Data 2 -Data 1")
        st.write("SSIM Band "+str(i)+": "+str(ssim(arr_st2[i],arr_st1[i]))+"%")
    
    st.divider()
    st.header("Root mean square error (RMSE)") 
    for i in range(0,len(arr_st1)-1):    
        st.caption("RMSE Data 1 -Data 2")
        st.write("RMSE Band "+str(i)+": "+str(math.sqrt(mse(arr_st1[i],arr_st2[i])))+"%")
        st.caption("RMSE Data 2 -Data 1")
        st.write("RMSE Band "+str(i)+": "+str(math.sqrt(mse(arr_st2[i],arr_st1[i])))+"%")

    st.divider()
    st.header("Mean square error (MSE)") 
    for i in range(0,len(arr_st1)-1):    
        st.caption("MSE Data 1 -Data 2")
        st.write("MSE Band "+str(i)+": "+str(mse(arr_st1[i],arr_st2[i]))+"%")
        st.caption("MSE Data 2 -Data 1")
        st.write("MSE Band "+str(i)+": "+str(mse(arr_st2[i],arr_st1[i]))+"%")

    st.divider()
    st.header("Normalized  mean square error (NMSE)") 
    for i in range(0,len(arr_st1)-1):    
        st.caption("NMSE Data 1 -Data 2")
        st.write("NMSE Band "+str(i)+": "+str(nmse(arr_st1[i],arr_st2[i]))+"%")
        st.caption("NMSE Data 2 -Data 1")
        st.write("NMSE Band "+str(i)+": "+str(nmse(arr_st2[i],arr_st1[i]))+"%")

def accuracy_l(s1,s2):
    arr_st1 = np.stack(read_land(s1))
    arr_st2 = np.stack(read_land(s2))
    st.header("Peak Signal-to-Noise Ratio (PSNR)")
    for i in range(0,len(arr_st1)-1):
        st.caption("Noise Data 1 -Data 2")
        st.write("Noise Band "+str(i)+": "+str(cv2.PSNR(arr_st1[i],arr_st2[i]))+"%")
        st.caption("Noise Data 2 -Data 1")
        st.write("Noise Band "+str(i)+": "+str(cv2.PSNR(arr_st2[i],arr_st1[i]))+"%")

    st.divider()
    st.header("Structural Similarity Index Measure (SSIM)") 
    for i in range(0,len(arr_st1)-1):    
        st.caption("SSIM Data 1 -Data 2")
        st.write("SSIM Band "+str(i)+": "+str(ssim(arr_st1[i],arr_st2[i]))+"%")
        st.caption("SSIM Data 2 -Data 1")
        st.write("SSIM Band "+str(i)+": "+str(ssim(arr_st2[i],arr_st1[i]))+"%")
    
    st.divider()
    st.header("Root mean square error (RMSE)") 
    for i in range(0,len(arr_st1)-1):    
        st.caption("RMSE Data 1 -Data 2")
        st.write("RMSE Band "+str(i)+": "+str(math.sqrt(mse(arr_st1[i],arr_st2[i])))+"%")
        st.caption("RMSE Data 2 -Data 1")
        st.write("RMSE Band "+str(i)+": "+str(math.sqrt(mse(arr_st2[i],arr_st1[i])))+"%")

    st.divider()
    st.header("Mean square error (MSE)") 
    for i in range(0,len(arr_st1)-1):    
        st.caption("MSE Data 1 -Data 2")
        st.write("MSE Band "+str(i)+": "+str(mse(arr_st1[i],arr_st2[i]))+"%")
        st.caption("MSE Data 2 -Data 1")
        st.write("MSE Band "+str(i)+": "+str(mse(arr_st2[i],arr_st1[i]))+"%")

    st.divider()
    st.header("Normalized  mean square error (NMSE)") 
    for i in range(0,len(arr_st1)-1):    
        st.caption("NMSE Data 1 -Data 2")
        st.write("NMSE Band "+str(i)+": "+str(nmse(arr_st1[i],arr_st2[i]))+"%")
        st.caption("NMSE Data 2 -Data 1")
        st.write("NMSE Band "+str(i)+": "+str(nmse(arr_st2[i],arr_st1[i]))+"%")