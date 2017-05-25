# LASS-Sequential-Pattern-Mining-for-Consequent-Pattern

# Input
You should create two text files named "airboxDeviceID.txt" and "lassDeviceID.txt" in advance,which list all the PM2.5 Device ID line by line in it.
e.g.,
```
  28C2DDDD479C
  28C2DDDD479F
  ...
```
# Execution
```
  python SeqPattMin.py
```

# Ouput 
The program will read in all the PM2.5 Device ID from two text files named "airboxDeviceID.txt" and "lassDeviceID.txt" ,and then create a folder named "PattMinPredict_csv" . In that folder ,there will be two folders "airbox" and "lass",whcih contains the Sequential Pattern Mining Prediction result and the baseLine Prediction result in CSV file format of each device that are listed in "airboxDeviceID.txt" and "lassDeviceID.txt" respectively.

# Notice 
The program won't ouput the csv file for the devices which don't have sufficient data required for the prediction process.  In other words,those  devices will be skipped automatically by the program.
