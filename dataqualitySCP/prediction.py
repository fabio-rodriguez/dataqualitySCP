import numpy as np
import statistics

from math import *

from .constants import *


def predict(input, l1):
    '''Predict the correct sensor values from input variables'''

    scaler = PREDICTION_SCALER
    
    Xs = np.transpose([input[k] for k in KEYS])
    Xs_norm = scaler.transform(Xs)
    
    predictions = {}
    errors = {}

    for i, k in enumerate(KEYS):
        if k not in PREDICTION_MODELS.keys():
            continue

        Xi = np.delete(Xs_norm, [i], 1)
        y = Xs[:, i]

        model = PREDICTION_MODELS[k]
        y_pred = model.predict(Xi)
        y_pred = [yi[0]*sqrt(scaler.var_[i])+scaler.mean_[i] for yi in y_pred]

        
        predictions[k] = y_pred
        e = np.abs(np.array(y)-np.array(y_pred))
        errors[k] = {'MEAN_ERROR': sum(e)/len(e), 'STD_ERROR': statistics.pstdev(e)}

    # return predictions, errors
    l1.put((predictions, errors))


def print_prediction_output(predictions, errors):
    
    print ("{:<8} {:<15} {:<10}".format('SENSOR','PREDICTION','ERROR'))

    for k in PREDICTION_KEYS:
        print ("{:<8} {:<15} {:<10}".format( k, str(round(predictions[k][0], 3)), str(round(errors[k], 3))))

