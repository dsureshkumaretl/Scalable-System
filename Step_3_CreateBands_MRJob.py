#! /usr/bin/env python
#Step_3_CreateBands_MRJob.py

import string
import numpy as np
import ast
import random
from itertools import combinations
from mrjob.job import MRJob
from mrjob.step import MRStep
import gzip

#This job will read the vocabulary file generated in the previous step as gzip and generates bands accordingly
class Step_3_CreateBands_MRJob(MRJob):

	vocabulary = {}
	hashes = []


	def mapper_init(self):
		with gzip.open('bookvocab.txt.gz', 'rt') as f:
			text = f.read()
			text_index = text.find('{')
			vocabtext = text[text_index:]
			vocab = ast.literal_eval(vocabtext)
			self.vocabulary = dict(vocab)

	# mapper_raw passes whole text file through, instead of line by line
	def mapper_raw(self, file_path, uri):
		# ignore vocabulary file
		#if uri.startswith('/home/hduser/lsh/doc'):
		with open(file_path, "r") as f:
			text = " ".join(f.readlines())
			text = text.translate(
				str.maketrans(
					"",
					"",
					string.punctuation
				)
			)
			tokens = text.split()
			shingles = []
			k = 2
			for i in range(len(tokens) - k + 1):
				shingle = " ".join(tokens[i:i + k])
				if shingle not in shingles:
					shingles.append(shingle)
		#bit vectors
			bit_vector = [0]*len(self.vocabulary)
			for shingle in shingles:
				i = self.vocabulary[shingle]
				bit_vector[i] = 1

		yield uri, bit_vector


	def reducer_init(self):

		#vocabulary
		with gzip.open('bookvocab.txt.gz', 'rt') as f:
			text = f.read()
			text_index = text.find('{')
			vocabtext = text[text_index:]
			vocab = ast.literal_eval(vocabtext)
			self.vocabulary = dict(vocab)

		# create hashes
		def create_hash_function(hash_size):
			hash_func = list(range(1, hash_size+1))
			random.shuffle(hash_func)
			return hash_func

		def create_hash_functions(size, n_funcs):
			hashes = []
			for x in range(n_funcs):
				hash_function = create_hash_function(size)
				hashes.append(hash_function)
			return hashes

		self.hashes = create_hash_functions(len(self.vocabulary), 1000)



	def reducer(self, key, values):


		bit_vector = list(values)
		bit_vector = bit_vector[0]

		# creating signatures
		hash_signature = []
		for f in self.hashes:
			for i in range(1, len(bit_vector)+1):
				function_index = f.index(i)
				signature_val = bit_vector[function_index]
				if signature_val == 1:
					hash_signature.append(function_index)
					break

		# creating bands
		bands = []
		if len(hash_signature) % 250 != 0:
			print("the number of bands must divide equally into signature len")
		else:
			n_rows = int(len(hash_signature) / 250)
			for row in range(0, len(hash_signature), n_rows):
				bands.append(hash_signature[row : row+n_rows])


		yield key, bands


	def steps(self):
		return [MRStep(mapper_init = self.mapper_init, mapper_raw = self.mapper_raw, reducer_init = self.reducer_init, reducer = self.reducer)]


if __name__ == '__main__':
	Step_3_CreateBands_MRJob.run()
