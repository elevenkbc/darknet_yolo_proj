# -*- coding: UTF-8 -*-
'''
Created on Jan 27, 2020

@author: bc
'''
import os
import cv2
import numpy as np
from skimage.filters import threshold_local
#預處理車牌, 將抓到車排反白，讓字變成黑色，並且去除部份陰影
def preprocess(img):
    V = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))[2] #得到灰階直
    thresh = threshold_local(V, 55) #binarized
    img_bw = 1.0*(V > thresh)
    white_num = np.sum(img_bw)
    black_num = img.shape[0]*img.shape[1] - np.sum(img_bw)
    
    if black_num - 300 > white_num:
        img_norimalized = 255 - img
        fg_mask = 255*(V > thresh).astype(np.uint8)
        bg_mask = 255*(V <= thresh).astype(np.uint8)
    else:
        img_norimalized = img
        fg_mask = 255*(V <= thresh).astype(np.uint8)
        bg_mask = 255*(V > thresh).astype(np.uint8)

    fg_masked = cv2.add(img_norimalized, np.zeros(np.shape(img_norimalized), dtype=np.uint8), mask=fg_mask)
    bg_masked = cv2.add(255*np.ones(np.shape(img_norimalized), dtype=np.uint8), np.zeros(np.shape(img_norimalized), dtype=np.uint8), mask=bg_mask)

    img_masked = fg_masked + bg_masked 
    return img_masked


# xmlFolder = 'yolo_dir/PlatePositionTraining/VideoImgXml'
# imgFolder = 'yolo_dir/PlatePositionTraining/VideoImg'
# saveImgPath = 'yolo_dir/PlateNumberTraining/testPlateImage'

xmlFolder = 'yolo_dir/PlateNumberTraining/VideoImgXml'
imgFolder = 'yolo_dir/PlateNumberTraining/PlateImg'
saveImgPath = 'yolo_dir/PlateNumberTraining/testPlateImage'

if not os.path.exists(saveImgPath):
    os.makedirs(saveImgPath)

filePrefix = 'plate'
fileNumStart = 452
fileNumEnd = 655
    
for num in range(fileNumStart, fileNumEnd + 1):
    filename = filePrefix + '%04d' % num
    print('preprocesing file name = %s' % (filename + '.jpg'))
    im = cv2.imread(os.path.join(imgFolder, (filename + '.jpg')))
    cv2.imshow('original im', im)
    im = preprocess(im)
    cv2.imshow('remove shadow', im)
    cv2.imwrite(os.path.join(saveImgPath, (filename + '.jpg')), im)
