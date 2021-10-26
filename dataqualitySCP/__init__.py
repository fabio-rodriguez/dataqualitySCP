import numpy as np
import pandas as pd
import scipy.io

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
    
    input = {key: df[key] for key in KEYS}
    evaluations, predictions, errors = __exe__(input, True) 


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
        print_errors(evaluations, errors) 

    return evaluations, predictions, errors 


def print_errors(eval_error, pred_error):
    
    print ("{:<8} {:<20} {:<20} {:<20}".format('SENSOR', 'EVAL_ACCURACY', 'PRED_MEAN_ERROR', 'PRED_STD_ERROR'))

    for k in PREDICTION_KEYS:
        print ("{:<8} {:<20} {:<20} {:<20}".format( 
            k, 
            'nil',# str(round(sum(eval_error[k])/len(eval_error[k]), 3)),
            str(round(pred_error[k]['MEAN_ERROR'], 3)),
            str(round(pred_error[k]['STD_ERROR'], 3)),
        ))

def dummy(arg1, arg2):
    arg2.put("example")


if __name__ == '__main__':
    pass