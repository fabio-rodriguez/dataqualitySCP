# dataqualitySCP

This package consists of Fault Detection and Offset Prediction algorithms for values of sensors in a Solar Cooling Plant (SCP). These algorithms are based on neural networks and fuzzy logic techniques that use historical data of the SCP to extract knowledge.


## Installation process

The requirements.txt file must be installed using Python 3.8 version:

>$\> pip install -r requirements.txt

Then, the dataqualitySCP package must be installed: 

>$\> python setup.py install

## How to use

Fault Detection and Offset Prediction over sensors requiere a list of sensor values for an instant of time. The SCP sensor we consider are: Irradiance, Flow, Ambient Temperature, Inlet Temperature and Outlet Temperature. Then, the program will detect which sensor is faulty and will predict the correct value of the sensor, this way the Offset Error can be obtained. We assume that no more than one sensor fails at the same time.         

First, the installed package must be imported:

> \>\>\> import dataqualitySCP as dq

The algorithm receive two different kind of inputs:

1. A list of sensor values (Simple Prediction)

2. A path to a validation data file and a path to an output folder (Data Set Prediction)

### Simple Prediction

In the first case, the 'process_sensors' function must be called and the input values of sensors must be inserted. For example:

> \>\>\> dq.process_sensors(irr=300, flow=6, tamb=40, tin=120, tout=140)

Then, the program will print the Detection, Prediction and Offset per sensor.

Also, the prediction of simple inputs can be invoked directly like below:

>$\> python -m dataqualitySCP --simple-input-prediction --irr 300 --flow 6 --tamb 40 --tin 120 --tout 140 

### Data Set Prediction

In the second case, the program receives a path to a validation data set (.csv, .xlsx) in which are listed the sensor values for many time steps and a path to the output folder.

The validation data set must have for each sensor three columns: 

1. Real Value: Real value of the sensor in the instant of time 	
2. Input Value: Input value received by the algorithm (may be faulty)
3. Faulty Value: value in the set {0,1} that indicates wheter the input value is faulty (1) or not (0)

An example of the validation data set is given in 'data/validation_data.csv' file. 

To make predictions in the data set file the funcion 'process_dataset' is used:

> \>\>\> dq.process_dataset(path_to_output_folder="path/to/output/folder/", path_to_dataset="path/to/validation/data.csv")

Also, the data set prediction can be invoked directly like below:

>$\> python -m dataqualitySCP --data-set-prediction --data-set-root "PATH/TO/VALIDATION/DATA.csv" --outputs-path "PATH/TO/OUTPUT/FOLDER/"

Then, the program will retrieve the 'output.csv' file with the following information per sensor:

1. Real Value: Real value of the sensor in a specific instant of time 	
2. Input Value: Input value received by the algorithm (may be faulty)
3. Faulty Value: value in the set {0,1} that indicates wheter the input value is faulty (1) or not (0)
4. Detection Value: value in the set {0,1} that indicates wheter the input value is detected as faulty (1) or not (0)
5. Detection Value: The predicted value for the faulty sensor, if there is not fault detected, the value is the same as the input 
6. Detection Value: If a fault is detected, the offset between the input value and the predicted value

The algorithm will output images illustrating the Evaluation and Prediction process in sensors. Also, the algorithm outputs a file named 'measures.csv' with information about the precision of evaluation and the error of prediction per sensor. 

The corresponding output for the 'data/validation_data.csv' file is given in the 'outputs' folder of the project.

The algorithm process the 'data/validation_data.csv' file by default as follows:

>$\> python -m dataqualitySCP --default-validation --outputs-path "PATH/TO/OUTPUT/FOLDER/"
