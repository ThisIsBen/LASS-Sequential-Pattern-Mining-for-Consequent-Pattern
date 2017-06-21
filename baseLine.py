

import sys

dataAmountPerTimeUnit=12

def getbaselinePrediction(actualPM25DataList=[],baseLinetempList=[]):
	#get the last data of 23th hour to generate baseline prediction
	baseLinetempList.append(actualPM25DataList[-2][-1])
	for i in range(0,dataAmountPerTimeUnit-1):
		try:
			baseLinetempList.append(actualPM25DataList[-1][i])
		except:
			return -1
	return baseLinetempList
