#!/bin/bash

# Input 
readonly INPUT_DIRECTORY="input"
echo -n "Is json file name integrateLabels.json?[y/n]:"
read which
while [ ! $which = "y" -a ! $which = "n" ]
do
 echo -n "Is json file name the same as this file name?[y/n]:"
 read which
done

# Specify json file.
if [ $which = "y" ];then
 JSON_NAME="integrateLabels.json"
else
 echo -n "JSON_FILE_NAME="
 read JSON_NAME
fi

# From json file, read required variables.
readonly JSON_FILE="${INPUT_DIRECTORY}/${JSON_NAME}"
readonly DATA_DIRECTORY=$(eval echo $(cat ${JSON_FILE} | jq -r ".data_directory"))
readonly SAVE_DIRECTORY=$(eval echo $(cat ${JSON_FILE} | jq -r ".save_directory"))
readonly LABEL_NAMES=$(cat ${JSON_FILE} | jq -r ".label_names[]")
readonly SAVE_NAME=$(cat ${JSON_FILE} | jq -r ".save_name")
readonly NUM_ARRAY=$(cat ${JSON_FILE} | jq -r ".num_array[]")
readonly LOG_FILE=$(eval echo $(cat ${JSON_FILE} | jq -r ".log_file"))

echo "LOG_FILE:${LOG_FILE}"

# Make directory to save LOG.
mkdir -p `dirname ${LOG_FILE}`
date >> $LOG_FILE

for number in ${NUM_ARRAY[@]}
do
 data="${DATA_DIRECTORY}/case_${number}"
 save_path="${SAVE_DIRECTORY}/case_${number}/${SAVE_NAME}"
 label_list=""
 for label_name in ${LABEL_NAMES[@]}
 do
   label="${data}/${label_name}"
   label_list+="${label} "
 done


 python3 integrateLabels.py --label_path_list ${label_list} --save_path ${save_path}

 # Judge if it works.
 if [ $? -eq 0 ]; then
  echo "case_${number} done."
 
 else
  echo "case_${number}" >> $LOG_FILE
  echo "case_${number} failed"
 
 fi

done


