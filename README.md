# Locality Sensitive Hashing

As the name suggests, this is a project on locality sensitive hashing. All of the information is contained in the notebook.

The sampledocs folder contains some books dataset for performing the document similarity task. It consists of news articles pulled from gutenberg website for academic purpose, with one document consisting of partial concatenations of the others. d.

The similarity task for vectors can easily generate synthetic data by just creating random matrices, so we do that in the notebook.

install the required libraries ,
pip install numpy,pandas,requests,bs4,string,csv,json,glob,mrjob,virtualenv

install the hadoop-3.3.4 using the instruction provided in the link ,
https://mymoodle.ncirl.ie/mod/resource/view.php?id=59065

Step 1 : Run the below code Step_1_ExtractDataSetJob.py using
python3 Step_1_ExtractDataSetJob.py
 
Step 2 : This will create books in the books folder , move it to the working dir
sudo mv /<wdir>/books/*.txt /<wdir>/

Step 3 : Next , we need to run the below job for generating the shingles , Step_2_Shingle_Vocab_MRJob

python3 Step_2_Shingle_Vocab_MRJob.py -r hadoop *.txt | gzip > bookvocab_k2.txt.gz

Step 4 : once the job2 in the previous step is completed then use the resulting file as input in the current job as shown below ,

python3 Step_3_CreateBands_MRJob.py -r hadoop --files <vocabfile>.txt.gz *.txt > output.txt

Step 5 : Run the below for generating the jaccard similarity , provided the output_<kvalue>.txt is generated from previous step ,

python3 Step_4_Jaccard_Similarity_Identifier.py


Step 6: USe the below notebook for visualization , LocalitySensitiveHashing.ipynb


Analyse the results and repeat for different values of k
