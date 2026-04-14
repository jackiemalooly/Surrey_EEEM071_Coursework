#!/bin/bash

STUDENT_ID='6861173' STUDENT_NAME="Jackie Malooly" python main.py \
-s veri \
-t veri \
-a googlenet \
--root /user/HS402/jm02999/Documents/Surrey_EEEM071_Coursework/ \
--height 224 \
--width 224 \
--optim amsgrad \
--lr 0.0003 \
--max-epoch 10 \
--stepsize 20 40 \
--train-batch-size 64 \
--test-batch-size 100 \
--save-dir logs/googlenet-veri
