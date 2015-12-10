###Text Classification of Political Blogs<br />
Task: given the training data of political blogs, predict the political opinion of each blog in the test data (left-leaning or right-leaning)<br />
Datasets: Training/left:3184,right:3256   Test/left:399,right:407<br />
Model: Maximum Entropy(using Mallet)<br />
Features: F1-unigram:rawFreq_in_doc, F2-bigram:rawFreq_in_doc, F3-trigram:rawFreq_in_doc,<br />
          F4-count of party members(extracted from an external source) in a doc divided by total word count in a doc<br />
          F5-count of party keywords(extracted from an external source) in a doc divided by total word count in a doc<br />
          F6-for all ngrams used as features, replace the rawFreq with 0.5+0.5*rawFreq/maxFreq_in_doc to avoid bias towards longer docs<br />
Baseline(test accuracy): F1 only - 93.6725%<br />
Results:                 F1+F2   - 94.7891%<br />
                         F1+F3   - 93.6725%<br />
                         F1+F4   - 93.7965%<br />
                         F1+F5   - 94.0447%<br />
                         F1+F6   - 94.2928%<br />
                best at F1+F2+F6 - 96.0298%<br />
                
###File Structure<br />
./data/       contains sample training and test dir, external source data extracted from webpages<br />
./scraper/    contains python scripts for extracting information from webpages<br />
./expt/       contains sample program output files (training/test vector files and MaxEnt classification results)<br />
./train_classiry.sh   the wrapper for creating feature vectors, running the classifier and writing results<br />
./create_vectors.sh   the shell script to invoke create_vectors.py<br />
./create_vectors.py   create feature vectors for all files under given dir<br />
./proc_file.sh        the shell script to invoke create_vectors.py with option '-f' to process a single input doc<br />
./proc_file.py        called by create_vectors.py to process an individual file<br />

###Usage
1. to process a single file, output the feature vectors to a give file:<br />
  ./proc_file.sh input_file targetLabel output_file<br />
2. to process all files under multiple dirs, output the feature vectors to a given file:<br />
  ./create_vectors.sh output_vector_file dir1 dir2 ... dir_n<br />
3. to create feature vectors for all the training and test data, run the classifier and output all the intermediate and resultative files to a given dir:<br />
  ./train_classify.sh param_file train_dir test_dir output_dir<br />

