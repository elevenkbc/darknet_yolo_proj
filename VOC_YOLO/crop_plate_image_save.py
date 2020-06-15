# -*- coding: UTF-8 -*-
'''
Created on Jan 23, 2020

@author: bc
'''

import os
import cv2
import xml.etree.ElementTree as ET


xmlFolder = 'yolo_dir/PlatePositionTraining/VideoImgXml'
imgFolder = 'yolo_dir/PlatePositionTraining/VideoImg'
saveImgPath = 'yolo_dir/PlateNumberTraining/testPlateImageNight'


plate_h = 60  #讓每一個擷取下來的 plate 高度 = 60
if not os.path.exists(saveImgPath):
    os.makedirs(saveImgPath)

plate_count = 979

# filePrefix = 'day'
filePrefix = 'night'
fileNumStart = 497
fileNumEnd = 577
    
for num in range(fileNumStart, fileNumEnd + 1):
    filename = filePrefix + '%04d' % num
    print('processing img', filename + '.jpg')
    im = cv2.imread(os.path.join(imgFolder, (filename + '.jpg')))
    cv2.namedWindow("Demo",0);
    cv2.resizeWindow("Demo", 1920//2, 1080//2);
    cv2.imshow('Demo', im)
    
    #如果沒有對應的 xml檔案，表示該圖中沒有車牌，直接處理下一筆
    try:
        tree = ET.parse(os.path.join(xmlFolder, filename + '.xml'))
    except FileNotFoundError:
        continue
    root = tree.getroot()
    for obj in root.findall('object'):
        name = obj.find('name').text
        bdx = obj.find('bndbox')
        xmin = int(bdx.find('xmin').text)
        ymin = int(bdx.find('ymin').text)
        xmax = int(bdx.find('xmax').text)
        ymax = int(bdx.find('ymax').text)
        im_plate = im[ymin:ymax, xmin:xmax, :]
        #等比例縮放到高=plate_want[0]
        s = plate_h/im_plate.shape[0] #縮放常數
        plate_w = round(im_plate.shape[1]*s)
        print(im_plate.shape)
        im_plate = cv2.resize(im_plate, (plate_w, plate_h), interpolation=cv2.INTER_LINEAR)
        print(im_plate.shape)
        cv2.imshow('plate(after)', im_plate) 
        cv2.imwrite(os.path.join(saveImgPath, 'plate%04d.jpg'%plate_count), im_plate)
        plate_count += 1
#         cv2.waitKey(20)

    
