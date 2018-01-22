'''

time:2018/01/15
Author:QD

------

1 get the data : xlrd
2 preprocess the data: data -> number : jieba / numpy
3 use the alg : scikit-learn

------

the file's line format:(I just get the [0] and [2] to the data and use it to study)

['漏洞名称',
'通告时间',
'漏洞描述',
'漏洞编号',
'漏洞类型',
'影响设备',
'影响OS',
'影响APP',
'补丁',
'基于边界',
'基于 网络',
'基于设备通用',
'基于设备端口',
'基于OS',
'基于服务端口',
'基于应用',
'基于服务',
'攻击步骤',
'推荐值',
'备注']


'''

import xlrd
import jieba
import numpy as np
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt

class net:

    filePath = ''
    alg      = ''
    data     = []
    feature  = []
    pos      = []           # position
    steps    = []           # steps
    holeType = []

    def __init__(self,filepath, alg):
        self.filePath = filepath
        self.alg = alg.lower()

    def preprocess(self):

        # 1 read the data
        filePath = self.filePath
        excel = xlrd.open_workbook(filePath)
        sheet = excel.sheets()[0]
        nrows = sheet.nrows
        for i in range(nrows):
            dictLine = {"name":sheet.row_values(i)[0],
                        "des":sheet.row_values(i)[2],
                        "way":sheet.row_values(i)[9]}
            #print(sheet.row_values(i)[4])
            self.data.append(dictLine)
            #print(sheet.row_values(i)[2])
        del(self.data[0])
        # print(self.data)

        # 2 data -> feature
        for line in self.data:
            #listFeature = [#self.getType(line['name']),
                           #self.getClass(line['des']),
                           #self.getPos(line['des']),
                           #self.getReason(line['des']),
                           #self.getStep(line['des']),
                           #self.getResult(line['des'])
                           #]
            lineFea = self.getFeature(line['des'])
            lineFea.append(line['way'])
            self.feature.append(lineFea)

        #print(self.feature)
        '''
        with open("pos.txt",'a+') as f:
            for line in self.pos:
                f.write(line+"\r\n")
        f.close()
        with open("step.txt",'a+') as f:
            for line in self.steps:
                f.write(line+"\r\n")
        f.close()
        #print(self.holeType)
        '''


    # get the type of info
    def getType(self,strings,ListDir = ''):

        lines = jieba.cut(strings)
        tmp = []
        for line in lines:
            tmp.append(line)

        #stri = ( (str(tmp[-3]) if len(tmp)>2 else "") + str(tmp[-2] + str(tmp[-1]))).strip("）,。")
        stri = (str(tmp[-2]) + str(tmp[-1])).strip("）,。")
        if not stri in self.holeType:
            self.holeType.append(stri)

        # print(", ".join(lines))
        return self.holeType.index(stri)


    # get the OS/APP/Device
    '''
        os | APP | Device
       000 | 100 |  200
    '''
    def getClass(self,strings):
        classnum = 200
        osArr = ["indow","mac","inux","unix","android","ios","ubuntu","OS"]
        appArr = ["office","play","http","web","nginx","pache","tomcat","mail","fire","ie","word","Samba","powerpoint","Player","lotus","flash","exchange_server","chrome"]
        for ii in osArr:
            if strings.find(ii) != -1:
                classnum = 0
                continue
        if(0 != classnum):
            for ii in appArr:
                if strings.find(ii) != -1:
                    classnum = 100
                    continue

        return classnum


    # get the position
    def getFeature(self,strings):

        ret = []

        mypos = ""
        mystep = ""
        lines = jieba.cut(strings)
        posFlag = 0
        stepFlag = 0
        for line in lines:
            if line == '。' or line == '，':
                posFlag = 0
                stepFlag = 0

            if posFlag == 1:
                mypos += str(line)
                with open("pos.txt",'a+') as f:
                    f.write(line+" ")
                f.close()

            if line == '存在':
                posFlag = 1

            if stepFlag == 1:
                mystep += str(line)
                with open("step.txt",'a+') as f:
                    f.write(line+" ")
                f.close()

            if line == '攻击者' or line == '者':
                stepFlag = 1

        with open("pos.txt",'a+') as f:
            f.write("\r\n")
        f.close()
        with open("step.txt",'a+') as f:
            f.write("\r\n")
        f.close()


        mystep = mystep.strip()
        print(mystep)
        if not mystep in self.steps:
            self.steps.append(mystep)

        mypos = mypos.replace('漏洞','').strip()
        if not mypos in self.pos:
            self.pos.append(mypos)

        ret.append(self.pos.index(mypos))
        ret.append(self.steps.index(mystep))
        #print(", ".join(lines))
        #print(ret)
        return ret


    # get the reason
    def getReason(self,strings):
        return 1


    # get the step
    def getStep(self,strings):
        return 1


    # get the result
    def getResult(self,strings):
        return 1


    # choice the alg , you can add your alg here
    def getTheModel(self):
        alg = self.alg
        #feature = self.feature
        print(alg)
        if 'kmeans' == alg:
            self.useKMeans()


    # use KMeans
    def useKMeans(self):
        print("begining")
        feature = self.feature
        x = np.array(feature)
        # print(x)
        y_pred = KMeans(n_clusters = 2).fit_predict(x)
        plt.figure()
        plt.scatter(x[:,0], x[:,1], c = y_pred)
        plt.show()



# filepath :the file path
filepath = 'tem.xlsx'
filepath = 'main.xls'
filepath = 'SQLL.xlsx'
alg = 'kmeans'
g = net(filepath, alg)
g.preprocess()
#g.getTheModel()
