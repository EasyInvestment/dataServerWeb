import streamlit as st
def Initialize():
    st.session_state["HomeButton"] = False

    st.session_state["csv_data"] = []
    st.session_state["tdms_data"] = []
    st.session_state["pkl_data"] = []
    st.session_state["dataName"] = []
    st.session_state["selectedData"] = None
    st.session_state["selected_data_name"] = None
    st.session_state["target"] = None

    st.session_state["scaler"] = None

    st.session_state["RandomForest"] = None
    st.session_state["MLPsklearn"] = None
    st.session_state["MLPkeras"] = None
    st.session_state["XGBoost"] = None

    st.session_state["x_train"] = None
    st.session_state["x_test"] = None
    st.session_state["y_train"] = None
    st.session_state["y_test"] = None

    st.session_state["target_value"] = None

    st.session_state["checkPreprocessing"] = False

    st.session_state["initCk"] = True

    st.session_state["param"] = None
    st.session_state["optmodel"] = None

    st.session_state["database"] = None
    st.session_state["sumData"] = None