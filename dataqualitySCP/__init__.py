import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics

from multiprocessing import Process, Queue
from os import error

from .constants import *
from .evaluation import evaluate
from .prediction import predict


def process_dataset(path_to_output_folder, path_to_dataset=f'{ROOT_DIR}/{PATH_TO_DATASETS}/validation_data.csv'):
    
    df = pd.read_csv(f'{path_to_dataset}') if path_to_dataset.endswith(".csv") else pd.read_excel(f'{path_to_dataset}')

    reals = {key: df[key] for key in KEYS}
    inputs = {key: df[f"INPUT_{key}"] for key in KEYS}
    faults = {key: df[f"FAULT_{key}"] for key in KEYS}
    
    evaluations, predictions = __exe__(inputs) 

    eval_errors_measure = {key: [] for key in EVALUATION_KEYS}
    eval_errors = {key: [] for key in EVALUATION_KEYS}
    pred_errors = {key: [] for key in EVALUATION_KEYS}
    full_predictions = {key: [] for key in EVALUATION_KEYS}
    full_predictions = {key: [] for key in EVALUATION_KEYS}
    
    for key in EVALUATION_KEYS:
        for i, e in enumerate(evaluations):
            eval_errors_measure[key].append(e[key] == bool(faults[key][i]))
            eval_errors[key].append(e[key])

            if not e[key]:
                full_predictions[key].append(inputs[key][i])
                pred_errors[key].append(0) 
            else:
                full_predictions[key].append(predictions[key][i])
                pred_errors[key].append(abs(predictions[key][i]-reals[key][i])) 

    pred_error_measure = { key: [error for error in pred_errors[key] if error != 0]  for key in EVALUATION_KEYS }
    measures = {key:{
                        "EVAL_ERROR": sum(eval_errors_measure[key])/len(eval_errors_measure[key]), 
                        "MEAN_ERROR": sum(pred_error_measure[key])/len(pred_error_measure[key]), 
                        "STD_ERROR": statistics.stdev(pred_errors[key])
                    } for key in EVALUATION_KEYS }

    output_predictions(df, eval_errors, pred_errors, full_predictions, measures, path_to_output_folder)


def __exe__(inputs, verbose=False):
    '''
        "verbose" argument is reserved for simple inputs.
    '''

    l1 = Queue()
    p1 = Process(target=evaluate, args=(inputs, l1, ))  
    l2 = Queue()
    p2 = Process(target=predict, args=(inputs, l2, )) 
    p1.start()   
    p2.start()     
    
    evaluations = l1.get()
    predictions = l2.get()
    
    if verbose:
        print_output(inputs, evaluations, predictions)

    return evaluations, predictions 


def output_predictions(df, eval_errors, pred_errors, full_predictions, measures, path_to_output_folder):
    
    headers = [
        "Hour",
        "IRR", "INPUT_IRR", "FAULT_IRR", "DETECTION_IRR", "PREDICTION_IRR", "OFFSET_IRR", 
        "FLOW", "INPUT_FLOW", "FAULT_FLOW", "DETECTION_FLOW", "PREDICTION_FLOW", "OFFSET_FLOW",
        "TAMB", "INPUT_TAMB", "FAULT_TAMB",     # "DETECTION_TAMB", "PREDICTION_TAMB",
        "TIN", "INPUT_TIN", "FAULT_TIN",        # "DETECTION_TIN", "PREDICTION_TIN",
        "TOUT", "INPUT_TOUT", "FAULT_TOUT",     # "DETECTION_TOUT", "PREDICTION_TOUT"
    ]
    data = np.array([
        df['Hour'],
        df["IRR"], df["INPUT_IRR"], df["FAULT_IRR"], eval_errors["IRR"], full_predictions["IRR"], pred_errors["IRR"],
        df["FLOW"], df["INPUT_FLOW"], df["FAULT_FLOW"], eval_errors["FLOW"], full_predictions["FLOW"], pred_errors["FLOW"],
        df["TAMB"], df["INPUT_TAMB"], df["FAULT_TAMB"],     # eval_errors["TAMB"], full_predictions["TAMB"],
        df["TIN"], df["INPUT_TIN"], df["FAULT_TIN"],        # eval_errors["TIN"], full_predictions["TIN"],
        df["TOUT"], df["INPUT_TOUT"], df["FAULT_TOUT"],     # eval_errors["TOUT"], full_predictions["TOUT"]
    ]) 
    output_data = pd.DataFrame(np.transpose(data), columns=headers)
    output_data.to_csv(f'{path_to_output_folder}/output.csv', index=True)

    headers = ["SENSOR", "DETECTION_PRECISION", "MEAN_PREDICTION_ERROR", "STD_PREDICTION_ERROR"] 
    data = np.array([
        [KEY_IRR, measures[KEY_IRR]["EVAL_ERROR"], measures[KEY_IRR]["MEAN_ERROR"], measures[KEY_IRR]["STD_ERROR"]],
        [KEY_FLOW, measures[KEY_FLOW]["EVAL_ERROR"], measures[KEY_FLOW]["MEAN_ERROR"], measures[KEY_FLOW]["STD_ERROR"]] 
    ]) 
    measures_data = pd.DataFrame(data, columns=headers)
    measures_data.to_csv(f'{path_to_output_folder}/measures.csv', index=True)

    plt.plot(df['Hour'], df["IRR"], "-b", label="Irr Real Data", linewidth=3)
    plt.plot(df['Hour'], full_predictions["IRR"], ".r", label="Predictions", markersize=1)
    plt.savefig(f'{path_to_output_folder}/irr_predictions.jpg')
    plt.legend()
    plt.close()

    plt.plot(df['Hour'], df["FLOW"], "-b", label="Flow Real Data", linewidth=3)
    plt.plot(df['Hour'], full_predictions["FLOW"], ".r", label="Predictions", markersize=1)
    plt.savefig(f'{path_to_output_folder}/flow_predictions.jpg')
    plt.legend()
    plt.close()


def print_output(inputs, evaluations, predictions):
    
    print ("{:<8} {:<15} {:<15} {:<15}".format('SENSOR', 'EVALUATION', 'PREDICTION', 'OFFSET'))

    for k in PREDICTION_KEYS:
        print ("{:<8} {:<15} {:<15} {:<15}".format( 
            k, 
            "FAILURE" if evaluations[0][k] else "FAULT FREE", 
            round(predictions[k][0], 3) if evaluations[0][k] else inputs[k][0],
            abs(round(predictions[k][0]-inputs[k][0], 3)) if evaluations[0][k] else "0" 
        ))


def process_sensors(irr, flow, tamb, tin, tout):

    inputs = {k: np.array([v]) for k, v in zip(KEYS, [irr, flow, tamb, tin, tout])}
    __exe__(inputs, verbose=True)  


if __name__ == '__main__':
    pass