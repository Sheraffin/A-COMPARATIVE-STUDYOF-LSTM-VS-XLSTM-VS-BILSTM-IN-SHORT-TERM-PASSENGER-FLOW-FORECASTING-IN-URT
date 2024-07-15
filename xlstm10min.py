import os

# Define the directory names
inflow_dir = 'data/inflowdata'
outflow_dir = 'data/outflowdata'
meteorology_dir='data/meteorology'
adjacency_dir='data/adjacency'
# Create the directories if they don't exist
if not os.path.exists(inflow_dir):
    os.makedirs(inflow_dir)

if not os.path.exists(outflow_dir):
    os.makedirs(outflow_dir)

if not os.path.exists(meteorology_dir):
    os.makedirs(meteorology_dir)

if not os.path.exists(adjacency_dir):
    os.makedirs(adjacency_dir)

print("Directories created successfully.")

import numpy as np
from math import sqrt
import csv

def Get_All_Data(TG,time_lag,TG_in_one_day,forecast_day_number,TG_in_one_week):
	#deal with inflow data 处理进站数据
	metro_enter = []
	with open('data/inflowdata/in_'+str(TG)+'min.csv') as f:
		data = csv.reader(f, delimiter=",")
		for line in data:
			line=[int(x) for x in line]
			metro_enter.append(line)

	def get_train_data_enter(data,time_lag,TG_in_one_day,forecast_day_number,TG_in_one_week):
		data = np.array(data)
		data2 = np.zeros((data.shape[0], data.shape[1]))
		a = np.max(data)
		b = np.min(data)
		for i in range(len(data)):
			for j in range(len(data[0])):
				data2[i, j] = round((data[i, j]-b)/(a-b), 5)
		#不包括第一周和最后一周的数据
		#not include the first week and the last week among the five weeks
		X_train_1 = [[] for i in range(TG_in_one_week, len(data2[0]) - time_lag+1 - TG_in_one_day*forecast_day_number)]
		Y_train = []
		for index in range(TG_in_one_week, len(data2[0]) - time_lag+1 - TG_in_one_day*forecast_day_number):
			for i in range(276):
				temp=data2[i,index-TG_in_one_week: index + time_lag-1-TG_in_one_week].tolist()
				temp.extend(data2[i,index-TG_in_one_day: index + time_lag-1-TG_in_one_day])
				temp.extend(data2[i,index: index + time_lag-1])
				X_train_1[index-TG_in_one_week].append(temp)
			Y_train.append(data2[:,index + time_lag-1])
		X_train_1,Y_train = np.array(X_train_1), np.array(Y_train)
		print(X_train_1.shape,Y_train.shape)

		X_test_1 = [[] for i in range(len(data2[0]) - TG_in_one_day*forecast_day_number,len(data2[0])-time_lag+1)]
		Y_test = []
		for index in range(len(data2[0]) - TG_in_one_day*forecast_day_number,len(data2[0])-time_lag+1):
			for i in range(276):
				temp = data2[i, index-TG_in_one_week: index + time_lag-1-TG_in_one_week].tolist()
				temp.extend(data2[i, index-TG_in_one_day: index + time_lag-1-TG_in_one_day])
				temp.extend(data2[i, index: index + time_lag-1])
				X_test_1[index-(len(data2[0]) - TG_in_one_day*forecast_day_number)].append(temp)
			Y_test.append(data2[:, index + time_lag-1])
		X_test_1,Y_test = np.array(X_test_1), np.array(Y_test)
		print(X_test_1.shape, Y_test.shape)

		Y_test_original = []
		for index in range(len(data[0]) - TG_in_one_day*forecast_day_number,len(data[0])-time_lag+1):
			Y_test_original.append(data[:, index + time_lag-1])
		Y_test_original = np.array(Y_test_original)

		print(Y_test_original.shape)

		return X_train_1,Y_train,X_test_1,Y_test,Y_test_original,a,b

	
	X_train_1,Y_train,X_test_1,Y_test,Y_test_original,a,b=get_train_data_enter(metro_enter,time_lag,TG_in_one_day,forecast_day_number,TG_in_one_week)
	print(a,b)

	#deal with outflow data. Similar with the inflow data while not including the testing data for outflow
	
	metro_exit = []
	with open('data/outflowdata/out_'+str(TG)+'min.csv') as f:
		data = csv.reader(f, delimiter=",")
		for line in data:
			line = [int(x) for x in line]
			metro_exit.append(line)

	def get_train_data_exit(data,time_lag,TG_in_one_day,forecast_day_number,TG_in_one_week):
		data = np.array(data)
		data2 = np.zeros((data.shape[0], data.shape[1]))
		a = np.max(data)
		b = np.min(data)
		for i in range(len(data)):
			for j in range(len(data[0])):
				data2[i, j]=round((data[i, j]-b)/(a-b), 5)
		X_train_1 = [[] for i in range(TG_in_one_week, len(data2[0]) - time_lag+1 - TG_in_one_day*forecast_day_number)]
		for index in range(TG_in_one_week, len(data2[0]) - time_lag+1 - TG_in_one_day*forecast_day_number):
			for i in range(276):
				temp=data2[i, index-TG_in_one_week: index + time_lag-1-TG_in_one_week].tolist()
				temp.extend(data2[i, index-TG_in_one_day: index + time_lag-1-TG_in_one_day])
				temp.extend(data2[i, index: index + time_lag-1])
				X_train_1[index-TG_in_one_week].append(temp)
		X_train_1 = np.array(X_train_1)
		print(X_train_1.shape)

		X_test_1 = [[] for i in range(len(data2[0]) - TG_in_one_day*forecast_day_number, len(data2[0])-time_lag+1)]
		for index in range(len(data2[0]) - TG_in_one_day*forecast_day_number, len(data2[0])-time_lag+1):
			for i in range(276):
				temp = data2[i,index-TG_in_one_week: index + time_lag-1-TG_in_one_week].tolist()
				temp.extend(data2[i, index-TG_in_one_day: index + time_lag-1-TG_in_one_day])
				temp.extend(data2[i, index: index + time_lag-1])
				X_test_1[index-(len(data2[0]) - TG_in_one_day*forecast_day_number)].append(temp)
		X_test_1 = np.array(X_test_1)
		print(X_test_1.shape)
		return X_train_1, X_test_1

	X_train_2, X_test_2 = get_train_data_exit(metro_exit, time_lag, TG_in_one_day, forecast_day_number, TG_in_one_week)

	#deal with graph data. involve the adjacency matrix 
	adjacency = []
	with open('adjacency.csv') as f:
		data = csv.reader(f, delimiter=",")
		for line in data:
			line = [float(x) for x in line]
			adjacency.append(line)
	adjacency = np.array(adjacency)
	# use adjacency matrix to calculate D_hat**-1/2 * A_hat *D_hat**-1/2
	I = np.matrix(np.eye(276))
	A_hat = adjacency+I
	D_hat = np.array(np.sum(A_hat, axis=0))[0]
	D_hat_sqrt = [sqrt(x) for x in D_hat]
	D_hat_sqrt = np.array(np.diag(D_hat_sqrt))
	D_hat_sqrtm_inv = np.linalg.inv(D_hat_sqrt)# get the D_hat**-1/2 
	#D_A_final = D_hat**-1/2 * A_hat *D_hat**-1/2
	D_A_final = np.dot(D_hat_sqrtm_inv, A_hat)
	D_A_final = np.dot(D_A_final, D_hat_sqrtm_inv)
	print(D_A_final.shape)
	def get_train_data_graph(data,D_A_final,time_lag,TG_in_one_day,forecast_day_number,TG_in_one_week,):
		data = np.array(data)
		data2 = np.zeros((data.shape[0], data.shape[1]))
		a = np.max(data)
		b = np.min(data)
		for i in range(len(data)):
			for j in range(len(data[0])):
				data2[i,j]=round((data[i,j]-b)/(a-b),5)
		X_train_1 = [[] for i in range(TG_in_one_week, len(data2[0]) - time_lag+1 - TG_in_one_day*forecast_day_number)]
		for index in range(TG_in_one_week, len(data2[0]) - time_lag+1 - TG_in_one_day*forecast_day_number):
			for i in range(276):
				temp=data2[i,index: index + time_lag-1]
				X_train_1[index-TG_in_one_week].append(temp)
			X_train_1[index-TG_in_one_week] = np.dot(D_A_final, X_train_1[index-TG_in_one_week])
		X_train_1= np.array(X_train_1)
		print(X_train_1.shape)

		X_test_1 = [[] for i in range(len(data2[0]) - TG_in_one_day*forecast_day_number,len(data2[0])-time_lag+1)]
		for index in range(len(data2[0]) - TG_in_one_day*forecast_day_number,len(data2[0])-time_lag+1):
			for i in range(276):
				temp = data2[i,index: index + time_lag-1]
				X_test_1[index-(len(data2[0]) - TG_in_one_day*forecast_day_number)].append(temp)
			X_test_1[index-(len(data2[0]) - TG_in_one_day*forecast_day_number)] = np.dot(D_A_final, X_test_1[index-(len(data2[0]) - TG_in_one_day*forecast_day_number)])
		X_test_1 = np.array(X_test_1)
		print(X_test_1.shape)

		return X_train_1,X_test_1

	X_train_3, X_test_3 = get_train_data_graph(metro_enter, D_A_final, time_lag, TG_in_one_day, forecast_day_number, TG_in_one_week)

	#deal with meteorology data including the weather and PM data 
	Weather = []
	with open('data/meteorology/'+str(TG)+' min after normolization.csv') as f:
		data = csv.reader(f, delimiter=",")
		for line in data:
			line = [float(x) for x in line]
			Weather.append(line)

	def get_train_data_weather_PM(data, time_lag, TG_in_one_day, forecast_day_number, TG_in_one_week,):
		data = np.array(data)
		
		X_train_1 = [[] for i in range(TG_in_one_week, len(data[0]) - time_lag+1 - TG_in_one_day*forecast_day_number)]
		for index in range(TG_in_one_week, len(data[0]) - time_lag+1 - TG_in_one_day*forecast_day_number):
			for i in range(len(data)):
				#For meteorology data，we only consider today's data, namely recent pattern.
				X_train_1[index-TG_in_one_week].append(data[i,index: index + time_lag-1])
		X_train_1 = np.array(X_train_1)
		print(X_train_1.shape)

		X_test_1 = [[] for i in range(len(data[0]) - TG_in_one_day*forecast_day_number, len(data[0])-time_lag+1)]
		for index in range(len(data[0]) - TG_in_one_day*forecast_day_number, len(data[0])-time_lag+1):
			for i in range(len(data)):
				X_test_1[index-(len(data[0]) - TG_in_one_day*forecast_day_number)].append(data[i, index: index + time_lag-1])
		X_test_1 = np.array(X_test_1)
		print(X_test_1.shape)
		return X_train_1,X_test_1

	X_train_4, X_test_4 = get_train_data_weather_PM(Weather, time_lag, TG_in_one_day, forecast_day_number, TG_in_one_week)

	return X_train_1, Y_train, X_test_1, Y_test, Y_test_original, a, b, X_train_2, X_test_2, X_train_3, X_test_3, X_train_4, X_test_4

from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from math import sqrt
import numpy as np

#define weighted_mean_absolute_percentage_error and other eveluation metrics
def weighted_mean_absolute_percentage_error(Y_true, Y_pred):
	#The shape of the two matrixs are all n*276 where 276 is the station numbers
	total_sum=np.sum(Y_true)
	average=[]
	for i in range(len(Y_true)):
		for j in range(len(Y_true[0])):
			if Y_true[i][j]>0:
				
				temp=(Y_true[i][j]/total_sum)*np.abs((Y_true[i][j] - Y_pred[i][j]) / Y_true[i][j])
				average.append(temp)
	return np.sum(average)

def evaluate_performance(Y_test_original,predictions):
	RMSE = sqrt(mean_squared_error(Y_test_original, predictions))
	print('RMSE is: '+str(RMSE))
	R2 = r2_score(Y_test_original, predictions)
	print("R2 is："+str(R2))
	MAE=mean_absolute_error(Y_test_original, predictions)
	print("MAE is："+str(MAE))
	WMAPE=weighted_mean_absolute_percentage_error(Y_test_original, predictions)
	print("WMAPE is"+str(WMAPE))
	return RMSE, R2, MAE, WMAPE

"""**FOR 10 Minutes**"""
import numpy as np
np.random.seed(1)
import tensorflow as tf
tf.random.set_seed(2)
import numpy as np
np.set_printoptions(threshold=np.inf)
import time, os
import keras
keras.backend.set_image_data_format('channels_last')
from keras.layers import *
from keras.models import *
# https://pypi.python.org/pypi/pydot
!apt-get -qq install -y graphviz && pip install pydot
import pydot
from tensorflow.keras.utils import plot_model
from keras.models import load_model
from keras.optimizers import Adam
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt

from load_data import Get_All_Data

os.environ["PATH"] += os.pathsep + 'E:/Program Files (x86)/Graphviz2.38/bin' # used for visualizing the model

global_start_time = time.time()

def Unit(x, filters, pool=False):
    res = x
    if pool:
        x = MaxPooling2D(pool_size=(2, 2), padding="same")(x)
        res = Conv2D(filters=filters, kernel_size=[1, 1], strides=(2, 2), padding="same")(res)
    out = BatchNormalization()(x)
    out = Activation("relu")(out)
    out = Conv2D(filters=filters, kernel_size=[3, 3], strides=[1, 1], padding="same")(out)
    out = BatchNormalization()(out)
    out = Activation("relu")(out)
    out = Conv2D(filters=filters, kernel_size=[3, 3], strides=[1, 1], padding="same")(out)
    out = keras.layers.add([res, out])
    return out

def attention_3d_block(inputs, timesteps):
    a = Permute((2, 1))(inputs)
    a = Dense(timesteps, activation='linear')(a)
    a_probs = Permute((2, 1))(a)
    output_attention_mul = multiply([inputs, a_probs])
    return output_attention_mul

def extended_lstm_model(time_lag):
    input1_ = Input(shape=(276, time_lag-1, 3), name='input1')
    input2_ = Input(shape=(276, time_lag-1, 3), name='input2')
    input3_ = Input(shape=(276, time_lag-1, 1), name='input3')
    input4_ = Input(shape=(11, time_lag-1, 1), name='input4')

    # First input
    x1 = Conv2D(filters=32, kernel_size=[3, 3], strides=[1, 1], padding="same")(input1_)
    x1 = Unit(x1, 32)
    x1 = Unit(x1, 64, pool=True)
    x1 = Flatten()(x1)
    x1 = Dense(276)(x1)

    # Second input
    x2 = Conv2D(filters=32, kernel_size=[3, 3], strides=[1, 1], padding="same")(input2_)
    x2 = Unit(x2, 32)
    x2 = Unit(x2, 64, pool=True)
    x2 = Flatten()(x2)
    x2 = Dense(276)(x2)

    # Third input
    x3 = Conv2D(filters=32, kernel_size=[3, 3], strides=[1, 1], padding="same")(input3_)
    x3 = Unit(x3, 32)
    x3 = Unit(x3, 64, pool=True)
    x3 = Flatten()(x3)
    x3 = Dense(276)(x3)

    # Fourth input
    x4 = Flatten()(input4_)
    x4 = Dense(276)(x4)
    x4 = Reshape(target_shape=(276, 1))(x4)
    x4 = Bidirectional(LSTM(128, return_sequences=True, input_shape=(276, 1)))(x4)
    x4 = Bidirectional(LSTM(276, return_sequences=False))(x4)
    x4 = Dense(276)(x4)

    out = keras.layers.add([x1, x2, x3, x4])
    out = Reshape(target_shape=(276, 1))(out)
    out = Bidirectional(LSTM(128, return_sequences=True, input_shape=(276, 1)))(out)
    out = attention_3d_block(out, 276)
    out = Flatten()(out)
    out = Dense(276)(out)

    model = Model(inputs=[input1_, input2_, input3_, input4_], outputs=[out])
    return model

def build_model(X_train_1, X_train_2, X_train_3, X_train_4, Y_train, X_test_1, X_test_2, X_test_3, X_test_4, Y_test, Y_test_original, batch_size, epochs, a, time_lag):
    X_train_1 = X_train_1.reshape(X_train_1.shape[0], 276, time_lag-1, 3)
    X_train_2 = X_train_2.reshape(X_train_2.shape[0], 276, time_lag-1, 3)
    X_train_3 = X_train_3.reshape(X_train_3.shape[0], 276, time_lag-1, 1)
    X_train_4 = X_train_4.reshape(X_train_4.shape[0], 11, time_lag-1, 1)
    Y_train = Y_train.reshape(Y_train.shape[0], 276)

    X_test_1 = X_test_1.reshape(X_test_1.shape[0], 276, time_lag-1, 3)
    X_test_2 = X_test_2.reshape(X_test_2.shape[0], 276, time_lag-1, 3)
    X_test_3 = X_test_3.reshape(X_test_3.shape[0], 276, time_lag-1, 1)
    X_test_4 = X_test_4.reshape(X_test_4.shape[0], 11, time_lag-1, 1)
    Y_test = Y_test.reshape(Y_test.shape[0], 276)

    if epochs == 50:
        model = extended_lstm_model(time_lag)
        model.compile(optimizer=Adam(), loss='mse', metrics=['mse'])
        model.fit([X_train_1, X_train_2, X_train_3, X_train_4], Y_train, batch_size=batch_size, epochs=epochs, verbose=2, shuffle=False)
        output = model.predict([X_test_1, X_test_2, X_test_3, X_test_4], batch_size=batch_size)
    else:
        # train models every 10 epochs
        model = load_model('testresult/' + str(epochs - 10) + '-model-with-graph.h5')
        model.fit([X_train_1, X_train_2, X_train_3, X_train_4], Y_train, batch_size=batch_size, epochs=10, verbose=2, shuffle=False)
        output = model.predict([X_test_1, X_test_2, X_test_3, X_test_4], batch_size=batch_size)

    # rescale the output of this model
    predictions = np.zeros((output.shape[0], output.shape[1]))
    for i in range(len(predictions)):
        for j in range(len(predictions[0])):
            predictions[i, j] = round(output[i, j] * a, 0)
            if predictions[i, j] < 0:
                predictions[i, j] = 0

    RMSE, R2, MAE, WMAPE = evaluate_performance(Y_test_original, predictions)
    # visualize the model structure
    plot_model(model, to_file='model.png', show_shapes=True)

    return model, Y_test_original, predictions, RMSE, R2, MAE, WMAPE

def Save_Data(path, model, Y_test_original, predictions, RMSE, R2, MAE, WMAPE, Run_epoch):
    print(Run_epoch)
    RMSE_ALL = []
    R2_ALL = []
    MAE_ALL = []
    WMAPE_ALL = []
    Average_train_time = []
    RMSE_ALL.append(RMSE)
    R2_ALL.append(R2)
    MAE_ALL.append(MAE)
    WMAPE_ALL.append(WMAPE)
    model.save(path + str(Run_epoch) + '-model-with-graph.h5')
    np.savetxt(path + str(Run_epoch) + '-RMSE_ALL.txt', RMSE_ALL)
    np.savetxt(path + str(Run_epoch) + '-R2_ALL.txt', R2_ALL)
    np.savetxt(path + str(Run_epoch) + '-MAE_ALL.txt', MAE_ALL)
    np.savetxt(path + str(Run_epoch) + '-WMAPE_ALL.txt', WMAPE_ALL)
    with open(path + str(Run_epoch) + '-predictions.csv', 'w') as file:
        predictions = predictions.tolist()
        for i in range(len(predictions)):
            file.write(str(predictions[i]).replace("'", "").replace("[", "").replace("]", "") + "\n")
    with open(path + str(Run_epoch) + '-Y_test_original.csv', 'w') as file:
        Y_test_original = Y_test_original.tolist()
        for i in range(len(Y_test_original)):
            file.write(str(Y_test_original[i]).replace("'", "").replace("[", "").replace("]", "") + "\n")
    duration_time = time.time() - global_start_time
    Average_train_time.append(duration_time)
    np.savetxt(path + str(Run_epoch) + '-Average_train_time.txt', Average_train_time)
    print('total training time(s):', duration_time)

# Loading data
X_train_1, Y_train, X_test_1, Y_test, Y_test_original, a, b, X_train_2, X_test_2, X_train_3, X_test_3, X_train_4, X_test_4 = Get_All_Data(TG=10, time_lag=6, TG_in_one_day=72, forecast_day_number=5, TG_in_one_week=360)

Run_epoch = 50  # first training 50 epoch, and then add 10 epoch every time, run 15 times
for i in range(15):
    model, Y_test_original, predictions, RMSE, R2, MAE, WMAPE = build_model(
        X_train_1, X_train_2, X_train_3, X_train_4, Y_train,
        X_test_1, X_test_2, X_test_3, X_test_4, Y_test, Y_test_original,
        batch_size=64, epochs=Run_epoch, a=a, time_lag=6)
    Save_Data("testresult/", model, Y_test_original, predictions, RMSE, R2, MAE, WMAPE, Run_epoch)
    Run_epoch += 10

# Display the results

import matplotlib.pyplot as plt
print(f"RMSE: {RMSE}")
print(f"R2: {R2}")
print(f"MAE: {MAE}")
print(f"WMAPE: {WMAPE}")

# Plot the actual vs predictions
plt.figure(figsize=(15, 5))
plt.plot(Y_test_original.flatten(), label='Actual')
plt.plot(predictions.flatten(), label='Predicted')
plt.legend()
plt.title('Actual vs Predicted')
plt.show()