#!/bin/bash

# Input 
readonly INPUT_DIRECTORY="input"
echo -n "Is json file name changeSpacing.json?[y/n]:"
read which
while [ ! $which = "y" -a ! $which = "n" ]
do
 echo -n "Is json file name the same as this file name?[y/n]:"
 read which
done

# Specify json file.
if [ $which = "y" ];then
 JSON_NAME="changeSpacing.json"
else
 echo -n "JSON_FILE_NAME="
 read JSON_NAME
fi

# From json file, read required variables.
readonly JSON_FILE="${INPUT_DIRECTORY}/${JSON_NAME}"
readonly DATA_DIRECTORY=$(eval echo $(cat ${JSON_FILE} | jq -r ".data_directory"))
readonly SAVE_DIRECTORY=$(eval echo $(cat ${JSON_FILE} | jq -r ".save_directory"))
readonly INPUT_NAME=$(cat ${JSON_FILE} | jq -r ".input_name")
readonly SAVE_NAME=$(cat ${JSON_FILE} | jq -r ".save_name")
readonly SPACING=$(cat ${JSON_FILE} | jq -r ".spacing")

readonly NUM_ARRAY=$(cat ${JSON_FILE} | jq -r ".num_array[]")
readonly LOG_FILE=$(eval echo $(cat ${JSON_FILE} | jq -r ".log_file"))

echo "LOG_FILE:${LOG_FILE}"

# Make directory to save LOG.
mkdir -p `dirname ${LOG_FILE}`
date >> $LOG_FILE

for number in ${NUM_ARRAY[@]}
do
 data="${DATA_DIRECTORY}/case_${number}"

 echo "input_dir:${data}"
 echo "save_dir:${data}"
 echo "input_name:${INPUT_NAME}"
 echo "save_name:${SAVE_NAME}"
 echo "spacing:${SPACING}"

 python3 changeSpacing.py ${data} ${data} --input_name ${INPUT_NAME} --save_name ${SAVE_NAME} --spacing ${SPACING}



 # Judge if it works.
 if [ $? -eq 0 ]; then
  echo "case_${number} done."
 
 else
  echo "case_${number}" >> $LOG_FILE
  echo "case_${number} failed"
 
 fi

done


