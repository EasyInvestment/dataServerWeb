import pymysql
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
def dataAll(database,table):
    # 커서 생성
    con = connect_db(database)
    cursor = con.cursor()

    # 모든 데이터 가져오기
    cursor.execute("SELECT * FROM "+table)

    data = cursor.fetchall()

    column_names = [i[0] for i in cursor.description]

    df = pd.DataFrame(data, columns=column_names)

    # 연결 및 커서 닫기
    cursor.close()
    con.close()

    return df
def connect_db(database):
    host = "investment.cu24cf6ah5lb.us-west-1.rds.amazonaws.com"
    port = 3306
    username = "someone555"
    database = database
    password = "12345asdfg"
    try:
        con = pymysql.connect(host=host, user=username, password=password,
                db=database, charset='utf8') # 한글처리 (charset = 'utf8')
    except Exception as e:
        print(">> connection 실패 ",e)
        return False

    return con
def getDatabaseName():
    host = "investment.cu24cf6ah5lb.us-west-1.rds.amazonaws.com"
    port = 3306
    username = "someone555"
    password = "12345asdfg"
    con = pymysql.connect(
        host=host,
        user=username,
        password=password,
        database='information_schema'  # information_schema 데이터베이스에 접속하여 데이터베이스 목록을 가져옵니다.
    )

    # 커서 생성
    cursor = con.cursor()

    # 데이터베이스 목록 조회
    cursor.execute("SHOW DATABASES")

    # 결과 가져오기
    databases = cursor.fetchall()
    databaseName = [i[0] for i in databases]
    cursor.close()
    con.close()
    return databaseName

def getTableName(database):
    con = connect_db(database)
    # 커서 생성
    cursor = con.cursor()

    # 테이블 목록 조회
    cursor.execute("SHOW TABLES")

    # 결과 가져오기
    tables = cursor.fetchall()
    tables = [table[0] for table in tables]
    cursor.close()
    con.close()

    return tables

def Indicator():
    table = getTableName("categoryIndicator")
    selected_cate = st.selectbox("카테고리 선택",table)
    b1 = st.button("데이터 보기")
    if b1:
        data = dataAll("categoryIndicator", str(selected_cate))
        import altair as alt
        # from vega_datasets import data

        # source = data.cars()

        fig, ax = plt.subplots(figsize=(25, 5))
        ax.plot(data["timestamp"],data["close"])
        ax.legend()
        ax.set_xlabel('timestamp')
        ax.set_ylabel('close')
        ax.set_title(selected_cate)

        chart = alt.Chart(data).mark_line().encode(
            x='timestamp',
            y='close',
            # color='Origin',
        ).interactive()

        tab1, tab2 = st.tabs(["chart1", "chart2"])

        with tab1:
            # Use the Streamlit theme.
            # This is the default. So you can also omit the theme argument.
            st.altair_chart(chart, theme=None, use_container_width=True)
        with tab2:
            # Use the native Altair theme.
            st.pyplot(fig)
