import os
import shutil
#open a file for each airbox and write each data of the airbox to that file
if not os.path.exists("./PattMinPredict_csv"):
        os.makedirs("./PattMinPredict_csv")
if not os.path.exists("./PattMinPredict_csv/lass"):
        os.makedirs("./PattMinPredict_csv/lass")
if not os.path.exists("./PattMinPredict_csv/airbox"):
        os.makedirs("./PattMinPredict_csv/airbox")


def write2file(actualPM25DataList,SPMPredictionList,baseLinePredictionList,measurement,device_id):



         
        if measurement=='airbox':
            #if the folder already exsits , delete it and recreate it to avoid retainning outdated files.
            if os.path.exists("./PattMinPredict_csv/airbox"):
                    shutil.rmtree('./PattMinPredict_csv/airbox')
                    os.makedirs("./PattMinPredict_csv/airbox")

        if measurement=='lass':
        #if the folder already exsits , delete it and recreate it to avoid retainning outdated files.
            if os.path.exists("./PattMinPredict_csv/lass"):
                    shutil.rmtree('./PattMinPredict_csv/lass')
                    os.makedirs("./PattMinPredict_csv/lass")

        # convert a list of lists to a list
        flattened_actualPM25DataList  = [val for sublist in actualPM25DataList for val in sublist]

        flattened_SPMPredictionList  = [val for sublist in SPMPredictionList for val in sublist]
        flattened_baseLinePredictionList  = [val for sublist in baseLinePredictionList for val in sublist]
        
        #if the device doesn't have the requested PM2.5 data,just skip it.
        if(len(flattened_actualPM25DataList)!=0):
                


                fp = open("./PattMinPredict_csv/"+measurement+"/"+device_id+".csv", "w+")
                for PM25index in range(len(flattened_actualPM25DataList)):

                        fp.write( str(PM25index)+","+str(flattened_actualPM25DataList[PM25index])+","+str(flattened_SPMPredictionList[PM25index])+","+str(flattened_baseLinePredictionList[PM25index])+"\n");
                                                
                fp.close()