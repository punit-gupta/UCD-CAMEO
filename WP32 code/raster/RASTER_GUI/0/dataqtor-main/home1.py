import pandas as pd

import pandas_profiling

import streamlit as st

from streamlit_pandas_profiling import st_profile_report

from pandas_profiling import ProfileReport

from glob import glob
from raster import * 
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep

# function


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
    task = st.selectbox("Menu", ["Data Profiler", "Spatial Data Quality", "Review Summary Report and Download Adjusted Data"])
    
    if task == "Data Profiler":
             
        arr_st = np.stack(read("IMG_DATA/*B?*.jp2"))
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

            
        tab1, tab2, tab3= st.tabs(["Furious","NDVI", "SAVI", "VARI","MNDWI","NDMI"])





    if task == "Spatial Data Quality":
        st.write("")
        tab1, tab2, tab3 = st.tabs(["Completeness", "Accuracy", "Owl"])

        with tab1:
            st.header("Completeness")
            train=dataset
            total = train.isnull().sum().sort_values(ascending=False)
            percent = (train.isnull().sum()/train.count()).sort_values(ascending=False)
            missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
            missing_data.head()
            st.write("ss")
            st.write(missing_data.head())
            st.write(train.isna().sum().sum() / train.size * 100)
            st.write(train.isnull().sum().sum() / train.size * 100)

        with tab2:
            st.header("A dog")
        

        
    
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