'''
Created on 2020年1月19日

@author: RaoBlack
'''
from xml.etree.ElementTree import Element, ElementTree


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


root = Element('annotation')
tree = ElementTree(root)

dict01 = {'folder':'frames', 
          'filename':'day001.jpg', 
          'path':'C:\\Users\\RaoBlack\\Google 雲端硬碟\\FuXuanTechVideo\\frames\\day001.jpg'}

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
indent(child00,1) #整理 source 標籤格式

#建立 size
child00 = Element('size')
root.append(child00)
dict01 = {'width':'1920',
          'height':'1080',
          'depth':'3'}
for k, v in dict01.items():
    child01 = Element(k)
    child01.text = v
    child00.append(child01)
indent(child00,1) #整理 size 標籤格式

#建立 segmented
child00 = Element('segmented')
child00.text = '0'
root.append(child00)



#建立 objects
objs = [
    {
        'name': 'M',
        'pose': 'Unspecified',
        'truncated': '0',
        'difficult': '0',
        'bndbox': ['1464', '653', '1478', '685']
    },
    {
        'name': 'K',
        'pose': 'Unspecified',
        'truncated': '0',
        'difficult': '0',
        'bndbox': ['1478', '649', '1493', '686']
    },
    {
        'name': 'G',
        'pose': 'Unspecified',
        'truncated': '0',
        'difficult': '0',
        'bndbox': ['1490', '654', '1510', '686']
    },
    {
        'name': '0',
        'pose': 'Unspecified',
        'truncated': '0',
        'difficult': '0',
        'bndbox': ['1510', '654', '1524', '681']
    },
    {
        'name': '1',
        'pose': 'Unspecified',
        'truncated': '0',
        'difficult': '0',
        'bndbox': ['1524', '653', '1539', '689']
    }       
]

bndbox_list = ['xmin', 'ymin', 'xmax', 'ymax']
for obj in objs:
    child00 = Element('object')
    root.append(child00)
    for k, v in obj.items():
        if k is not 'bndbox':
            child01 = Element(k)
            child01.text = v
            child00.append(child01)
        else:
            child01 = Element(k)
            for i in range(len(bndbox_list)):
                child02 = Element(bndbox_list[i])  
                child02.text = v[i]
                child01.append(child02)
            child00.append(child01)   
indent(child00, 1) #整理 object 標籤格式

indent(root, 0)
tree.write('tmp.xml', 'UTF-8')