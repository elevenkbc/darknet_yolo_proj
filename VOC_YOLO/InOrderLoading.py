# -*- coding: UTF-8 -*-
'''
Created on 2020年2月1日

@author: RaoBlack
'''
import os
from shutil import copyfile

#按照順序讀取，更改黨名另存


FolderPath = '/home/bc/Documents/FuXuanTechVideo/0404/Video_20180404111426_104 (2019-1-21 PM 11-04-07)'

TargetPath = 'yolo_dir/PlatePositionTraining/VideoImg'
# rn = 'day'
rn = 'night'
num = 535
for file in sorted(os.listdir(FolderPath)):
    print('Processing filename=', file)
    newName = rn + '%04d'%num + '.jpg'
    print('newName=', newName)
#     copyfile(os.path.join(FolderPath, file), os.path.join(TargetPath, newName))
    num += 1