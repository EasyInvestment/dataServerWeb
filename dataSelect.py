import pymysql
import streamlit as st
import pandas as pd
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

def  Selector():
    sumData = {}
    if st.session_state["database"] == None:
        database = getDatabaseName()
        st.session_state["database"] = database
        for i in range(len(database)):
            table = getTableName(database[i])
            sumData[database[i]] = table
        st.session_state["sumData"] = sumData
    else:
        database = st.session_state["database"]
        sumData = st.session_state["sumData"]

    selected_cate = st.selectbox("카테고리 선택",database)
    selected_table = st.selectbox("종목 선택",sumData[selected_cate])
    b1 = st.button("데이터 보기")
    if b1:
        data = dataAll(str(selected_cate), str(selected_table))
        st.write(data)
