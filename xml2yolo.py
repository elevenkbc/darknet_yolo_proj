'''
Created on Feb 2, 2020

@author: bc
'''
import xml.etree.ElementTree as ET
import os
import string

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

 
def convert_annotation(xmlFolderPath, saveFolderPath, filename, classesList):
    try:
        in_file = open(os.path.join(xmlFolderPath, filename + '.xml'), 'r', encoding='utf-8')
    except FileNotFoundError:
        print('not found %s return' % (filename + '.xml'))
        return  # 找不到文件就不處理，直接return 
    out_file = open(os.path.join(saveFolderPath, filename + '.txt'), 'w', encoding='utf-8')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')  
    w = int(size.find('width').text)
    h = int(size.find('height').text)
 
    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classesList :
            continue
        cls_id = classesList.index(cls)
        xmlbox = obj.find('bndbox')   
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    out_file.close()
    
    
#---------------------------------------------------------------


if __name__ == "__main__":
#     xmlFolderPath = 'yolo_dir/PlatePositionTraining/VideoImgXml'
#     saveFolderPath = 'yolo_dir/PlatePositionTraining/VideoImgTxt'
    
#     xmlFolderPath = 'yolo_dir/Pedicle_0902/Xml'
#     saveFolderPath = 'yolo_dir/Pedicle_0902/Txt'

    xmlFolderPath = 'yolo_dir/Pedicle_1112/Xml'
    saveFolderPath = 'yolo_dir/Pedicle_1112/Txt'
    if not os.path.exists(saveFolderPath):
        os.makedirs(saveFolderPath)
    # case1: 車牌位置檢測
#     classesList = ['Plate'] 
    
    # case2: 車牌中的英文數字檢測
#     classesList = []
#     AtoZ = string.ascii_uppercase
#     for i in range(len(AtoZ)):
#         classesList.append(AtoZ[i])
#     for i in range(10):
#         classesList.append(str(i))
#     
#     if not os.path.exists(saveFolderPath):
#         os.makedirs(saveFolderPath)
    # case3: pedicle eyes and nose
    classesList = ['eyes', 'nose', 'line']

    # 方法1: 整個folder 按照順序通通讀取
    files = os.listdir(xmlFolderPath)
    files.sort(key=lambda x:int(x[3:7]))#檔案照順序讀取
   
    for file in files:
        print('processing file', file)
        fn, _ = os.path.splitext(file) #分離檔名、副檔名
        convert_annotation(xmlFolderPath, saveFolderPath, fn, classesList)
    
    # 方法2: 照一個範圍的檔案順序讀取
#     filePrefix = 'day'
#     filePrefix = 'night'
#     fileNumStart = 498
#     fileNumEnd = 577
#     for num in range(fileNumStart, fileNumEnd + 1):
#         fn = filePrefix + '%04d' % num
#         print('processing filename = ', fn)
#         convert_annotation(xmlFolderPath, saveFolderPath, fn)
#         stop = 1
