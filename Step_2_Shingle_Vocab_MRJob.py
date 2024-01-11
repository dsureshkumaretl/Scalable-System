#! /usr/bin/env python
#! /usr/bin/env python3
# Step_2_Shingle_Vocab_MRJob.py

import string
import numpy as np
from mrjob.job import MRJob

#This class will be the job which reads the file and produces vocabulary after comparision

class Step_2_Shingle_Vocab_MRJob(MRJob):
	# mapper_raw passes whole text file through, instead of line by line
	def mapper_raw(self, file_path, uri):
		with open(file_path, "r") as f:
			text = " ".join(f.readlines())
			text = text.translate(
				str.maketrans(
					"",
					"",
					string.punctuation
				)
			)
			tokens = text.split() # picking all the individual words in the file
			shingles = []
			k = 2 #this can be varied across each time to get the varied bands for comparative analysis
			for i in range(len(tokens) - k + 1):
				shingle = " ".join(tokens[i:i + k])
				if shingle not in shingles:
					shingles.append(shingle)
		yield 1, shingles


	def reducer(self, key, shingles):
		shingle_set = []
		for i in shingles:
			shingle_set.append(i)
		all_shingles = {item for shingles in shingle_set for item in shingles}
		vocabulary = {}
		for i, shingle in enumerate(list(all_shingles)):
			vocabulary[shingle] = i
		yield key, vocabulary


if __name__ == '__main__':
	Step_2_Shingle_Vocab_MRJob.run()