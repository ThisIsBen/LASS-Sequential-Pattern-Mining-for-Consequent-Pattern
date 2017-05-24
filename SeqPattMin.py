from influxdb import InfluxDBClient

#from prefixspan import frequent_rec,topk_rec


import sys
from collections import defaultdict
from heapq import heappop, heappush
import operator
#from consequentPattern import pattern_mining,genCandidate
import consequentPattern
import HillFunction
import SPM
import baseLine
import RWFile

import os
import shutil


import numpy as np
#open a file for each airbox and write each data of the airbox to that file
if not os.path.exists("./PattMinPredict_csv"):
        os.makedirs("./PattMinPredict_csv")
if not os.path.exists("./PattMinPredict_csv/lass"):
        os.makedirs("./PattMinPredict_csv/lass")
if not os.path.exists("./PattMinPredict_csv/airbox"):
        os.makedirs("./PattMinPredict_csv/airbox")


#if the folder already exsits , delete it and recreate it to avoid retainning outdated files.
if os.path.exists("./PattMinPredict_csv/airbox"):
        shutil.rmtree('./PattMinPredict_csv/airbox')
        os.makedirs("./PattMinPredict_csv/airbox")


#if the folder already exsits , delete it and recreate it to avoid retainning outdated files.
if os.path.exists("./PattMinPredict_csv/lass"):
        shutil.rmtree('./PattMinPredict_csv/lass')
        os.makedirs("./PattMinPredict_csv/lass")

'''
adjustable var
'''
dataAmountPerTimeUnit=12



def SeqPattMin_and_baseLine(measurement,device_id):
		actualPM25DataList=[]
		SPMPredictionList=[]
		baseLinePredictionList=[]
		SPMtempList=[]
		baseLinetempList=[]
		'''
		Step 1 loop H:0~24
		select "PM2.5" from airbox where "Device_id" = '28C2DDDD479C' and time <=  '2017-05-19'   - Hh   and time >'2017-05-19' - Hh - 1h
		Generate actual PM25 data List
		'''
		actualPM25DataList,SPMtempList=SPM.SPMPrediction(actualPM25DataList,SPMtempList,measurement,device_id)
		#if We currently can't get any data from this device of the past 24 hours on the date specified by programmer.
		#just skip that device.
		if (actualPM25DataList==-1):
			print("We currently can't get any data from this device of the past 24 hours on the date specified by programmer. ")
			return

		#reverse actualPM25DataList to old-->new 
		actualPM25DataList=actualPM25DataList[::-1]
		#print("in SeqPattMin {}".format(actualPM25DataList))
		#print("in SPMtempList SPMp {}".format(SPMtempList))



		'''

		Step 2 Init SPMPredictionList and baseLinePredictionList



		'''
		SPMPredictionList=list(actualPM25DataList)
		SPMPredictionList.pop()
		SPMPredictionList.append(SPMtempList)
		baseLinePredictionList=list(actualPM25DataList)
		baseLinePredictionList.pop()
		baseLinetempList=baseLine.getbaselinePrediction(actualPM25DataList,baseLinetempList)
		baseLinePredictionList.append(baseLinetempList)
		#print("in SeqPattMin SPMp {}".format(SPMPredictionList))
		#print("in SeqPattMin base {}".format(baseLinePredictionList))
		#print("in baseLinetempList SPMp {}".format(baseLinetempList))

		#cal RMSE of SPM and baseLine prediction
		SPM_RMSE,baseLine_RMSE=getRMSE(actualPM25DataList,SPMtempList,baseLinetempList)

		RWFile.write2file(actualPM25DataList,SPMPredictionList,baseLinePredictionList,measurement,device_id,SPM_RMSE,baseLine_RMSE)
		'''
		del actualPM25DataList[:]
		del SPMPredictionList[:]
		del baseLinePredictionList[:]
		del SPMtempList[:]
		del baseLinetempList[:]
		'''

def calRMSE(predictions, targets):
	return np.sqrt(((predictions - targets) ** 2).mean())


def getRMSE(actualPM25DataList,SPMtempList,baseLinetempList):
	
	#to contain the last dataAmountPerTimeUnit PM2.5 data
	actual=[]

	# convert a list of lists to a list
	flattened_actualPM25DataList  = [val for sublist in actualPM25DataList for val in sublist]
	for i in range(-1*dataAmountPerTimeUnit,0):
		actual.append(flattened_actualPM25DataList[i])
	SPM_RMSE=calRMSE(np.array(SPMtempList),np.array(actual))
	baseLine_RMSE=calRMSE(np.array(baseLinetempList),np.array(actual))

	return SPM_RMSE,baseLine_RMSE




if __name__ == "__main__":
	
	airbox_devices=[]
	lass_devices=[]
	airbox_devices=RWFile.readDeviceIDFromFile("./airboxDeviceID.txt")
	lass_devices=RWFile.readDeviceIDFromFile("./lassDeviceID.txt")

	
	
	for device_id in airbox_devices :
		SeqPattMin_and_baseLine("airbox",device_id)

	for device_id in lass_devices :
		SeqPattMin_and_baseLine("lass",device_id)