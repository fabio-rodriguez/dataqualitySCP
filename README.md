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

## Simple Prediction

In the first case, the 'process_sensors' function must be called and the input values of sensors must be inserted. For example:

> \>\>\> dq.process_sensors(irr=300, flow=6, tamb=40, tin=120, tout=140)\

Then, the program will print the Detection, Predictions and OFFSET per sensor.

Also, the prediction of simple inputs can be invoked directly like below:

>$\> python -m dataqualitySCP --simple-input-prediction --irr 300 --flow 6 --tamb 40 --tin 120 --tout 140 \

## Data Set Prediction

In the second case, the program receives a path to a validation data set (.csv, .xlsx) in which are listed the sensor values for many time steps and a path to the ouputs folder.

The validation data set must have for each sensor three columns: 

1. Real Value: Real value of the sensor in the instant of time 	
2. Input Value: Input value received by the algorithm (may be faulty)
3. Faulty Value: {0,1} values that indicate wheter the input value is faulty (1) or not (0)

An example of the validation data set is given in 'data/validation_data.csv' file. 

To make predictions in the data set file the funcion 'process_dataset' is used:

> \>\>\> dq.process_dataset(path_to_output_folder="PATH/TO/OUTPUT/FOLDER/", path_to_dataset="PATH/TO/VALIDATION/DATA.csv")\

Also, the data set prediction can be invoked directly like below:

>$\> python -m dataqualitySCP --data-set-prediction --data-set-root "PATH/TO/VALIDATION/DATA.csv" --outputs-path "PATH/TO/OUTPUT/FOLDER/"

Then, the program will output the 'output.csv' file with the following information per sensor:

1. Real Value: Real value of the sensor in the instant of time 	
2. Input Value: Input value received by the algorithm (may be faulty)
3. Faulty Value: {0,1} values that indicate wheter the input value is faulty (1) or not (0)
4. Detection Value: {0,1} values that indicate wheter the input value is detected as faulty (1) or not (0)
5. Detection Value: The predicted value for the faulty sensor, if there is not fault detected, the value is the same of the input 
6. Detection Value: If a fault is detected, the offset between the input value and the predicted value

For each sensor the algorithm will output an image illustrating the Evaluation and Prediction precess. Also, the algorithm aouputs a file named 'measures.csv' with information about the precision of evaluation and the error of prediction per sensor. 

The corresponding output for the 'validation_data.csv' data set is given in the 'outputs' folder in the project.

The algorithm can be run for the default data set as follow:

>$\> python -m dataqualitySCP --default-validation --outputs-path "PATH/TO/OUTPUT/FOLDER/"