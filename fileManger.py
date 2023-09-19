import pandas as pd
from nptdms import TdmsFile
import streamlit as st
import numpy as np


def fileRead():
    # CSV 파일 업로더 위젯 생성
    uploaded_file_csv = st.file_uploader("Upload a CSV file", type=["csv"])
    # 파일 업로드
    uploaded_tdms = st.file_uploader("Upload a TDMS file", type=["tdms"])

    uploaded_pkl = st.file_uploader("Upload a .pkl file", type=["pkl"])

    if uploaded_file_csv is not None and not uploaded_file_csv.name in st.session_state["dataName"]:
        st.session_state["csv_data"].append({uploaded_file_csv.name : pd.read_csv(uploaded_file_csv,index_col=0)})
        st.session_state["dataName"].append(uploaded_file_csv.name)

    if uploaded_tdms is not None and not uploaded_tdms.name in st.session_state["dataName"]:
        st.session_state["tdms_data"].append(uploaded_tdms)
        st.session_state["dataName"].append(uploaded_tdms.name)
    
    if uploaded_pkl is not None and not uploaded_pkl.name in st.session_state["dataName"]:
        st.session_state["pkl_data"].append(uploaded_pkl)
        st.session_state["dataName"].append(uploaded_pkl.name)

def fileList():
    st.write()
    st.write()
    st.subheader("불러온 파일 목록")

    if len(st.session_state["dataName"]) != 0:
        name = [i for i in st.session_state["dataName"]]
        dataList = pd.DataFrame(name,columns=["fileName"])
        st.write(dataList)