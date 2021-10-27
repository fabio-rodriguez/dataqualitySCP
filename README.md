# dataqualitySCP

This package consists in a Fault Detection and Value Prediction algorithms for sensor values in a Solar Cooling Plant (SCP). These algorithms are based on neural networks and fuzzy logic techniques that use historical data of the plant extract knowledge.


# Installation process

The requirements.txt file must be installing (Python 3.8):

>$\> pip install -r requirements.txt

Then, the dataqualitySCP package must be installed: 

>$\> python setup.py install

# How to use

For Fault Detection and Value Prediction over sensors requiere a list of sensor values for an instant of time: Irradiance, Flow, Ambient Temperature, Inlet Temperature and Outlet Temperature. Then, the program will detect which sensor is faulty and will predict the correct value of the sensor, this way the Offset Error of the sensor can be obtained.        

First, the installed package must be imported:

> \>\>\> import dataqualitySCP as dq

The algorithm receive two different kind of inputs:

1. List of values for each sensor (Simple Prediction)

2. One path to a data set file and one path to an output folder (Data Set Prediction)

In the first case, the 'process_sensors' function must be called and the input values of sensors must be inserted. For example:

> \>\>\> dq.process_sensors(irr=300, flow=6, tamb=40, tin=120, tout=140)\

Then, the program will print the Detection, Predictions and OFFSET per sensor.

In the second case,


Example of the possible input values for sensors are given in the 'data' folder.
