#!/bin/bash

STUDENT_ID=6861173 STUDENT_NAME="Jackie Malooly" python main.py \
-s veri \
-t veri \
-a googlenet \
--evaluate \
--resume logs/googlenet-color-lr-0.00008-veri/model.pth.tar-10 \
--root /user/HS402/jm02999/Surrey_EEEM071_Coursework \
--save-dir logs/googlenet-color-lr-0.00008-veri \
