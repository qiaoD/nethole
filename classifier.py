'''
time:2018/01/19
Author:QD


类型 | 位置 | 原因 | 步骤 | 后果 | 解决方案

1 每项在excel中占一列
2 出现多个关键字，用竖杠进行分割

steps:
1 read the template and get the array xlrd
2 predict and get the score

'''

import xlrd
import numpy as np

class cls:

    allType   = ""
    filePath  = ""
    bigDict   = {}          # dict
    keys      = []          # all the types

    def __init__(self,filePath):
        self.filePath = filePath
        if ""!=self.filePath :
            self.build()

    def build():
        filePath = self.filePath
        excel = xlrd.open_workbook(filePath)
        sheet = excel.sheets()[0]
        nrows = sheet.nrows
        for i in range(nrows):
            tname = sheet.row_values(i)[0]            # get the type
            tlist = [sheet.row_values(i)[1],
                     sheet.row_values(i)[2],
                     sheet.row_values(i)[3],
                     sheet.row_values(i)[4],
                     sheet.row_values(i)[5]]
            if self.bigDict.has_key(tname):
                self.bigDict[tname].append(tlist)
            else :
                self.bigDict[tname] = [tlist]
        self.keys = self.bigDict.keys()               # get all the keys of dict



    def predict(self,predictFile):
        if "" == predictFile:
            return -1;

        myKey = 'sql'                                 # just for debug
        myDict = self.bigDict[myKey]
        for l in myDict:
            print(l)
