import joblib 
import keras
import numpy as np
import os

from math import *
from multiprocessing import Process, Queue
from sklearn import preprocessing


KEY_IRR = "IRR"
KEY_FLOW = "FLOW"
KEY_TAMB = "TAMB"
KEY_TIN = "TIN"
KEY_TOUT = "TOUT"
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

keys = [KEY_IRR, KEY_FLOW, KEY_TAMB, KEY_TIN, KEY_TOUT]
prediction_keys = [KEY_IRR, KEY_FLOW, KEY_TIN, KEY_TOUT]


def read_inputs():
    '''Function for reading the input data'''

    irr = float(input("Irradiance: "))
    flow = float(input("Flow: "))
    tamb = float(input("Ambient Temperature: "))
    tin = float(input("Inlet Temperature: "))
    tout = float(input("Outlet Temperature: "))

    values = [irr, flow, tamb, tin, tout]

    return {k: v for k, v in zip(keys, values)}



def path_to_prediction_models(path="/models/prediction"):
    '''Get the models path for predicting '''

    irr = "irradiance_model.h5"
    flow = "flow_model.h5"
    tin = "tin_model.h5"
    tout = "tout_model.h5"

    models = [irr, flow, tin, tout]
    
    return {k: f'{ROOT_DIR}/{path}/{m}' for k, m in zip(prediction_keys, models)}


def get_predictions_scaler(path="./norm_scales"):
    '''Get the parameters of the scaler (mean and std) for predicting '''
    return joblib.load(f'{ROOT_DIR}/{path}/std_scaler.bin')


def predict(input, l1):
    '''Predict the correct sensor values from input variables'''

    models = path_to_prediction_models()
    scaler = get_predictions_scaler()
    
    Xs = [input[k] for k in keys]
    Xs_norm = scaler.transform([Xs])
    
    predictions = {}
    errors = {}

    for i, k in enumerate(keys):
        if k not in models.keys():
            continue

        Xi = Xs_norm[:]
        Xi = np.delete(Xi, [i], 1)
        model = keras.models.load_model(models[k])

        y_pred = model.predict(Xi)
        y_pred = [yi[0]*sqrt(scaler.var_[i])+scaler.mean_[i] for yi in y_pred]
        
        predictions[k] = y_pred
        errors[k] = abs(y_pred[0]-Xs[i])

    l1.put((predictions, errors))


def __exe__():

    input = read_inputs()

    l1 = Queue()
    p1 = Process(target=predict, args=(input, l1, ))  
    l2 = Queue()
    p2 = Process(target=func1, args=(200, l2, )) 
    p1.start()   
    p2.start()      
    print_prediction_output(*l1.get()) 
    # print(l2.get())


def func1(x, l1):
    l1.put(1)


def print_prediction_output(predictions, errors):
    
    print ("{:<8} {:<15} {:<10}".format('SENSOR','PREDICTION','ERROR'))

    for k in prediction_keys:
        print ("{:<8} {:<15} {:<10}".format( k, str(round(predictions[k][0], 3)), str(round(errors[k], 3))))


if __name__ == '__main__':
    
    __exe__()    