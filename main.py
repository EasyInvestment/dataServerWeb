import streamlit as st
import pandas as pd
import os
from fileManger import fileRead, fileList
from setting import Initialize
from Preprocessing import dataPreprocessing
from modeling import modelTraing
from visualization import visualizeTestData
from controlGainOptimization import bayesianOptimization
from st_on_hover_tabs import on_hover_tabs
from streamlit_antd_components import segmented
from streamlit_antd_components import tabs
from streamlit_antd_components import alert
from streamlit_antd_components import switch, BsIcon
from miminizeOptimization import miminizeOptimization
from basinhopping import basinhope
from dataCrawling import crawling
from dataSelect import Selector
from dataIndicator import Indicator
import warnings
# 경고 메시지 무시 설정
warnings.filterwarnings("ignore", message="I don't know how to infer vegalite type from 'empty'.*")

###############실행 방법################
#
#   command 창에 streamlit run 파일이름 --server.maxUploadSize 업로드 용량(MB)
#   실행을 원하는 파일이름을 적고 뒤에 업로드 용량을 적으셔야지 용량이 큰 파일도 업로드가 됩니다.
#   ex)
#   streamlit run main.py --server.maxUploadSize 2000
#   -> main.py를 실행하고 2GB의 데이터까지 업로드 할 수 있는 서버환경 구축됨
# 
#####################################

def session_state_ck():
    for key, _ in st.session_state.items():
        if key == "initCk":
            return True
    return False

def run():

    st.set_page_config(layout="wide")

    if not session_state_ck():
        Initialize()

    st.header("Easy Investment 데이터 모니터링 서버")
    st.markdown('<style>' + open('CSS/style.css').read() + '</style>', unsafe_allow_html=True)


    with st.sidebar:
        tabs = on_hover_tabs(tabName=["데이터 수집하기", "데이터 조회하기","카테고리별 지수"], 
                            iconName=["G","S","C"], default_choice=0)
    if tabs == "Home":
        # Create an empty placeholder
        if st.session_state["HomeButton"]:
            fileRead()
            fileList()
        else:
            # Create an empty placeholder
            button_placeholder = st.empty()

            # 버튼을 생성하고 클릭 이벤트를 처리합니다.
            if button_placeholder.button('시작', key='my_button'):
                st.session_state["HomeButton"] = True
                # Clear the placeholder to hide the button
                button_placeholder.empty()
                fileRead()
                fileList()

    if tabs == "파일 불러오기":
        fileRead()
        fileList()
    elif tabs == "데이터 수집하기":
        crawling()
    elif tabs == "데이터 조회하기":
        Selector()
    elif tabs == "카테고리별 지수":
        Indicator()
    elif tabs == "카테고리별 지수":
        pass
    elif tabs == "데이터 전처리":
        dataPreprocessing()

    elif tabs == "기계학습 모델링":
        if st.session_state["checkPreprocessing"] == False:
            dataPreprocessing()
        else:
            modelTraing(st.session_state["selectedData"])

    elif tabs == "데이터 가시화":
        visualizeTestData()

    elif tabs == "제어게인 최적화":
        bayesianOptimization()

    elif tabs == "제어게인 최적화2":
        miminizeOptimization()

    elif tabs == "제어게인 최적화3":
        basinhope()

if __name__ == "__main__":
    run()