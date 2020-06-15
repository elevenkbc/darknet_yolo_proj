# -*- coding: UTF-8 -*-
'''
Created on 2020年1月20日

@author: RaoBlack
'''
#選擇有標註物品的frame，並且將這些frame與 label(xml)移動到特定資料夾
import os
from shutil import copyfile
 
currentRoot = os.getcwd()
folder = 'yolo_dir'
Imgfolder = 'img'
Xmlfolder = 'xml'

ImgPath = os.path.join(folder, Imgfolder)
XmlPath = os.path.join(folder, Xmlfolder)
if not os.path.isdir(ImgPath):
    os.makedirs(ImgPath)
if not os.path.isdir(XmlPath):
    os.makedirs(XmlPath)
    

fromImgPath = 'C:\\Users\\RaoBlack\\Google 雲端硬碟\\FuXuanTechVideo\\frames'
fromXmlPath = 'C:\\Users\\RaoBlack\\Google 雲端硬碟\\FuXuanTechVideo\\Label_plate'


for file in os.listdir(fromXmlPath):
    print('processing', file)
    filename, _ = os.path.splitext(file)
    copyfile(os.path.join(fromXmlPath, filename+'.xml'), os.path.join(XmlPath ,filename+'.xml'))
    copyfile(os.path.join(fromImgPath, filename+'.jpg'), os.path.join(ImgPath ,filename+'.jpg'))
    