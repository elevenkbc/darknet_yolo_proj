# -*- coding: UTF-8 -*-
'''
Created on Jan 25, 2020

@author: bc
'''
import os
import cv2
import numpy as np
#預處理車牌, 將抓到車牌去除陰影 + 灰階化
def rm_shadow(im):
    dilated_img = cv2.dilate(im, np.ones((7,7), np.uint8))
    bg_img = cv2.medianBlur(dilated_img, 21)
    diff_img = 255 - cv2.absdiff(im, bg_img)
    norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    return norm_img


xmlFolder = 'yolo_dir/xml'
imgFolder = 'yolo_dir/crop_img'
saveImgPath = 'yolo_dir/processing01'

if not os.path.exists(saveImgPath):
    os.makedirs(saveImgPath)

for file in os.listdir(imgFolder):
    im = cv2.imread(os.path.join(imgFolder, file))
#     cv2.imshow('original im', im)
    rgb_im = cv2.split(im)
    rgb_im2 = []
    for im_tmp in rgb_im:
        norm_img = rm_shadow(im_tmp)
        rgb_im2.append(norm_img)
    rgb_im2 = cv2.merge(rgb_im2)#去除陰影後
#     cv2.imshow('remove shadow', rgb_im2)
#     cv2.waitKey(0)
    cv2.imwrite(os.path.join(saveImgPath, file), rgb_im2)
