#!/bin/sh
export _JAVA_OPTIONS="-Xms4g -Xmx4g"
param_filename=$1
train_dir=$2
test_dir=$3
output_dir=$4
train_data=$train_dir/*
test_data=$test_dir/*
train_vector_txt=$output_dir/train.vectors.txt
test_vector_txt=$output_dir/test.vectors.txt
train_vector_bin=$output_dir/train.vectors
test_vector_bin=$output_dir/test.vectors
model=$output_dir/me.model
test_result=$output_dir/test.result
mkdir -p $output_dir
./create_vectors.sh $param_filename $train_vector_txt $train_data
./create_vectors.sh $param_filename $test_vector_txt $test_data
mallet import-svmlight --input $train_vector_txt --output $train_vector_bin
mallet import-svmlight --input $test_vector_txt --output $test_vector_bin  --use-pipe-from $train_vector_bin
vectors2classify --training-file $train_vector_bin --testing-file $test_vector_bin --trainer MaxEnt --output-classifier $model --report train:accuracy train:confusion test:accuracy test:confusion >$test_result 2>$output_dir/me.model.stderr