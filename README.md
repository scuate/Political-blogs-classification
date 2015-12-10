#####Text Classification of Political Blogs<br />
<b>Task</b>:   given the training data of political blogs, predict the political opinion of each blog in the test data (left-leaning or right-leaning)<br />
<b>Datasets</b>:   Training/left:3184,right:3256   Test/left:399,right:407<br />
<b>Model</b>:   Maximum Entropy(using Mallet)<br />
<b>Features</b>:   
            F1-unigram:rawFreq_in_doc <br />
            F2-bigram:rawFreq_in_doc <br />
            F3-trigram:rawFreq_in_doc<br />
            F4-count of party members(extracted from an external source) in a doc divided by total word count in a doc<br />
            F5-count of party keywords(extracted from an external source) in a doc divided by total word count in a doc<br />
            F6-for all ngrams used as features, replace the rawFreq with 0.5+0.5*rawFreq/maxFreq_in_doc to avoid bias towards longer docs<br />
<b>Baseline(of test accuracy)</b>:       
F1 only - 93.6725%<br />
<b>Results</b>:              
F1+F2   - 94.7891%<br />
F1+F3   - 93.6725%<br />
F1+F4   - 93.7965%<br />
F1+F5   - 94.0447%<br />
F1+F6   - 94.2928%<br />
F1+F2+F6 - 96.0298% -> best result <br />
                
#####File Structure<br />
<b>./data/</b>                contains sample training and test dir, external source data extracted from webpages<br />
<b>./scraper/</b>            contains python scripts for extracting information from webpages<br />
<b>./expt/</b>               contains sample program output files (training/test vector files and MaxEnt classification results)<br />
<b>./train_classiry.sh</b>     the wrapper for creating feature vectors, running the classifier and writing results<br />
<b>./create_vectors.sh</b>           the shell script to invoke create_vectors.py<br />
<b>./create_vectors.py</b>           create feature vectors for all files under given dir<br />
<b>./proc_file.sh</b>                the shell script to invoke create_vectors.py with option '-f' to process a single input doc<br />
<b>./proc_file.py</b>                called by create_vectors.py to process an individual file<br />

#####Usage
1. to process a single file, output the feature vectors to a give file:<br />
  ./proc_file.sh input_file targetLabel output_file<br />
2. to process all files under multiple dirs, output the feature vectors to a given file:<br />
  ./create_vectors.sh output_vector_file dir1 dir2 ... dir_n<br />
3. to create feature vectors for all the training and test data, run the classifier and output all the intermediate and resultative files to a given dir:<br />
  ./train_classify.sh param_file train_dir test_dir output_dir<br />

