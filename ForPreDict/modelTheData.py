# -*- coding: utf-8 -*-
"""
Created on Fri May 30 14:15:37 2014

@author: zqh
"""


import numpy as np

from sklearn.ensemble import GradientBoostingRegressor

from sklearn.decomposition import PCA
from matplotlib import pyplot as plt 
#from sklearn.lda import LDA


def my_Decomposing(X,n):

#    X = iris.data
#    y = iris.target
#    target_names = iris.target_names
    
    
    pca = PCA(n_components=n)
    X_r = pca.fit(X).transform(X)
#    lda = LDA(n_components=n)
#    X_r2 = lda.fit(X, y).transform(X)    
    return X_r


def modelTheData(data,target):

#    params = {'n_estimators': 400, 'max_depth': 4, 'min_samples_split': 2,
#          'subsample': 0.5,'min_samples_leaf': 2,
#          'learning_rate': 0.01, 'loss': 'ls'}


#beijing
#    myMachine = GradientBoostingRegressor(alpha=0.9, init=None, learn_rate=None,
#             learning_rate=0.05, loss='ls', max_depth=1, max_features=None,
#             min_samples_leaf=2, min_samples_split=2, n_estimators=300,
#             random_state=None, subsample=0.5, verbose=0)

    myMachine = GradientBoostingRegressor(alpha=0.9, init=None, learn_rate=None,
             learning_rate=0.05, loss='ls', max_depth=3, max_features=None,
             min_samples_leaf=2, min_samples_split=2, n_estimators=500,
             random_state=None, subsample=0.5, verbose=0)
#shanghai
#    myMachine = GradientBoostingRegressor(alpha=0.9, init=None, learn_rate=None,
#             learning_rate=0.05, loss='ls', max_depth=3, max_features=None,
#             min_samples_leaf=2, min_samples_split=2, n_estimators=500,
#             random_state=None, subsample=0.5, verbose=0)





#    myMachine = GradientBoostingRegressor(**params)
    myMachine.fit(data,target)

    return myMachine
    





def predictCityPm(myMachine,DataSet):
#    n=12
    Data,Target=DataSet[:,1:-1],DataSet[:,-1] 
    
#    Data_decomp = my_Decomposing(Data,n)
    
    preDara=myMachine.predict(Data)
    
    date = DataSet[:,0]
    

    plt.figure()
    plt.plot(range(len(date)),Target,label = 'true')
    plt.plot(range(len(date)),preDara,label = 'predict')
    plt.legend(loc='upper right')
    plt.title('predict and true value')
    
#    plt.savefig('xm_predict.png',dpi = 600)
    
    plt.show()
    
    plt.figure()
    plt.plot(range(len(date)),preDara-Target)
    plt.title('eroor plot')
    plt.show()
    
    

    return preDara




dataSet = np.random.permutation(BJ_DataSet) 
myData,myTarget=dataSet[:,1:-1],dataSet[:,-1]      

#n=12
#deX1 = my_Decomposing(myData,n)
#myMachine = modelTheData(deX1,myTarget)

myMachine = modelTheData(myData,myTarget)


#XM_preDara = predictCityPm(myMachine,XM_DataSet)


SH_preDara = predictCityPm(myMachine,SH_DataSet)
































