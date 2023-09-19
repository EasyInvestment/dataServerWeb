import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error

def visualizeResults(pred,y_test):
    import altair as alt
    # from vega_datasets import data

    # source = data.cars()

    fig, ax = plt.subplots(figsize=(25, 5))
    ax.scatter(range(len(pred)), pred, label='Predict', color='b', marker='o')
    ax.scatter(range(len(y_test)), y_test, label='True Label', color='r', marker='x')
    ax.legend()
    ax.set_xlabel('Index')
    ax.set_ylabel('Value')
    ax.set_title('Predict | True Label')

    t = pd.DataFrame(y_test.reshape(-1,1),columns=["actual"])
    t = pd.concat([t,pd.DataFrame(pred.reshape(-1,1),columns=["predict"])],axis=1)
    chart = alt.Chart(t).mark_circle().encode(
        x='actual',
        y='predict',
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

    mae = np.round(np.mean(np.abs(pred - y_test)),5)
    mse = np.round(np.mean((pred - y_test)**2),5)
    st.write("MAE:{} (s)".format(mae))
    st.write("MSE:{}".format(mse))
    st.divider()
    st.write("R2:{0:.4f}".format((r2_score(y_test, pred))))
    st.write("RMSE: {0:.4f} (s)".format(mean_squared_error(y_test,pred)**0.5))

    st.divider()
    st.write("MAPE: {0:.4f} * 100%".format(mean_absolute_percentage_error(y_test, pred)))
    # print('RMSE: {0:.4f} (s)'.format(mean_squared_error(y_test,pred)**0.5))
    # print("MAPE: {0:.4f} * 100%".format(mean_absolute_percentage_error(y_test, pred)))

def visualizeTestData():
    trained_model = []
    if st.session_state["RandomForest"] != None:
        trained_model.append("RandomForest")
    if st.session_state["MLPsklearn"] != None:
        trained_model.append("MLPsklearn")
    if st.session_state["MLPkeras"] != None:
        trained_model.append("MLPkeras")
    if st.session_state["XGBoost"] != None:
        trained_model.append("XGBoost")
    model_name = st.selectbox("테스트 학습모델 선택", set(trained_model))

    b1 = st.button("테스트 실행")
    if b1:
        with st.spinner('테스트 진행중...'):
            x_test = st.session_state["x_test"]
            y_test = st.session_state["y_test"]

            model = st.session_state[model_name]
            pred = model.predict(x_test)
            visualizeResults(pred,y_test)
        st.toast('테스트 완료', icon='😍')