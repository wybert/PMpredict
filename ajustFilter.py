# -*- coding: utf-8 -*-
"""
Created on Tue May 06 09:47:03 2014

@author: zqh
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 04 21:53:41 2014

@author: zqh
"""

#----------------------------训练模型---------------------------------

import numpy as np
import pylab as plt
from sklearn.ensemble import GradientBoostingRegressor

def myModel(dataSet):

    dataSet = np.random.permutation(dataSet) 
    myData,myTarget=dataSet[:,1:-1],dataSet[:,-1]
    date = dataSet[:,0]



    rat = 0.7
    ratio = int(len(myData)*rat)
    myMachine =  GradientBoostingRegressor(n_estimators=100, learning_rate=1.0,
               max_depth=1, random_state=0, loss='ls')
    myMachine.fit(myData[:ratio], myTarget[:ratio])
    
    myDate = date[ratio:]

#    print myMachine.score(myData[ratio:],myTarget[ratio:])
    


    preDara=myMachine.predict(myData[ratio:])
    error=preDara-myTarget[ratio:]
#  sort and mannge
    

    
    trueValu=myTarget[ratio:]
    
    fa=len(trueValu)
    trueValu=trueValu.reshape(fa,1)
    preDara=preDara.reshape(fa,1)
    error=error.reshape(fa,1)
    myDate=myDate.reshape(fa,1)

    data=np.hstack((trueValu,preDara,error,myDate))
    inx=np.argsort(data[:,1])
    data=data[inx,:]
    return data


def get_hist_one(dataSet,jiange):      

    data= myModel(dataSet)
#    trueValu,preDara,error,myDate
    # use shiyingsuanfa 
    # dui 500 fen duan ,间隔为10      
    hist_one=[]
    
    for i in range(360/jiange):
        start=i*jiange
        end=start+jiange
#        print start,':',end
        bar=[]
        for j in range(len(data[:,1])):
            if data[:,1][j] >=start and data[:,1][j]< end:
                bar.append(data[:,2][j])
#        print sum(bar)
        if len(bar)!=0:
            hist_one.append(sum(bar)/len(bar))
        else:
            hist_one.append(0)
    return hist_one




def caclu_adjustor(dataSet,jiange):
    
    hist=np.zeros((360/jiange,1),dtype=float)   
    feq=200   
    chuxian_cishu=np.zeros((360/jiange,feq),dtype=float)
    for i in range(feq):
        hist_one=get_hist_one(dataSet,jiange)
        for j in range(len(hist_one)):
            if hist_one[j] !=0:
                chuxian_cishu[j,i] +=1
#        print hist_one
        hist_one = np.array(hist_one).reshape(hist.shape)
#        print hist_one
        hist += hist_one
    print '-----------------------------------'
#    print hist
    
    cishu = np.sum(chuxian_cishu,axis=1)
    cishu=cishu.reshape(len(cishu),1)
#    print cishu.shape
   
#    print hist.shape
    hist=hist/(cishu)
#    print hist.shape
   
    return hist

def error_adjust(dataSet,jiange):
    
    
    hist=caclu_adjustor(dataSet,jiange)
    
    
    data= myModel(dataSet)
    y=[]
    
    for i in range(360/jiange):
        start=i*jiange
        end=start+jiange
#        print start,':',end
        for j in range(len(data[:,1])):

            if data[:,1][j] >=start and data[:,1][j]< end:
#                print preDara[j]
#                print hist[i]            
                y.append(data[:,1][j]-hist[i][0])
            
#                y.append(data[:,1][j]*(e**-(hist[i][0]*0.001)))


    y=np.array(y)
#    print len(trueValu),len(y)
   
    return data,y,hist
def draw_preformance(data,y,hist,jiange):
    
    error2=y-data[:,0]
    x=np.arange(360/jiange)*jiange
    plt.plot(x,hist)
#    plt.show()
    zero_line= np.zeros((len(x),1),dtype=float)
    plt.plot(x,zero_line)
    
    plt.scatter(data[:,1],data[:,2],marker='o',alpha=0.7,label='adjust before')
    
    plt.scatter(data[:,1],error2,c='r',marker='o',alpha=0.7,label='adjusted')
    plt.xlim(xmin=0,xmax=350)
    plt.legend(loc='upper left')
    plt.title('adjust befor and after')
    plt.show()




     
##     plot error effects
#     
 
#    effects = abs(data[:,2])-abs(error2)
#    print 'effects '
#    plt.scatter(y,effects)
##    plt.xlim(xmax=250)
#    plt.show()
#    
#    plt.scatter(data[:,2],effects)
##    plt.xlim(xmax=250)
#    plt.show()
#    
    
    
    inx=np.argsort(data[:,3])
    data=data[inx,:]
    y=y[inx]
    plt.plot(data[:,3],data[:,0],label='true')
    plt.plot(data[:,3],data[:,1],label='predict1')
    plt.plot(data[:,3],y,label='predict2')
    plt.legend(loc='upper right')  
    plt.title('fuibi')
    plt.savefig('test.png',dpi=200)
    plt.show()


#--------------------------------------------------------------------------------    
    

jiange=10
data,y,hist = error_adjust(dataSet,jiange)
draw_preformance(data,y,hist,jiange)
    
    























