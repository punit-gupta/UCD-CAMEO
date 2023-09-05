import pandas as pd

import pandas_profiling

import streamlit as st

from streamlit_pandas_profiling import st_profile_report

from pandas_profiling import ProfileReport

st.set_page_config(page_title="CAMEO Spatial Data Quality!", page_icon="🔍", layout="wide")

st.title("CAMEO Spatial Data Quality!")

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

if uploaded_file is None:
    st.write("")
    st.info('Awaiting for file to be uploaded.')
    st.write("")
    """
    **Get your data ready for use before you start working with it:**

    1. Upload your Excel/CSV file  
    """
else: 
    dataset = reading_dataset()
    before = beforeSTable()
    task = st.selectbox("Menu", ["Data Profiler", "Spatial Data Quality", "Review Summary Report and Download Adjusted Data"])
    st.session_state.beforeSS = before
    if task == "Data Profiler":
        pr = ProfileReport(dataset, explorative=True, orange_mode=True)
        st_profile_report(pr)   
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