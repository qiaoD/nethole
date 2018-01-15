'''
1 get the data : xlrd
2 preprocess the data: data -> number : jieba / numpy
3 use the alg : scikit-learn
'''

import xlrd
import jieba
import numpy as np
import sklearn

class net:
    
    filePath =''
    alg = ''
    oldData = ''
    data    = ''

    def __init__(filepath, alg):
        self.filePath = filepath
        self.alg = alg
    
    def preprocess():
        pass

    def getTheModel():
        pass

filepath = 'tem.xlsx'
alg = ''
g = net(filepath, alg)


    
