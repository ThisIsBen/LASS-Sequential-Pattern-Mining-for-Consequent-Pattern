import os


def readDeviceIDFromFile(filename):
    with open(filename) as f_in:
        lines = filter(None, (line.rstrip() for line in f_in))
    return lines



def write2file(actualPM25DataList,SPMPredictionList,baseLinePredictionList,measurement,device_id,SPM_RMSE,baseLine_RMSE):



         
        

        # convert a list of lists to a list
        flattened_actualPM25DataList  = [val for sublist in actualPM25DataList for val in sublist]

        flattened_SPMPredictionList  = [val for sublist in SPMPredictionList for val in sublist]
        flattened_baseLinePredictionList  = [val for sublist in baseLinePredictionList for val in sublist]

        #if the device doesn't have the requested PM2.5 data,just skip it.
        if(len(flattened_actualPM25DataList)!=0):
                


                fp = open("./PattMinPredict_csv/"+measurement+"/"+device_id+".csv", "w+")
                fp.write("RMSE of SPM,RMSE of baseLine\n")
                fp.write(str(SPM_RMSE)+","+str(baseLine_RMSE)+"\n")
                fp.write( "No,ActualPM25Data,Sequential Pattern Mining Prediction,BaseLine Prediction\n");
                for PM25index in range(len(flattened_actualPM25DataList)):

                        fp.write( str(PM25index)+","+str(flattened_actualPM25DataList[PM25index])+","+str(flattened_SPMPredictionList[PM25index])+","+str(flattened_baseLinePredictionList[PM25index])+"\n");
                                                
                fp.close()