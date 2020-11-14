'''
Created on Nov 13, 2020

@author: raoblack
'''

import cv2
import numpy as np
import os

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, ElementTree
import string
def rotate_flip(img):
    # flip by x=y
    h = img.shape[0]
    w = img.shape[1]
    c = img.shape[2]
    S = img[:h, :h, :].copy()
    #cv2.imshow('test1', img_i)
    for i in range(S.shape[2]):
        S[:, :, i] = np.transpose(S[:, :, i])

    newS = S.copy()
#     for i in range(h):
#         newS[:, i, :] = S[:, h-1-i, :]
    resimg = img.copy()
    resimg[:h, :h, :] = newS
    return resimg
    
def Xml_flip(xmlFolderPath, filename, imgFolderPath):
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
    try:
        in_file = open(os.path.join(xmlFolderPath, filename + '.xml'), 'r', encoding='utf-8')
    except FileNotFoundError:
        print('not found %s return' % (filename + '.xml'))
        return  # 找不到文件就不處理，直接return 
    sfn = filename + '_f' #save file name
    
    img = cv2.imread(os.path.join(imgFolderPath, filename + '.jpg'))
    
    img_flip = rotate_flip(img)
    
    cv2.imwrite(os.path.join(imgFolderPath, sfn + '.jpg'), img_flip)
    
     
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')  
    im_w = int(size.find('width').text)
    im_h = int(size.find('height').text)
    im_c = int(size.find('depth').text)
     
    

#     for i in range(len(txtArray)):
# 
# 
#         # 換算成 (xmin, xmax, ymin, ymax) VOC 格式
#         x = txtLine[1]
#         y = txtLine[2]
#         w = txtLine[3]
#         h = txtLine[4]
#         xmin = int(round((2 * x - w) * im_w / 2));
#         xmax = int(round((2 * x + w) * im_w / 2));
#         ymin = int(round((2 * y - h) * im_h / 2));
#         ymax = int(round((2 * y + h) * im_h / 2));
#         tmpDict['bndbox'] = [str(xmin), str(ymin), str(xmax), str(ymax)]
#         objs.append(tmpDict)
        
    #建立objs
    objs = []
    for obj in root.iter('object'):
        tmpDict = dict()
        tmpDict['name'] = obj.find('name').text
        tmpDict['pose'] = 'Unspecified'
        tmpDict['truncated'] = '0'
        tmpDict['difficult'] = '0'
        
        xmlbox = obj.find('bndbox')
        xmin = xmlbox.find('ymin').text;
        xmax = xmlbox.find('ymax').text;
        ymin = xmlbox.find('xmin').text;
        ymax = xmlbox.find('xmax').text;
        tmpDict['bndbox'] = [xmin, ymin, xmax, ymax]
        objs.append(tmpDict)
  
    root = Element('annotation')
    tree = ElementTree(root)
    imgfolder = os.path.basename(imgFolderPath)
    dict01 = {'folder': imgfolder,
          'filename':  sfn + '.jpg',
          'path':os.path.join(imgFolderPath, sfn + '.jpg')}
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
              'depth':str(im_c)}
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
                 
  
    indent(child00, 1) #整理 object 標籤格式
 
    indent(root, 0) #整理 annotation 的格式
    tree.write(os.path.join(xmlFolderPath, sfn + '.xml'), 'UTF-8')
     
      
    
    
def testRotateImg():
    img = cv2.imread("/home/raoblack/workspace/darknet_yolo_trainingdata/yolo_dir/Pedicle_1112/Img/img0010.jpg")
    img2 = rotate_flip(img)
    cv2.imshow('img', img)
    cv2.imshow('img2', img2)
    cv2.waitKey(0)
def test_flip_label():
    xmlFolderPath = "yolo_dir/Pedicle_1112/Xml"
    filename = "img0002"
    imgFolderPath = "yolo_dir/Pedicle_1112/Img"
    Xml_flip(xmlFolderPath, filename, imgFolderPath)
if __name__ == "__main__":
#     testRotateImg()
#     test_flip_label()

    xmlFolderPath = "yolo_dir/Pedicle_1112/Xml"
    imgFolderPath = "yolo_dir/Pedicle_1112/Img"
    


    files = os.listdir(imgFolderPath)
    files.sort(key=lambda x:int(x[-8:-4]))#檔案照順序讀取
   
    for file in files:
        print('processing file', file)
        filename, _ = os.path.splitext(file) #分離檔名、副檔名
        Xml_flip(xmlFolderPath, filename, imgFolderPath)
        
    