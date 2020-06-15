# -*- coding: UTF-8 -*-
'''
Created on 2020年1月20日

@author: RaoBlack
'''

import numpy as np
import cv2
import os
from xml.etree.ElementTree import Element, ElementTree
import string

def convert2xml(imgfolderPath, savefolder, yolofolder, txtName, classArrray):
    #將xml存到 imgfolderPath中，與原jpg圖片一起
    def indent(elem, level=0):
        "自動換行，縮排"
        i = "\n" + level*"    "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "    "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
    
    
    
    fn, _ = os.path.splitext(txtName) #去除附檔名的filename
    img = cv2.imread(os.path.join(imgfolderPath, fn + '.jpg'))
    im_h, im_w, im_ch = img.shape
    
    
    rootPath = os.path.abspath(os.path.join(imgfolderPath, os.pardir)) #imgfolderPath 的上一層目錄
    savePath = os.path.join(rootPath, savefolder)
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    
    #建立objects
    #讀取yolo.txt 檔案
    txtArray = np.loadtxt(os.path.join(rootPath, yolofolder, fn+'.txt'), delimiter=' ')
    if txtArray.ndim == 0:#如果預測沒有東西
        return
    if txtArray.ndim != 2:
        txtArray = [txtArray] #處理有時候 txtArray 不是2D numpy array 問題
    #建立objs
    objs = []
    for i in range(len(txtArray)):
        txtLine = txtArray[i]
        tmpDict = dict()
        tmpDict['name'] = classArrray[int(txtLine[0])]
        tmpDict['pose'] = 'Unspecified'
        tmpDict['truncated'] = '0'
        tmpDict['difficult'] = '0'
        # 換算成 (xmin, xmax, ymin, ymax) VOC 格式
        x = txtLine[1]
        y = txtLine[2]
        w = txtLine[3]
        h = txtLine[4]
        xmin = int(round((2 * x - w) * im_w / 2));
        xmax = int(round((2 * x + w) * im_w / 2));
        ymin = int(round((2 * y - h) * im_h / 2));
        ymax = int(round((2 * y + h) * im_h / 2));
        tmpDict['bndbox'] = [str(xmin), str(ymin), str(xmax), str(ymax)]
        
        objs.append(tmpDict)
    
    root = Element('annotation')
    tree = ElementTree(root)
    imgfolder = os.path.basename(imgfolderPath)
    dict01 = {'folder':imgfolder,
          'filename':fn + '.jpg',
          'path':os.path.join(imgfolderPath, fn + '.jpg')}
    #建立 folder, segmented, path
    for k, v in dict01.items():
        child00 = Element(k)
        child00.text = v
        root.append(child00)
    #建立 source
    child00 = Element('source')
    root.append(child00)
    child01 = Element('database')
    child01.text = 'Unknown'
    child00.append(child01)
    indent(child00, 1) #整理 source 標籤格式    root.append(child00)    
    
    #建立 size
    child00 = Element('size')
    root.append(child00)
    dict01 = {'width':str(im_w),
              'height':str(im_h),
              'depth':str(im_ch)}
    for k in ['width', 'height', 'depth']:
        child01 = Element(k)
        child01.text = dict01[k]
        child00.append(child01)
    indent(child00,1) #整理 size 標籤格式
    #建立 segmented
    child00 = Element('segmented')
    child00.text = '0'
    root.append(child00)
    
    #建立 object
    bndbox_list = ['xmin', 'ymin', 'xmax', 'ymax']
    for obj in objs:
        child00 = Element('object')
        root.append(child00)
        for k in ['name', 'pose', 'truncated', 'difficult']:
            child01 = Element(k)
            child01.text = obj[k]
            child00.append(child01)
        #bndbox case
        k = 'bndbox'
        child01 = Element(k)
        bndboxDic = obj[k]
        for i in range(len(bndbox_list)):
            child02 = Element(bndbox_list[i])  
            child02.text = bndboxDic[i]
            child01.append(child02)
        child00.append(child01)
                
#         for k, v in obj.items():
#             if k is not 'bndbox':
#                 child01 = Element(k)
#                 child01.text = v
#                 child00.append(child01)
#             else:
#                 child01 = Element(k)
#                 for i in range(len(bndbox_list)):
#                     child02 = Element(bndbox_list[i])  
#                     child02.text = v[i]
#                     child01.append(child02)
#                 child00.append(child01)   
    indent(child00, 1) #整理 object 標籤格式

    indent(root, 0) #整理 annotation 的格式
    tree.write(os.path.join(savePath, fn + '.xml'), 'UTF-8')


# classArrray = ['plate']
classArrray = []
AtoZ = string.ascii_uppercase
for a in AtoZ:
    classArrray.append(a)
for i in range(10):
    classArrray.append(str(i))
    

imgfolderPath = '/home/bc/eclipse-workspace/PLR_35/VOC_YOLO/yolo_dir/PlateNumberTraining/PlateImg'

yolofolder = 'predictTxt'
savefolder = 'predictTxtXml'

for file in sorted(os.listdir(os.path.join('yolo_dir/PlateNumberTraining', yolofolder))):
    print('processing', file)
    convert2xml(imgfolderPath, savefolder, yolofolder, file, classArrray)
    
