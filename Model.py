import xgboost
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from keras.models import Sequential
from keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam, Adagrad, RMSprop, SGD
from tensorflow.keras.callbacks import EarlyStopping

class BaseModel:
    def __init__(self, input_dim, output_dim):
        self.input_dim = input_dim
        self.output_dim = output_dim

    def train(self, X_train, y_train):
        pass

    def predict(self, X_test):
        pass
class XgBoostModel(BaseModel):
    def __init__(self, input_dim, output_dim,n_estimators,learning_rate,gamma,subsample,colsample_bytree,max_depth):
        super().__init__(input_dim, output_dim)
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.subsample = subsample
        self.colsample_bytree = colsample_bytree
        self.max_depth = max_depth
        print(n_estimators, learning_rate, gamma, subsample, colsample_bytree, max_depth)
        self.model = self.build_model()

    def build_model(self):
        model = xgboost.XGBRegressor(n_estimators = self.n_estimators, learning_rate = self.learning_rate, gamma = self.gamma, subsample = self.subsample, colsample_bytree = self.colsample_bytree, max_depth = self.max_depth)
        return model
    
    def train(self,X_train,Y_train):
        self.model.fit(X_train,Y_train)

    def predict(self,X_test):
        return self.model.predict(X_test)
    
class RandomForestModel(BaseModel):

    def __init__(self, input_dim, output_dim,n_estimators,max_depth,min_samples_split,min_samples_leaf):
        super().__init__(input_dim, output_dim)
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.model = self.build_model()

    def build_model(self):
        model = RandomForestRegressor(n_estimators=self.n_estimators, max_depth=self.max_depth, min_samples_split=self.min_samples_split,min_samples_leaf=self.min_samples_leaf)
        return model

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.model.predict(X_test)

class SklearnMLPModel(BaseModel):

    def __init__(self, input_dim, output_dim, activation, solver, learning_rate, max_iter):
        super().__init__(input_dim, output_dim)
        self.activation = activation
        self.solver = solver
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.model = self.build_model()

    def build_model(self):
        model = MLPRegressor(activation=self.activation,solver=self.solver,learning_rate_init=self.learning_rate,max_iter=self.max_iter)
        return model
    
    def train(self, X_train, y_train):
        self.model = MLPRegressor()
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.model.predict(X_test)

class KerasMLPModel(BaseModel):
    dropout_rate = 0.2
    def __init__(self, input_dim, output_dim,epochs,batch_size,activation,learning_rate,optimizer):
        super().__init__(input_dim, output_dim)
        self.epochs = epochs
        self.batch_size = batch_size
        self.activation = activation

        if optimizer == "Adam":
            self.optimizer = Adam(learning_rate=learning_rate)

        elif optimizer == "Adagrad":
            self.optimizer = Adagrad(learning_rate=learning_rate)

        elif optimizer == "RMSprop":
            self.optimizer = RMSprop(learning_rate=learning_rate)

        elif optimizer == "SGD":
            self.optimizer = SGD(learning_rate=learning_rate)
        self.model = self.build_model()

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train, epochs=self.epochs, batch_size=self.batch_size)

    def build_model(self):
        model = Sequential()
        model.add(Dense(16, input_dim=self.input_dim, activation=self.activation))

        model.add(Dense(64, activation=self.activation))

        model.add(Dense(128, activation=self.activation))
        model.add(Dropout(self.dropout_rate))

        model.add(Dense(64, activation=self.activation))

        model.add(Dense(16, activation=self.activation))

        model.add(Dense(self.output_dim,activation="linear"))

        model.compile(loss='mse', optimizer=self.optimizer)
        return model

    def predict(self, X_test):
        return self.model.predict(X_test)