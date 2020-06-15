# -*- coding: UTF-8 -*-
'''
Created on Jan 27, 2020

@author: bc
'''
#將frame (img) 與 label(txt) 移動到特定資料夾

import os
from shutil import copyfile


# targetPath = 'yolo_dir/PlatePositionTraining/Images'
# imgPath = 'yolo_dir/PlatePositionTraining/VideoImg'
# txtPath = 'yolo_dir/PlatePositionTraining/VideoImgTxt'

targetPath = 'yolo_dir/PlateNumberTraining/PlateImg_image_0212'
imgPath = 'yolo_dir/PlateNumberTraining/PlateImg'
txtPath = 'yolo_dir/PlateNumberTraining/PlateImgTxt'

if not os.path.isdir(targetPath):
    os.makedirs(targetPath)
for file in sorted(os.listdir(txtPath)):
    print('processing', file)
    filename, _ = os.path.splitext(file)
    copyfile(os.path.join(txtPath, filename+'.txt'), os.path.join(targetPath ,filename+'.txt'))
    copyfile(os.path.join(imgPath, filename+'.jpg'), os.path.join(targetPath ,filename+'.jpg'))
    
