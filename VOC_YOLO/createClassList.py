'''
Created on 2020年1月19日

@author: RaoBlack
'''
import string
import os   
AtoZ = string.ascii_uppercase
print(AtoZ)


classList = dict()
AtoZ = string.ascii_uppercase
for i in range(len(AtoZ)):
    classList[AtoZ[i]] = i
for i in range(10):
    classList[str(i)] = i + 26
    
print(classList)


path=os.path.dirname("C:/folder1/folder2/filename.xml")
print(path)
print(os.path.basename(path))


print(os.path.abspath(os.path.join(path, os.pardir)))
