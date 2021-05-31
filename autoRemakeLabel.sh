#!/bin/bash

#Input
# Input 
readonly INPUT_DIRECTORY="input"
echo -n "Is json file name remakeLabel.json?[y/n]:"
read which
while [ ! $which = "y" -a ! $which = "n" ]
do
 echo -n "Is json file name the same as this file name?[y/n]:"
 read which
done

# Specify json file path.
if [ $which = "y" ];then
 JSON_NAME="remakeLabel.json"
else
 echo -n "JSON_FILE_NAME="
 read JSON_NAME
fi

# From json file, read required variables.
readonly JSON_FILE="${INPUT_DIRECTORY}/${JSON_NAME}"
readonly DATA_DIRECTORY=$(eval echo $(cat ${JSON_FILE} | jq -r ".data_directory"))
readonly SAVE_DIRECTORY=$(eval echo $(cat ${JSON_FILE} | jq -r ".save_directory"))
readonly LABEL_NAME=$(cat ${JSON_FILE} | jq -r ".label_name")
readonly SAVE_NAME=$(cat ${JSON_FILE} | jq -r ".save_name")
readonly NUM_CLASS=$(cat ${JSON_FILE} | jq -r ".num_class")
readonly IGNORE_CLASSES=$(cat ${JSON_FILE} | jq -r ".ignore_classes")
readonly SQUEEZE=$(cat ${JSON_FILE} | jq -r ".squeeze")
readonly NUM_ARRAY=$(cat ${JSON_FILE} | jq -r ".num_array[]")
readonly LOG_FILE=$(cat ${JSON_FILE} | jq -r ".log_file")

mkdir -p `dirname ${LOG_FILE}`
date >> $LOG_FILE

for number in ${NUM_ARRAY[@]}
do

 label="${DATA_DIRECTORY}/case_${number}/${LABEL_NAME}"
 save="${SAVE_DIRECTORY}/case_${number}/${SAVE_NAME}"

 if ${SQUEEZE}; then
     squeeze="--squeeze"
 else
     squeeze=""
 fi

  


 python3 remakeLabel.py ${label} ${save} --num_class ${NUM_CLASS} --ignore_classes ${IGNORE_CLASSES} ${squeeze}

 # Judge if it works.
 if [ $? -eq 0 ]; then
  echo "case_${number} done."

 else
  echo "case_${number}" >> $LOG_FILE
  echo "case_${number} failed"

 fi

done


