from os import error
import numpy as np
import pandas as pd
import statistics

from multiprocessing import Process, Queue

from .constants import *
from .evaluation import evaluate
from .prediction import predict


def process_input(irr, flow, tamb, tin, tout, verbose=False):
    input = {KEY_IRR: irr, KEY_FLOW: flow, KEY_TAMB: tamb, KEY_TIN: tin, KEY_TOUT: tout}
    return __exe__(input, verbose)


## TODO
def process_dataset(path_to_dataset, path_to_output_folder, verbose=False):
    pass


## TODO
def default_validation(path_to_output_folder):
    df = pd.read_csv(f'{ROOT_DIR}/{PATH_TO_DATASETS}/validation_data.csv') 
    
    # IRR,INPUT_IRR,FAULT_IRR
    reals = {key: df[{key}] for key in KEYS}
    inputs = {key: df[f"INPUT_{key}"] for key in KEYS}
    faults = {key: df[f"FAULT_{key}"] for key in KEYS}
    
    evaluations, predictions = __exe__(inputs) 

    eval_errors = {key: [] for key in EVALUATION_KEYS}
    pred_errors = {key: [] for key in EVALUATION_KEYS}
    full_predictions = {key: [] for key in EVALUATION_KEYS}
    
    for key in EVALUATION_KEYS:
        for i, e in enumerate(evaluations):
            eval_errors.append(e[key] == bool(faults[key][i]))
            
            if not e[key]:
                full_predictions[key].append(inputs[key][i])
            else:
                full_predictions[key].append(predictions[key][i])
                pred_errors[key].append(abs(predictions[key][i]-reals[key][i])) 

    measures = { key: {
                    "EVAL_ERROR": sum(eval_errors[key])/len(eval_errors[key]), 
                    "MEAN_ERROR": sum(pred_errors[key])/len(pred_errors[key]), 
                    "STD_ERROR": statistics.stdev(pred_errors[key])
                } for key in EVALUATION_KEYS }

    ## Crear output file and output dataframe 
    return measures, full_predictions


def __exe__(input):

    l1 = Queue()
    p1 = Process(target=evaluate, args=(input, l1, ))  
    l2 = Queue()
    p2 = Process(target=predict, args=(input, l2, )) 
    p1.start()   
    p2.start()     
    
    evaluations = l1.get()
    predictions = l2.get()
    
    return evaluations, predictions 


def print_errors(eval_error, pred_error):
    
    print ("{:<8} {:<20} {:<20} {:<20}".format('SENSOR', 'EVAL_ACCURACY', 'PRED_MEAN_ERROR', 'PRED_STD_ERROR'))

    for k in PREDICTION_KEYS:
        print ("{:<8} {:<20} {:<20} {:<20}".format( 
            k, 
            'nil',# str(round(sum(eval_error[k])/len(eval_error[k]), 3)),
            str(round(pred_error[k]['MEAN_ERROR'], 3)),
            str(round(pred_error[k]['STD_ERROR'], 3)),
        ))


if __name__ == '__main__':
    pass