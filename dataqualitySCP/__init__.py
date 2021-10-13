
from multiprocessing import Process, Queue

from .prediction import *


def read_inputs():
    '''Function for reading the input data'''

    irr = float(input("Irradiance: "))
    flow = float(input("Flow: "))
    tamb = float(input("Ambient Temperature: "))
    tin = float(input("Inlet Temperature: "))
    tout = float(input("Outlet Temperature: "))

    values = [irr, flow, tamb, tin, tout]

    return {k: v for k, v in zip(keys, values)}


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


if __name__ == '__main__':
    
    __exe__()    