import streamlit as st
import numpy as np
from bayes_opt import BayesianOptimization

# black_box_function에서 모델 객체 가져오기
def black_box_function(**kwargs):
    target_value = st.session_state["target_value"]
    model = st.session_state[st.session_state["model_name"]]
    input_data = [float(value) for key, value in kwargs.items()]
    if st.session_state["model_name"] == "MLPkeras":
        output = model.predict(np.array(input_data).reshape(1, -1))[0][0]
    else:
        output = model.predict(np.array(input_data).reshape(1, -1))[0]
    return 1/(abs(output - target_value)+0.0000000001)

def bayesianOptimization():

    target_value = st.number_input("target값 입력")
    st.session_state["target_value"] = target_value

    selected_model = []
    if st.session_state["RandomForest"] != None:
        selected_model.append("RandomForest")
    if st.session_state["MLPsklearn"] != None:
        selected_model.append("MLPsklearn")
    if st.session_state["MLPkeras"] != None:
        selected_model.append("MLPkeras")
    if st.session_state["XGBoost"] != None:
        selected_model.append("XGBoost")
    model_name = st.selectbox("테스트 학습모델 선택", set(selected_model))
    data = st.session_state["selectedData"].drop([st.session_state["target"]],axis=1)

    pbounds = {}
    for i in range(len(data.columns)):
        curr_name = data.columns[i]
        col1,col2 = st.columns(2)
        with col1:
            val1 = st.number_input(curr_name+" 최소값 입력",value=0.0)
        with col2:
            ma = data[curr_name].mean()
            val2 = st.number_input(curr_name + " 최대값 입력",value=ma)
        pbounds[curr_name] = (val1,val2)
    st.session_state["model_name"] = model_name
    epochs = int(st.number_input("epoch 입력",value=100))
    b1 = st.button("Search best PID parameter")
    if b1:
        with st.spinner('찾는중...'):
            optimizer = BayesianOptimization(
                f=black_box_function,
                pbounds=pbounds,
                random_state=1,
                allow_duplicate_points=True
            )
            optimizer.maximize(
                init_points=10,
                n_iter=epochs,
            )

            st.write('Print best PID parameter')
            result = optimizer.max
            st.write("target :",result["target"])

            for key, value in result["params"].items():
                print(key,value)
                st.write(key + " : " + str(value))

            st.toast('완료', icon='😍')
        input_data = [float(value) for key, value in result["params"].items()]
        st.session_state["param"] = input_data
        # model = st.session_state[st.session_state["model_name"]]
        # if st.session_state["model_name"] == "MLPkeras":
        #     output = model.predict(np.array(input_data).reshape(1, -1))[0][0]
        # else:
        #     output = model.predict(np.array(input_data).reshape(1, -1))[0]
        # st.write("output:",output)
        # st.write("taget - output :",target_value-output)
    if st.session_state["param"] != None:
        trained_model = [] 
        if st.session_state["RandomForest"] != None:
            trained_model.append("RandomForest")
        if st.session_state["MLPsklearn"] != None:
            trained_model.append("MLPsklearn")
        if st.session_state["MLPkeras"] != None:
            trained_model.append("MLPkeras")
        selected_model = st.selectbox("Model 선택",trained_model)
        model = st.session_state[selected_model]
        input_data = st.session_state["param"]
        if selected_model == "MLPkeras":
            output = model.predict(np.array(input_data).reshape(1, -1))[0][0]
        else:
            output = model.predict(np.array(input_data).reshape(1, -1))[0]
        st.write("target:",target_value)
        st.write("output:",output)
        st.write("|taget - output| :",abs(target_value-output))
        st.write("상대오차(%) :",np.round((abs(target_value-output)/abs(target_value)) * 100,2),"%")