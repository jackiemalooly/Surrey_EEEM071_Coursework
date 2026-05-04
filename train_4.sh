#!/bin/bash

STUDENT_ID=6861173 STUDENT_NAME="Jackie Malooly" python main.py \
-s veri \
-t veri \
-a googlenet \
--root /user/HS402/jm02999/Surrey_EEEM071_Coursework \
--height 224 \
--width 224 \
--optim amsgrad \
--lr 0.00008 \
--max-epoch 10 \
--stepsize 20 40 \
--train-batch-size 256 \
--test-batch-size 100 \
--color-jitter \
--random-erase \
--save-dir logs/googlenet-color-lr-batch-256-veri \