
from multiprocessing import Process, Queue

from constants import *
from prediction import predict
from evaluation import evaluate


def read_inputs():
    '''Function for reading the input data'''

    irr = float(input("Irradiance: "))
    flow = float(input("Flow: "))
    tamb = float(input("Ambient Temperature: "))
    tin = float(input("Inlet Temperature: "))
    tout = float(input("Outlet Temperature: "))

    values = [irr, flow, tamb, tin, tout]

    return {k: v for k, v in zip(KEYS, values)}


def __exe__():

    evaluate({k: v for k, v in zip(KEYS, [100,10,30,100,120])}, None)
    
    input = read_inputs()

    l1 = Queue()
    p1 = Process(target=predict, args=(input, l1, ))  
    l2 = Queue()
    p2 = Process(target=evaluate, args=(input, l2, )) 
    p1.start()   
    p2.start()     
    
    predictions, errors = l1.get()
    evaluations = l2.get()
    print_output(evaluations, predictions, errors) 


def print_output(evaluations, predictions, errors):
    
    print ("{:<8} {:<15} {:<15} {:<10}".format('SENSOR', 'FAULT FREE', 'PREDICTION','ERROR'))

    for k in PREDICTION_KEYS:
        print ("{:<8} {:<15} {:<15} {:<10}".format( 
            k, 
            "NO" if evaluations[k] else "YES", 
            str(round(predictions[k][0], 3)), 
            str(round(errors[k], 3))
        ))


if __name__ == '__main__':
    
    __exe__()    