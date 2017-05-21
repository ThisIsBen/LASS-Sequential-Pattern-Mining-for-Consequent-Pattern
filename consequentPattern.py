def genCandidate(pattern_count, len, element):
	gen = []
	'''
	print("Use pattern in the last iteration, with the element can be extend" \
		"to gen the cadicate")
	'''
	#print(len, "sagashimashou from", pattern_count )

	for x in pattern_count.keys():
		for y in element:
			if y[1] == 1:
				gen.append(x+y[0])
	#print(gen)
	return gen
def pattern_mining(dataset, element, threshold):
	cur_pattern_len = 1
	flag = 1
	found_pattern = { }
	
	while flag == 1:
		# how to gen a candidate list?? (by found pattern in last round)
		### decide the candidate pattern to matching
		if found_pattern == { }:
			candidate = [x[0] for x in element]
			#print (candidate)
		else:
			candidate = genCandidate(pattern_count, cur_pattern_len, element)
			#print("haah")


		pattern_count = { }
		for c in candidate:
			pattern_count[c] = 0
		#print(pattern_count)

		### scan dataset to matching
		for x in dataset:
			#print(x)
			for c in candidate:

				if c in x:
					pattern_count[c] += 1
					
		#print(pattern_count)


		# pruning
		for k in pattern_count.keys():
			if  pattern_count[k] < threshold:
				#print(k, pattern_count[k])
				del pattern_count[k]
				
				for e in element:
					# these element are not enough, so not need to extend
					if e[0] == k:
						e[1] = 0
						#print(e)

		### append newly found pattern, pattern length++
		#print("after pruning: ", pattern_count)
		if pattern_count == { }:
			flag = 0
			print("can't extend anymore", cur_pattern_len)
			#print(candidate)
		# found_pattern.update(pattern_count)
		found_pattern[cur_pattern_len] = pattern_count
		cur_pattern_len += 1
	# print(found_pattern)
	return found_pattern