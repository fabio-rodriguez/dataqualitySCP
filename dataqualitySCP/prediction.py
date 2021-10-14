import joblib 
import keras
import numpy as np

from math import *
from sklearn import preprocessing

from constants import *


def path_to_prediction_models(path="/models/prediction"):
    '''Get the models path for predicting '''

    irr = "irradiance_model.h5"
    flow = "flow_model.h5"
    tamb = "tamb_model.h5"
    tin = "tin_model.h5"
    tout = "tout_model.h5"

    models = [irr, flow, tamb, tin, tout]
    
    return {k: f'{ROOT_DIR}/{path}/{m}' for k, m in zip(PREDICTION_KEYS, models)}


def get_predictions_scaler(path="./norm_scales"):
    '''Get the parameters of the scaler (mean and std) for predicting '''
    return joblib.load(f'{ROOT_DIR}/{path}/std_scaler.bin')


def predict(input, l1):
    '''Predict the correct sensor values from input variables'''

    models = path_to_prediction_models()
    scaler = get_predictions_scaler()
    
    Xs = [input[k] for k in KEYS]
    Xs_norm = scaler.transform([Xs])
    
    predictions = {}
    errors = {}

    for i, k in enumerate(KEYS):
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


def print_prediction_output(predictions, errors):
    
    print ("{:<8} {:<15} {:<10}".format('SENSOR','PREDICTION','ERROR'))

    for k in PREDICTION_KEYS:
        print ("{:<8} {:<15} {:<10}".format( k, str(round(predictions[k][0], 3)), str(round(errors[k], 3))))

