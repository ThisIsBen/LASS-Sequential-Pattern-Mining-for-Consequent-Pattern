def hillFunction(pattern_len):
	n=4
	
	Km=8
	weight = (pattern_len**n * 1.0 /( Km**n + pattern_len**n ))
	
	return weight
def getHillWeightList(lenList):
	weightList=[]
	
	
	for pattern_len in lenList:
		
		
		correspondingWeight=hillFunction(pattern_len)
		weightList.append(correspondingWeight)
		print("pattern_len={0} , corresponding_weight={1}".format(pattern_len,correspondingWeight))
	
	return weightList
def MultiplyHillFunWeight(dataset):
	
	lenList=dataset.keys()
	weightList=getHillWeightList(lenList)
	lengthCount=0
	for pattern_len, pattern_collectionDict in dataset.iteritems():
		
		for pattern, freq in pattern_collectionDict.iteritems():
			
			dataset[pattern_len][pattern]=freq*weightList[lengthCount]
			
		lengthCount=lengthCount+1
	
	
	return dataset
		

	
	
	
	