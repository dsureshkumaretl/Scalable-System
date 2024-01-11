def jaccard(a,b):
   return len(set(a).intersection(set(b)))/len(set(a).union(set(b)))


from itertools import combinations
import numpy as np
import ast
import csv
import json

input_files=[]
sig_bands=[]

with open("outputdir/output_k2.txt","r",encoding="utf-8") as file:
    
    row_recs = file.readlines()
    for row in row_recs:
        eof = row.find('.txt')
        bands_idx = row.find('][')
        filename = row[:eof]
        input_files.append(filename)
        bands = row(bands_idx)37
        bands = ast.literal_eval(bands)
        sig_bands.append(bands)
    for combination in combinations(range(len(input_files)),2):
        print("Comparing {} and {}.".format(input_files[combination[0]],input_files[combination[1]]))
        matches = 0
    for s1, s2 in zip(sig_bands[combination[0]], sig_bands[combination[1]]):
        if s1 == s2:
            matches += 1
            print(f"{s1} matches {s2}")
        print(f"{matches} matches found")
        if matches == 0:
            print("No matches found")
    
    for combination in combinations(range(len(input_files)), 2):
        print(f"Jaccard similarity for {input_files[combination[0]]} and {input_files[combination[1]]}.")
        shingle_similarity = jaccard(input_files[combination[0]],input_files[combination[1]])
        print(f"shingle:{shingle_similarity}\n")
    
 