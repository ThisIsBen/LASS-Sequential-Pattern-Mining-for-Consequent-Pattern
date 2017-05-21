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
import WriteCSV

if __name__ == "__main__":
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
	actualPM25DataList,SPMtempList,measurement,device_id=SPM.SPMPrediction(actualPM25DataList,SPMtempList)

	#reverse actualPM25DataList to old-->new 
	actualPM25DataList=actualPM25DataList[::-1]
	print("in SeqPattMin {}".format(actualPM25DataList))
	print("in SPMtempList SPMp {}".format(SPMtempList))



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
	print("in SeqPattMin SPMp {}".format(SPMPredictionList))
	print("in SeqPattMin base {}".format(baseLinePredictionList))
	print("in baseLinetempList SPMp {}".format(baseLinetempList))


	WriteCSV.write2file(actualPM25DataList,SPMPredictionList,baseLinePredictionList,measurement,device_id)