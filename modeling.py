import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from Model import RandomForestModel, SklearnMLPModel, KerasMLPModel,XgBoostModel
import numpy as np
import joblib
def selectScaler():
    scaler = ["Standard Scaler", "MinMaxScaler", "not used"] + [st.session_state["pkl_data"][i].name for i in range(len(st.session_state["pkl_data"]))]
    selected_scaler = st.selectbox("Scaler 선택",scaler)
    return selected_scaler

def selectModel():
    model_list = ["RamdomForestModel", "MLPModel(sklearn)","MLP(keras)","XGBoost"]
    selected_model = st.selectbox("데이터에 사용할 모델를 선택",model_list)
    return selected_model

def dataDivision(select_data):

    split_options = ['데이터 분할(Random)', '데이터 분할(슬라이드)']
    selected_split = st.radio('학습데이터 분할 방법, random / ratio:', split_options)

    if selected_split == "데이터 분할(Random)":
        number_input = st.number_input('학습데이터 분할 비율 :', min_value=1, max_value=100, value=80, step=1)
        test_size = 1 - number_input/100
        train_data_set,test_data_set = train_test_split(select_data,test_size=test_size,random_state=0)

    elif selected_split == "데이터 분할(슬라이드)":
        values = st.slider('Select a range of train data', 0, 100, (0, 75))
        st.write('학습데이터 비율:', values[1] - values[0],"%")
        data_length, low, high = len(select_data), values[0]/100, values[1]/100
        low_index = int(data_length * low)
        high_index = int(data_length * high)
        train_data_set = select_data.iloc[low_index:high_index]
        test_data_set = pd.concat([select_data.iloc[:low_index], select_data.iloc[high_index:]],axis=0)
    
    return train_data_set, test_data_set

def dataScaling(train_data,test_data,scaler):

    if scaler == "Standard Scaler":
        Scaler = StandardScaler().fit(train_data)
        scaling_train_data = Scaler.transform(train_data)
        scaling_test_data = Scaler.transform(test_data)
        return scaling_train_data,scaling_test_data,Scaler
    
    elif scaler == "MinMaxScaler":
        Scaler = MinMaxScaler().fit(train_data)
        scaling_train_data = Scaler.transform(train_data)
        scaling_test_data = Scaler.transform(test_data)
        return scaling_train_data, scaling_test_data,Scaler

    elif scaler == "not used":
        return train_data, test_data,None

    elif scaler[-3:] == "pkl":
        Scaler = joblib.load('scaler/' + scaler)
        scaling_train_data = Scaler.transform(train_data)
        scaling_test_data = Scaler.transform(test_data)
        return scaling_train_data, scaling_test_data,Scaler

def dataScalingY(train_data,test_data,scaler):

    if scaler == "Standard Scaler":
        Scaler = StandardScaler().fit(train_data)
        scaling_train_data = Scaler.transform(train_data)
        scaling_test_data = Scaler.transform(test_data)
        return scaling_train_data,scaling_test_data,Scaler
    
    elif scaler == "MinMaxScaler":
        Scaler = MinMaxScaler().fit(train_data)
        scaling_train_data = Scaler.transform(train_data)
        scaling_test_data = Scaler.transform(test_data)
        return scaling_train_data, scaling_test_data,Scaler

    elif scaler == "not used":
        return train_data, test_data,None

    elif scaler[-3:] == "pkl":
        Scaler = joblib.load('scaler/' + scaler[:-5]+"y"+scaler[-4:])
        scaling_train_data = Scaler.transform(train_data)
        scaling_test_data = Scaler.transform(test_data)
        return scaling_train_data, scaling_test_data,Scaler

def modelParameter(selected_model):

    if selected_model == "RamdomForestModel":
        n_estimators = st.number_input('n_estimators',value=100)
        max_depth = st.text_input('max_depth',"None")

        if max_depth == "None":
            max_depth = None
        else:
            try:
                max_depth = int(max_depth)
            except:
                max_depth = None
        
        min_samples_split = st.number_input('min_samples_split',value=2)
        min_samples_leaf = st.number_input('min_samples_leaf',value=1)
        return n_estimators,max_depth,min_samples_split,min_samples_leaf
    
    elif selected_model == "XGBoost":
        n_estimators = st.number_input('n_estimators',value=100)
        learning_rate = st.number_input('learning_rate',value=0.08)
        gama = st.number_input('gama',value=0)
        subsample = st.number_input('subsample',value=0.75)
        colsample_bytree = st.number_input('colsample_bytree',value=1)
        max_depth = st.number_input('max_depth',value=7)

        return n_estimators, learning_rate, gama, subsample, colsample_bytree, max_depth
    elif selected_model == "MLPModel(sklearn)":
        activation = st.selectbox("activation",("relu","identity", "logistic", "tanh"))
        solver = st.selectbox("optimaizer",("adam","sgd","lbfgs"))
        learning_rate_init = st.number_input('learning_rate',value=0.001,step=0.00001)
        max_iter = st.number_input('max_iter',value=200)

        return activation, solver, learning_rate_init, max_iter
    
    elif selected_model == "MLP(keras)":
        epochs = int(st.number_input('epochs',value=100))
        batch_size = st.number_input('batch_size',value=32)
        learning_rate = st.number_input('learning_rate',value=0.001)
        activation = "relu"
        optimizer = st.selectbox("Optimizer",("Adam","Adagrad","RMSprop","SGD"))

        return epochs, batch_size, activation, learning_rate, optimizer
    
def trainingWidget(model,x_train,y_train,type,selected_scaler,scaler_f,scaler_y):
    col1,col2 = st.columns(2)
    with col1:
        b1 = st.button("학습 실행")
        if b1:
            with st.spinner('학습 진행중...'):
                model.train(x_train,y_train)
            st.toast('학습 완료', icon='😍')
            if type == "RamdomForestModel":
                st.session_state["RandomForest"] = model
            elif type == "MLPModel(sklearn)":
                st.session_state["MLPsklearn"] = model
            elif type == "MLP(keras)":
                st.session_state["MLPkeras"] = model
            elif type == "XGBoost":
                st.session_state["XGBoost"] = model
    with col2:
        b2 = st.button("스케일러 저장")
        if b2:
            with st.spinner('저장중...'):
                st.session_state["scaler"] = scaler_f
                name = st.session_state["selected_data_name"] + "+" + selected_scaler
                joblib.dump(scaler_f, "scaler/"+name+'_f.pkl')
                joblib.dump(scaler_y, "scaler/"+name+'_y.pkl')
                st.toast('저장 완료', icon='😍')

def setData(x_train,x_test,y_train,y_test):
    st.session_state["x_train"] = x_train
    st.session_state["x_test"] = x_test
    st.session_state["y_train"] = y_train
    st.session_state["y_test"] = y_test

def modelTraing(select_data):
    train_data_set, test_data_set = dataDivision(select_data)
    selected_scaler = selectScaler()
    selected_model = selectModel()

    target = st.session_state["target"]

    x_train,x_test,y_train,y_test = train_data_set.drop([target],axis=1), test_data_set.drop([target],axis=1), train_data_set[target], test_data_set[target]

    x_train,x_test,Scaler_f = dataScaling(x_train,x_test,selected_scaler)
    y_train,y_test,Scaler_y = dataScalingY(y_train.to_numpy().reshape(-1,1),y_test.to_numpy().reshape(-1,1),selected_scaler)

    setData(x_train,x_test,y_train,y_test)

    input_dim = x_train.shape[1]
    output_dim = 1
    if selected_model == "RamdomForestModel":
        n_estimators,max_depth,min_samples_split,min_samples_leaf = modelParameter(selected_model)
        model = RandomForestModel(input_dim, output_dim,n_estimators,max_depth,min_samples_split,min_samples_leaf)

        trainingWidget(model,x_train,y_train, selected_model,selected_scaler,Scaler_f,Scaler_y)

    elif selected_model == "XGBoost":
        n_estimators, learning_rate, gama, subsample, colsample_bytree, max_depth = modelParameter(selected_model)
        model = XgBoostModel(input_dim, output_dim,n_estimators, learning_rate, gama, subsample, colsample_bytree, max_depth)
        trainingWidget(model,x_train,y_train, selected_model,selected_scaler,Scaler_f,Scaler_y)

    elif selected_model == "MLPModel(sklearn)":
        activation, solver, learning_rate_init, max_iter = modelParameter(selected_model)
        model = SklearnMLPModel(input_dim, output_dim, activation, solver, learning_rate_init, max_iter)

        trainingWidget(model,x_train,y_train, selected_model,selected_scaler,Scaler_f,Scaler_y)

    elif selected_model == "MLP(keras)":
        epochs, batch_size, activation, learning_rate, optimizer = modelParameter(selected_model)
        model = KerasMLPModel(input_dim, output_dim, epochs, batch_size, activation, learning_rate, optimizer)

        trainingWidget(model,x_train,y_train, selected_model,selected_scaler,Scaler_f,Scaler_y)