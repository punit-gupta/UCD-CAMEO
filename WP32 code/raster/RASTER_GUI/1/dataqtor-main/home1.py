import pandas as pd

import streamlit as st
from glob import glob
from raster import * 
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep

from raster import *


st.set_page_config(page_title="CAMEO Raster Spatial Data Quality!", page_icon="🔍", layout="wide")

st.title("CAMEO Raster Spatial Data Quality!")

@st.cache_data
def reading_dataset():
    global dataset
    try:
        dataset = pd.read_excel(uploaded_file)
    except ValueError:
        dataset = pd.read_csv(uploaded_file)
    return dataset

@st.cache_data
def beforeSTable():
    global before
    before = pd.DataFrame(columns=["Column", "Null Records", "Out of Format Records", "Proper Format Records", "Column DQ Score(%)"])
    return before



hide_streamlit_style = """
            <style>
            footer {
	        visibility: hidden;
	            }
            footer:after {
	            content:'developed by CAMEO Team (UCD); 
	            visibility: visible;
	            display: block;
	            position: relative;
	            #background-color: red;
	            padding: 5px;
	            top: 2px;
                    }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


with st.sidebar.subheader('Upload your Data here..'):
    uploaded_file = st.sidebar.file_uploader("Please upload a file of type: xlsx, csv", type=["xlsx", "csv"])

if uploaded_file is True:
    st.write("")
    st.info('Awaiting for file to be uploaded.')
    st.write("")
    """
    **Get your data ready for use before you start working with it:**

    1. Upload your Excel/CSV file  
    """
else: 
    type = st.selectbox("Data Source", ["None","Sentinel-2 Bands", "Landsat-8 Bands","Sentinel-2 GeoTiff","Landasat-8 Tiff", "Sentinel Tiff"])
    task = st.selectbox("Menu", ["Data Profiler", "Spatial Data Quality", "Review Summary Report and Download Adjusted Data"])
    
    if (type=="Sentinel-2 Bands"):
        arr_st = np.stack(read("IMG_DATA/*B?*.jp2"))
        if (task == "Data Profiler"):
            ep.plot_bands(arr_st, cmap = 'gist_earth', figsize = (20, 12), cols = 6, cbar = False)
            st.header("Satelite Bands 1-13")
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()

            tab1, tab2, tab3, tab4, tab5 , tab6, tab7= st.tabs(["RGB","NDVI", "SAVI", "VARI","MNDWI","NDMI","Ferrous Minerals"])

            with tab1:
                #RGB image       
                ep.plot_rgb(arr_st,rgb=(3, 2, 1),stretch=True,str_clip=0.2,figsize=(10, 16),title="RGB Composite Image" )
                st.pyplot()

            with tab2:
                #Normalized Difference Vegetation Index (NDVI)
                st.header("Normalized Difference Vegetation Index (NDVI)")
                ndvi = es.normalized_diff(arr_st[7], arr_st[3])
                ep.plot_bands(ndvi, cmap="RdYlGn", cols=1, vmin=-1, vmax=1, figsize=(5 , 5))
                st.pyplot()

            with tab3:
                #Soil-Adjusted Vegetation Index (SAVI)
                st.header("Soil-Adjusted Vegetation Index (SAVI) ")
                L = 0.5
                savi = ((arr_st[7] - arr_st[3]) / (arr_st[7] + arr_st[3] + L)) * (1 + L)
                ep.plot_bands(savi, cmap="RdYlGn", cols=1, vmin=-1, vmax=1, figsize=(5, 5))
                st.pyplot()    

            with tab4:
                #Visible Atmospherically Resistant Index (VARI)
                st.header("Visible Atmospherically Resistant Index (VARI) ")
                vari = (arr_st[2] - arr_st[3])/ (arr_st[2] + arr_st[3] - arr_st[1])
                ep.plot_bands(vari, cmap="RdYlGn", cols=1, vmin=-1, vmax=1, figsize=(10, 14))
                st.pyplot()

            with tab5:
                #Modified Normalized Difference Water Index (MNDWI) 
                st.header("Modified Normalized Difference Water Index (MNDWI)  ")
                mndwi = es.normalized_diff(arr_st[2], arr_st[10])
                ep.plot_bands(mndwi, cmap="RdYlGn", cols=1, vmin=-1, vmax=1, figsize=(10, 14))
                st.pyplot()        

            with tab6:
                #Normalized Difference Moisture Index (NDMI) 
                st.header("Normalized Difference Moisture Index (NDMI) ")
                mndwi = es.normalized_diff(arr_st[7], arr_st[10])
                ep.plot_bands(mndwi, cmap="RdYlGn", cols=1, vmin=-1, vmax=1, figsize=(10, 14))
                st.pyplot()

            with tab7:
                #Ferrous Minerals
                st.header("Ferrous Minerals ")
                mndwi = np.divide(arr_st[10], arr_st[7])
                ep.plot_bands(mndwi, cmap="RdYlGn", cols=1, vmin=-1, vmax=1, figsize=(10, 14))
                st.pyplot()

        if (task == "Spatial Data Quality"):
            st.write("")
            tab1, tab2, tab3,tab4 = st.tabs(["Completeness", "Accuracy", "Classification", "Precison"])

            with tab1:
                st.header("Completeness")
                ndvi = es.normalized_diff(arr_st[7], arr_st[3])
                v1=np.array(ndvi[0])
                unique, frequency = np.unique(v1,return_counts = True)
                st.subheader("Percentage of No Data: "+ str(np.count_nonzero(np.isnan(v1))/len(v1)))


            with tab2:
                st.header("Accuracy")

            with tab3:
                st.header("Classification")
                ndvi1 = es.normalized_diff(arr_st[4], arr_st[3])
                # Create classes and apply to NDVI results
                #ndvi_class_bins = [-1, 0, 0.1, 0.25, 0.4, 1]
                ndvi_class_bins = [-1, 0,
                                    0, 0.4,
                                    0.4, 1]
                ndvi_landsat_class = np.digitize(ndvi1, ndvi_class_bins)

                # Apply the nodata mask to the newly classified NDVI data
                ndvi_landsat_class = np.ma.masked_where(
                    np.ma.getmask(ndvi1), ndvi_landsat_class
                )
                print(np.unique(ndvi_landsat_class))


                # Define color map
                #nbr_colors = [ "y", "yellowgreen", "g", "darkgreen","blue"]
                nbr_colors = [ "y","g","blue","yellowgreen"]
                nbr_cmap = ListedColormap(nbr_colors)

                # Define class names
                ndvi_cat_names = [
                    "soil",
                    "green",
                    "water",
                    "No data"
                ]

                # Get list of classes
                classes = np.unique(ndvi_landsat_class)
                classes = classes.tolist()
                # The mask returns a value of none in the classes. remove that
                classes = classes[0:5]

                # Plot your data
                fig, ax = plt.subplots(figsize=(12, 12))
                im = ax.imshow(ndvi_landsat_class, cmap=nbr_cmap)

                ep.draw_legend(im_ax=im, classes=classes, titles=ndvi_cat_names)
                ax.set_title(
                    "Normalized Difference Vegetation Index (NDVI) Classes",
                    fontsize=14,
                )
                ax.set_axis_off()

                # Auto adjust subplot to fit figure size
                plt.tight_layout()
                st.pyplot()
                
            with tab4:
                st.header("Precision")
                #precision=["Low","Medium","High"]
                #resolution=""
                if(type=="Sentinel-2 Bands"):
                    precision="Low"
                    resolution="10 Meters"
                if(type=="Landsat-8 Bands"):
                    precision="Medium"
                    resolution="30 Meters"   
                if(type=="MODIS Bands"):
                    precision="High"
                    resolution="1000 Meters"
                
                st.subheader("Precision: "+ precision)
                st.subheader("Resolution: "+ resolution)
        
    if (type=="Landsat-8 Bands"):
        if (task == "Data Profiler"):
            arr_st = np.stack(read("IMG_DATA1/*B?*.jp2"))
            ep.plot_bands(arr_st, cmap = 'gist_earth', figsize = (20, 12), cols = 6, cbar = False)
            st.header("Satelite Bands 1-13")
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()

            tab1, tab2, tab3, tab4, tab5 , tab6, tab7= st.tabs(["RGB","NDVI", "SAVI", "VARI","MNDWI","NDMI","Ferrous Minerals"])

            with tab1:
                #RGB image       
                ep.plot_rgb(arr_st,rgb=(3, 2, 1),stretch=True,str_clip=0.2,figsize=(10, 16),title="RGB Composite Image" )
                st.pyplot()

            with tab2:
                #Normalized Difference Vegetation Index (NDVI)
                st.header("Normalized Difference Vegetation Index (NDVI)")
                ndvi = es.normalized_diff(arr_st[4], arr_st[3])
                ep.plot_bands(ndvi, cmap="RdYlGn", cols=1, vmin=-1, vmax=1, figsize=(5 , 5))
                st.pyplot()

            with tab3:
                #Soil-Adjusted Vegetation Index (SAVI)
                st.header("Soil-Adjusted Vegetation Index (SAVI) ")
                L = 0.5
                savi = ((arr_st[7] - arr_st[3]) / (arr_st[7] + arr_st[3] + L)) * (1 + L)
                ep.plot_bands(savi, cmap="RdYlGn", cols=1, vmin=-1, vmax=1, figsize=(5, 5))
                st.pyplot()    

            with tab4:
                #Visible Atmospherically Resistant Index (VARI)
                st.header("Visible Atmospherically Resistant Index (VARI) ")
                vari = (arr_st[2] - arr_st[3])/ (arr_st[2] + arr_st[3] - arr_st[1])
                ep.plot_bands(vari, cmap="RdYlGn", cols=1, vmin=-1, vmax=1, figsize=(10, 14))
                st.pyplot()

            with tab5:
                #Modified Normalized Difference Water Index (MNDWI) 
                st.header("Modified Normalized Difference Water Index (MNDWI)  ")
                mndwi = es.normalized_diff(arr_st[2], arr_st[10])
                ep.plot_bands(mndwi, cmap="RdYlGn", cols=1, vmin=-1, vmax=1, figsize=(10, 14))
                st.pyplot()        

            with tab6:
                #Normalized Difference Moisture Index (NDMI) 
                st.header("Normalized Difference Moisture Index (NDMI) ")
                mndwi = es.normalized_diff(arr_st[7], arr_st[10])
                ep.plot_bands(mndwi, cmap="RdYlGn", cols=1, vmin=-1, vmax=1, figsize=(10, 14))
                st.pyplot()

            with tab7:
                #Ferrous Minerals
                st.header("Ferrous Minerals ")
                mndwi = np.divide(arr_st[10], arr_st[7])
                ep.plot_bands(mndwi, cmap="RdYlGn", cols=1, vmin=-1, vmax=1, figsize=(10, 14))
                st.pyplot()



        
    
    if task == "Review Summary Report and Download Adjusted Data":
        st.write("'Before' Summary Table")
        bst=st.session_state.beforeSS
        st.dataframe(before.style.format({"Column DQ Score(%)": '{:,.2f}'}))

        st.write("")
        bodq_score = round(bst["Column DQ Score(%)"].mean(), 2)
        aodq_score = round(ast["Column DQ Score(%)"].mean(), 2)

        if bodq_score <= 25:
            before_arrow = 1
        elif bodq_score > 25 and bodq_score <= 50:
            before_arrow = 2
        elif bodq_score > 50 and bodq_score <= 75:
            before_arrow = 3
        else:
            before_arrow = 4

        if aodq_score <= 25:
            after_arrow = 1
        elif aodq_score > 25 and aodq_score <= 50:
            after_arrow = 2
        elif aodq_score > 50 and aodq_score <= 75:
            after_arrow = 3
        else:
            after_arrow = 4

        odq_graph = st.beta_columns(2)
        with odq_graph[0]:
            gauge(labels=['VERY LOW', 'LOW', 'MEDIUM', 'HIGH'], \
                  colors=["#1b0203", "#ED1C24", '#FFCC00', '#007A00'], arrow=before_arrow, title=str(bodq_score) + '%')
            plt.title("'Before' Overall DQ Score", fontsize=16)
            st.pyplot()
        with odq_graph[1]:
            gauge(labels=['VERY LOW', 'LOW', 'MEDIUM', 'HIGH'], \
                  colors=["#1b0203", "#ED1C24", '#FFCC00', '#007A00'], arrow=after_arrow, title=str(aodq_score) + '%')
            plt.title("'After' Overall DQ Score", fontsize=16)
            st.pyplot()