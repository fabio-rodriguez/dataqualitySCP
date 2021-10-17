import numpy as np
import pandas as pd
import scipy.io
import time

from multiprocessing import Process, Queue

from constants import *
from evaluation import evaluate
from main import parse_input
from prediction import predict


def __exe__(input, verbose=False):

    l1 = Queue()
    p1 = Process(target=evaluate, args=(input, l1, ))  
    l2 = Queue()
    p2 = Process(target=predict, args=(input, l2, )) 
    p1.start()   
    p2.start()     
    
    evaluations = l1.get()
    predictions, errors = l2.get()
    
    if verbose:
        print_output(evaluations, predictions, errors) 

    return evaluations, predictions, errors 


def __exe_dataframe__(dataset_root, outputs_path, verbose=False):
    
    exp_1data = scipy.io.loadmat(dataset_root)
    data = exp_1data[list(exp_1data.keys())[-1]][0][0]
    validation_set = np.transpose([data[:, 0], data[:, 5], data[:, 11], data[:, 8], data[:, 9], data[:, 6]])

    df = pd.DataFrame(columns=(
        'Irr', 'Irr_Fault_Free', 'Irr_Fault_Pred', 'Irr_Prediction', 'Irr_Pred_Error',
        'Flow', 'Flow_Fault_Free', 'Flow_Fault_Free', 'Flow_Prediction', 'Flow_Pred_Error',
        'Tamb', 'Tamb_Fault_Free', 'Tamb_Fault_Free', 'Tamb_Prediction', 'Tamb_Pred_Error',
        'Tin', 'Tin_Fault_Free', 'Tin_Fault_Free', 'Tin_Prediction', 'Tin_Pred_Error', 
        'Tout', 'Tout_Fault_Free', 'Tout_Fault_Free', 'Tout_Prediction', 'Tout_Pred_Error',
    ))

    pred_error = {k: [] for k in KEYS}
    eval_error = {k: [] for k in KEYS}

    for i, row in enumerate(validation_set):

        input = {k: v for k, v in zip(KEYS, row)}
        evaluations, predictions, errors = __exe__(input)

        for k in KEYS:
            # TODO Get wheter or not the value is Fault
            eval_error[k].append(0)
            pred_error[k].append(errors[k])

        output_row = []        
        for k in PREDICTION_KEYS:
            output_row.append(input[k]) 
            # TODO Get wheter or not the value is Fault
            output_row.append(None) 
            output_row.append("NO" if evaluations[k] else "YES") 
            output_row.append(round(predictions[k][0], 3)) 
            output_row.append(round(errors[k], 3)) 

        df.loc[i] = output_row

    print(df)    
    df.to_csv(outputs_path)

    if verbose:
        print_errors(eval_error, pred_error)


def print_output(evaluations, predictions, errors):
    
    print ("{:<8} {:<15} {:<15} {:<10}".format('SENSOR', 'FAULT FREE', 'PREDICTION','ERROR'))

    for k in PREDICTION_KEYS:
        print ("{:<8} {:<15} {:<15} {:<10}".format( 
            k, 
            "NO" if evaluations[k] else "YES", 
            str(round(predictions[k][0], 3)), 
            str(round(errors[k], 3))
        ))

    print()


def print_errors(eval_error, pred_error):
    
    print ("{:<8} {:<15} {:<15} {:<10}".format('SENSOR', 'EVAL MEAN ERROR', 'PRED MEAN ERROR'))

    for k in PREDICTION_KEYS:
        print ("{:<8} {:<20} {:<20}".format( 
            k, 
            str(round(sum(eval_error[k])/len(eval_error[k]), 3)),
            str(round(sum(pred_error[k])/len(pred_error[k]), 3))
        ))

    print()


if __name__ == '__main__':
    
    option, values = parse_input()

    t0 = time.time()

    if option == "simple":
        input = {k: v for k, v in zip(KEYS, values)}
        __exe__(input, verbose=True)    
    
    elif option == "dataset": 
        dataset_root, outputs_path = values
        __exe_dataframe__(dataset_root, outputs_path)

    tf = round((time.time()-t0)/60, 2)
    print(f"**Computing Time: {tf} minutes.")