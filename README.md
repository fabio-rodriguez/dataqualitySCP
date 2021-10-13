# dataqualitySCP

This is a project for Fault Detection and Offset Prediction of sensor values in a Solar Cooling Plant (SCP). The Fault Detection and Offset Prediction processes are based in neural networks and fuzzy logic.


# Installation process

The requirements.txt file must be installing (Python 3.8):

>$\> pip install -r requirements.txt

Then, the dataqualitySCP package must be installed: 

>$\> python setup.py install

# How to use

The Fault Detection and Offset Prediction over sensors of the is a process with many steps. First a llist sensor values for an instant of time must be given: Irradiance, Flow, Ambient Temperature, Inlet Temperature and Outlet Temperature. Then, the program will detect which sensor is faulty and predicts the correct value for the sensor, so it predicts the Offset Error of the sensor.        

In this initial release of the project just the prediction part is integrated. So the program, given the list of sensor inputs will predict the correct value of each sensor and the Offset Error in each case.

First the installed package must be imported:

> \>\>\> import dataqualitySCP as dq

To test the package the \__exe__ function must be called and the sensors input values must be manually inserted. For example:

> \>\>\> dq.\__exe__()\
> Irradiance: 300\
> Flow: 12\
> Ambient Temperature: 30\
> Inlet Temperature: 150\
> Outlet Temperature: 160

Then, the program will print the Predictions and the Errors.


