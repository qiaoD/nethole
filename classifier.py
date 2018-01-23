'''
time:2018/01/22
Author:QD


漏洞描述 | 类型 | 影响方面 | 位置 | 原因 | 步骤 | 后果 | 解决方案

1 每项在excel中占一列
2 出现多个关键字，用竖杠进行分割

steps:
1 read the template and get the array xlrd
2 predict and get the score

'''

import xlrd
import xlwt
import numpy as np

class cls:

    #allType   = ""
    filePath  = ""
    bigDict   = {}          # dict
    keys      = []          # all the types
    # sheet     = ''          # write handle

    def __init__(self,filePath):
        self.filePath = filePath
        if ""!=self.filePath :
            self.build()

    def build(self):
        filePath = self.filePath
        excel = xlrd.open_workbook(filePath)
        sheet = excel.sheets()[0]
        nrows = sheet.nrows
        beg = 1
        for i in range(nrows):
            tname = sheet.row_values(i)[beg]            # get the type
            tname = 'file'
            tlist = [sheet.row_values(i)[beg+1],
                     sheet.row_values(i)[beg+2],
                     sheet.row_values(i)[beg+3],
                     sheet.row_values(i)[beg+4],
                     sheet.row_values(i)[beg+5],
                     sheet.row_values(i)[beg+6],
                     sheet.row_values(i)[beg+7],    # base border
                     sheet.row_values(i)[beg+8],
                     sheet.row_values(i)[beg+9],
                     sheet.row_values(i)[beg+10],
                     sheet.row_values(i)[beg+11],
                     sheet.row_values(i)[beg+12],
                     sheet.row_values(i)[beg+13],
                     sheet.row_values(i)[beg+14]]
            if tname in self.bigDict:
                self.bigDict[tname].append(tlist)
            else :
                self.bigDict[tname] = [tlist]
        self.keys = self.bigDict.keys()               # get all the keys of dict
        #print(self.bigDict)
        #self.sheet = sheet



    def predict(self,predictFile):
        if "" == predictFile:
            return -1;
        wb = xlwt.Workbook()
        ws = wb.add_sheet('q')

        # get the predictFile
        excel = xlrd.open_workbook(predictFile)
        sheet = excel.sheets()[0]
        nrows = sheet.nrows
        for i in range(nrows):
            des = sheet.row_values(i)[6]                  # get the description
            for jj in range(0,15):
                ws.write(i, jj, sheet.row_values(i)[jj])
            scoreList = []
            for l in self.getType():
                # key words
                '''
                theType     = l[0].split('|')
                theAffect   = l[1].split('|')
                thePos      = l[2].split('|')
                theReason   = l[3].split('|')
                theStep     = l[4].split('|')
                theResult   = l[5].split('|')
                '''
                theList     = (str(l[0]) + "|" +
                              str(l[1]) + "|" +
                              str(l[2]) + "|" +
                              str(l[3]) + "|" +
                              str(l[4]) + "|" +
                              str(l[5])).split('|')
                leng = len(theList)

                num = 0
                for ii in theList:
                    if -1 != des.find(ii):
                        num += 1
                scoreList.append(num/leng)

            index = scoreList.index(max(scoreList))

            for j in range(6,14):
                ws.write(i, j+9, self.bigDict['file'][index][j])
                print(self.bigDict['file'][index][j])

        wb.save("e.xls")




    def getType(self):
        myKey = 'file'                                     # just for dubeg
        myList = self.bigDict[myKey]
        for l in myList:
            yield l


# FOR DEBUG
filePath = 'file.xls'
predictFile = 'hole.xlsx'

c = cls(filePath)
c.predict(predictFile)

'''
#end
'''
