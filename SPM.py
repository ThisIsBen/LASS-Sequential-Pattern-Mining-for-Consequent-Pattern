#!/usr/bin/python3
'''
_msg_monitors = """
air monitors in Tainan City: (id)
				airbox
								74DA38AF489E
								74DA38AF487A
								74DA38AF4842
								74DA38AF482E
								74DA38AF4812
								74DA38AF479A
								74DA3895E068
								74DA3895E04C
								74DA3895DFF6
								74DA3895C39E
								74DA388FF4F8
								28C2DDDD479F
								28C2DDDD479C
								28C2DDDD415F
				lass
								YK_160
								FT1_CCH01
"""

'''

from influxdb import InfluxDBClient

#from prefixspan import frequent_rec,topk_rec


import sys
from collections import defaultdict
from heapq import heappop, heappush
import operator
#from consequentPattern import pattern_mining,genCandidate
import consequentPattern
import HillFunction

db=[]
#init predict pivot
PM25InNoList=[]

'''
adjustable var for different prediction time interval
'''
dataAmountPerTimeUnit=12
pastHours=24
predictionLengthInHour=1

predictionDate="'2017-05-19'"
'''
#get the past 24 hours data from present
predictionDate="now()"
'''

#min_support for Sequential Pattern Mining
min_support = 2
def query_interval_by_device_id(client, measurement='', device_id='', late_time='now()', duration='1h'):
				# return type: Raw JSON from InfluxDB
				#print(late_time)
				early_time = late_time + ' - '  + duration
				#print(early_time)
				#if(early_time=='now() - 0h - 1h'):
				#	str_query = 'select "PM2.5" from ' + measurement + ' where "Device_id" = \'' + device_id + '\' and time <= now() and time > now() - 1h' 
				#else:
				str_query = 'select "PM2.5" from ' + measurement + ' where "Device_id" = \'' + device_id + '\' and time <= ' + late_time + ' and time > ' + early_time
				print(str_query)
				return client.query(str_query).raw

def get_pm25s_from_query(json={}):
				# return type: list
				ret = []
				for value in json['series'][0]['values']:
								#print(value[1])
								ret.append(value[1])
				#get the latest PM2.5 Data value
				#if(predictPivot=="0"):								
					#predictPivot=ret[len(ret)-1]

				PM25InNoList.append(ret)
				return ret

def pm25_to_pattern(pm25=0):
				# return type: str
				_pm25_levels = [11, 23, 35, 41, 47, 53, 58, 64, 70]
				_patterns =    ['a','b','c','d','e','f','g','h','i','j']
				for i in range(0, len(_pm25_levels)):
								
								if pm25 <= _pm25_levels[i] :
												return _patterns[i]+' '
								elif pm25>_pm25_levels[len(_pm25_levels)-1]:
												return _patterns[len(_patterns)-1]+' '

				return _patterns[len(_pm25_levels)]

def pm25s_to_patterns(pm25s=[]):
				# return type: list
				ret = []
				for pm25 in pm25s:
								ret.append(pm25_to_pattern(pm25))
				return ret


def predictPM25Level(predictionRef=[],predictionCandidateDic={}):
				
				for(patt,probability) in predictionRef:
								if( patt[len(patt)-1] not in predictionCandidateDic ):
												predictionCandidateDic[patt[len(patt)-1]] = 0
								predictionCandidateDic[patt[len(patt)-1]]=predictionCandidateDic[patt[len(patt)-1]]+probability
				
				#print("predictionCandidateDic : {}".format(predictionCandidateDic))


				maxFreq=0
				predictionResult=' '
				for  pattRef,freqRef in predictionCandidateDic.iteritems():
				
								if(freqRef>maxFreq):
												maxFreq=freqRef
												predictionResult=pattRef

				return predictionResult

def Level2PM25No (predictLevel,candidatePM25Level={}):
				_pm25_levels = [11, 23, 35, 41, 47, 53, 58, 64, 70]#suppose j means PM2.5<100

				#set PM25 Prediction Value base
				PM25PredictionValue=PM25InNoList[0][-1]
				

				
					

				
				for PM25Level, prob in candidatePM25Level.iteritems():
				# return type: str
					if(PM25Level!=predictLevel):


						#suppose j means 100
						if(PM25Level=='j'):
							PM25PredictionValue+=100*prob*0.01
							
						elif(ord(PM25Level)-97-1>=0):
							if(PM25Level>predictLevel):
								PM25PredictionValue+=((_pm25_levels[ord(PM25Level)-97]+_pm25_levels[ord(PM25Level)-97-1])/2)*prob*0.01
							else:
								PM25PredictionValue-=((_pm25_levels[ord(PM25Level)-97]+_pm25_levels[ord(PM25Level)-97-1])/2)*prob*0.01
						
						
						#if it's 'a':(11+0)/2*prob
						else:
							PM25PredictionValue-=((_pm25_levels[0]+0)/2)*prob*0.01
				
				#rounding
				PM25PredictionValue=int(PM25PredictionValue+0.55)
				return PM25PredictionValue


def SPMPrediction(actualPM25DataList=[],SPMtempList=[],measurement="airbox",device_id="0"):
				
				
			
				client = InfluxDBClient(host='127.0.0.1', port=8086, database='PM25')
				#prefixSpanCmd=raw_input( 'Please enter (frequent | top-k) <threshold>').split()

				#get PM2.5 data from the selected airbox device
				
				print('measurement = {0}, device_id = {1}'.format(measurement, device_id))
				print('') # new line

				#get the actual PM25 data from the past 1st to 24th hour of a certain time.
				for h in range(0,pastHours):#get data from the past 1st to 24th hour
								try:			
												#get the past 24 hours data from '2017-05-19'
												result = query_interval_by_device_id(client, measurement, device_id, predictionDate+" - " + str(h) + 'h' ,'1h')
												
												'''
												#get the past 24 hours data from present
												result = query_interval_by_device_id(client, measurement, device_id, "now() - " + str(h) + 'h' ,'1h')
												'''


												get_pm25s_from_query(result)
												
												
																
												
												
				


							
				
												



								except:
												print('[debug] There may be no result in this query.')
												print('[debug]   measurement = {0}, device_id = {1}, h = {2}'.format(measurement, device_id,h))
				#copy the content of PM25InNoList
				actualPM25DataList=list(PM25InNoList)
				
				
				'''
				db = [
								[0, 1, 2, 3, 4],
								[1, 1, 1, 3, 4],
								[2, 1, 2, 2, 0],
								[1, 1, 1, 2, 2],
				]
				'''
							
				'''

				db = [
								['a',('a','b','c'),('a','c'),'d',('c','f')],
								[('a','d'),'c',('b','c'),('a','e')],
								[('e','f'),('a','b'),('d','f'),'c','b'],
								['e','g',('a','f'),'c','b','c'],
				]
				'''
				for pastMinutes in range(predictionLengthInHour*60, 0, -5):

					#clear db and PM25InNoList for next 5 mins prediction.
					


					#get the data from the past 1st to 24th hour of a cetain time for CPM adn baseline prediction.
					for h in range(0,pastHours):#get data from the past 1st to 24th hour
									try:			
													#get the past 24 hours data from '2017-05-19'
													result = query_interval_by_device_id(client, measurement, device_id, predictionDate+" - " + str(h) + 'h - '+str(pastMinutes)+'m' ,'1h')
													
													


													patternList=(''.join(pm25s_to_patterns(get_pm25s_from_query(result)))).split()
													
													
																	
													
													db.append(patternList)
					


								
					
													



									except:
													print('[debug] There may be no result in this query.')
													print('[debug]   measurement = {0}, device_id = {1}, h = {2}'.format(measurement, device_id,h))



					formatDB=[]
					tempStr=""
					k=len(db)
					#print("@@@@@@@@@@")
					#print(k)

					#if not all data in each past hours is successfully retrieved
					retrievedHours=k
					if(k<pastHours):		
						k=pastHours
						

					for i in range(0,len(db)):
									#print(" ")
									#print ("PM2.5 level in the {}th hour in the past".format(k))
									#print (db[retrievedHours-1])
									retrievedHours=retrievedHours-1
									k=k-1
									tempStr = ''.join(db[retrievedHours])

									formatDB.append(tempStr)
									tempStr=""
					
					

					

					element = [['a', 1], 
																['b', 1],
																['c', 1],
																['d', 1],
																['e', 1], 
																['f', 1], 
																['g', 1], 
																['h', 1],
																['i', 1],
																['j', 1]
													]
													#minimum support=2
					
					patternLenDict = consequentPattern.pattern_mining(formatDB, element, min_support)
					del patternLenDict[1] # remove  entry with key 'Length ==1' becuase it's meaningless for sequential pattern mining app
					if(len(patternLenDict)>=dataAmountPerTimeUnit+2):
						del patternLenDict[dataAmountPerTimeUnit+1]# remove  entry with key 'Length ==1' becuase it's meaningless for sequential pattern mining app
					#print(patternLenDict)
					#print (formatDB)
					dataset_weight_applied=HillFunction.MultiplyHillFunWeight(patternLenDict)
					#print ("dataset with weight applied={0}".format(dataset_weight_applied))
					
					#sort the freq of each pattern after weight applied.
					sorted_dataset={}
					lenCount=2
					for pattern_len, pattern_collectionDict in dataset_weight_applied.iteritems():	
						for pattern, freq in pattern_collectionDict.iteritems():			
							sorted_set = sorted(dataset_weight_applied[pattern_len].items(), key=operator.itemgetter(1))
							sorted_set.reverse()
						sorted_dataset[lenCount]=sorted_set
						lenCount=lenCount+1

					#print ("After sorting= {0}".format(sorted_dataset))

					#print (" ")#/n


					
					#get referech string from the most recent 12 PM2.5 data of the device.
					lenFormatDB=len(formatDB)

					#if We currently can't get any data from this device of the past 24 hours on the date specified by programmer.
					#just skip this device
					if(lenFormatDB==0):
						return -1,-1
					referenceString=formatDB[lenFormatDB-1]
					i=2
					while len(referenceString)<dataAmountPerTimeUnit:
							referenceString=formatDB[lenFormatDB-i]+referenceString
							
							i=i+1
					
					#print(referenceString)


					#compare the most matched pattern of each length
					candidatePredictionPattDict={}
					cur_len=2
					for pattern_len, pattern_collectionDict in sorted_dataset.iteritems():	
						for i in range(0,len(sorted_dataset[pattern_len])):
							#print(sorted_dataset[pattern_len][i])
							#print("foundPatt    ={0}".format(sorted_dataset[pattern_len][i][0]))

							comparedString=""
							for j in range(0,cur_len-1):
								comparedString+=sorted_dataset[pattern_len][i][0][j]
							#print("comparedPatt ={0}".format(comparedString))
							#print("referencePatt={0}".format(referenceString[-len(comparedString):]))
							
							if(comparedString==referenceString[-len(comparedString):]):
								#print("~~~~Pattern matched!!~~~~~")
								candidatePredictionPattDict[sorted_dataset[pattern_len][i][0]]=sorted_dataset[pattern_len][i][1]
							#print("")#\n
						cur_len=cur_len+1
					
					#sort the candidatePredictionPatt
					sorted_candidatePredictionPattDict = sorted(candidatePredictionPattDict.items(), key=operator.itemgetter(1))
					sorted_candidatePredictionPattDict.reverse()
					#print("candidatePredictionPatts of Device :{0}  is  {1}".format(device_id,sorted_candidatePredictionPattDict))
					#print ("The prediction PM2.5 level in the next 5 mins is : {}".format(predictLevel))

					#check if the candidatePredictionPattDict is empty or not.
					'''
					if(bool(candidatePredictionPattDict) ):
					'''
					predictionCandidateDic={}
					predictLevel=predictPM25Level(sorted_candidatePredictionPattDict,predictionCandidateDic)
					#print ("The prediction PM2.5 level in the next 5 mins is : {}".format(predictLevel))


					predictLevelInNo=Level2PM25No (predictLevel,predictionCandidateDic)
					print ("The prediction PM2.5 level in number of the next 5 mins is : {}".format(predictLevelInNo))
					SPMtempList.append(predictLevelInNo)

					#print("The latest PM2.5 data in the 2nd hour from now = {}".format(PM25InNoList[1]))
					#print("The latest PM2.5 data in the 1st hour from now = {}".format(PM25InNoList[0]))
					
					#clear these list for next use.
					del db[:]
					del PM25InNoList[:]
				
				return actualPM25DataList,SPMtempList




				'''
				#to keep prediction reference
				predictionRef=[]
				#print out GSP result

				print ("The last datum is : {}".format(predictPivot))
				for (freq, patt) in results:
								#print out only the patterns that have 2<=length<=6,
								#have the latest data involved .        
							
								if( len(patt)>=2 and len(patt)<=6 and  predictPivot in patt ):
												if(patt.count(predictPivot)>1 or patt[len(patt)-1]!=predictPivot):
																print("{}: {}".format(patt, freq))

																#add reference for prediction to a list
																predictionRef.append((freq, patt))



				#predict PM2.5 level in the next 5 mins
				predictLevel=predictPM25Level(predictionRef)
				print ("The prediction PM2.5 level in the next 5 mins is : {}".format(predictLevel))
				'''








			

			