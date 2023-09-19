import streamlit as st
import pandas as pd
from streamlit_antd_components import transfer
def findData(name):
    for i in st.session_state["csv_data"]:
        if name == list(i.keys())[0]:
            return i[list(i.keys())[0]]
    return None

def dataPreprocessing():
    availableFiles = st.session_state["dataName"]
    selected_data_name = st.selectbox("데이터 선택",availableFiles)
    st.session_state["selected_data_name"] = selected_data_name
    data = findData(selected_data_name)

    st.dataframe(data)

    if type(data) != type(None):
        select_data,select_columns = selectFeature(data)
        target = selectTarget(select_columns)

        b1 = st.button("데이터 저장")
        if b1:
            with st.spinner('저장중...'):
                st.session_state["selectedData"] = select_data
                st.session_state["target"] = target
                st.session_state["checkPreprocessing"] = True
                st.toast('저장 완료', icon='😍')


def selectFeature(data):
    st.write("Feature 선택")
    label = ["Source", "Target"]
    selected_columns = transfer(
        items=list(data.columns),
        index=[],
        label=label
    )
    select_data = data[selected_columns]
    select_data = select_data.dropna()
    return select_data,selected_columns

def selectTarget(selected_columns):
    st.write("Target 선택")
    target = st.radio(
    "Target 선택",
    set(selected_columns))
    return target