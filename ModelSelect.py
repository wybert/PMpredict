# -*- coding: utf-8 -*-
"""
Created on Fri Apr 04 21:53:41 2014

@author: zqh
"""

#----------------------------训练模型---------------------------------

import numpy as np
import pylab as plt

dataSet = np.random.permutation(BJ_DataSet) 

myData,myTarget=dataSet[:,1:-1],dataSet[:,-1]



date = dataSet[:,0]

rat = 0.7

ratio = int(len(myData)*rat)



#plt.plot(myTarget[:ratio],'ro')
#plt.show()
#
#
#plt.plot(date,myTarget,'ro')
#plt.show()


#
##------------select machine--------------------------------

from sklearn.ensemble import GradientBoostingRegressor
#from sklearn.ensemble import GradientBoostingClassifier




myMachine =  GradientBoostingRegressor(n_estimators=100, learning_rate=1.0,
           max_depth=1, random_state=0, loss='ls')

myMachine.fit(myData[:ratio], myTarget[:ratio])


print myMachine.score(myData[ratio:],myTarget[ratio:])
preDara=myMachine.predict(myData[ratio:])



myDate = date[ratio:]

x=range(len(myTarget[ratio:]))
plt.plot(x,myTarget[ratio:],label='true')
plt.plot(x,preDara,label='predict')
plt.legend(loc='upper right')
plt.title('predict and true value')
plt.show()

#myDate = date[ratio:]


careError=[]
careMyDate=[]
error=preDara-myTarget[ratio:]
for i in range(len(error)):
    if abs(error[i])>=50:
        careError +=[error[i]]
        careMyDate += [myDate[i]]
for item in careMyDate:
    print item
#
#plt.scatter(careMyDate,careError)
##plt.text()
#plt.show()
#   

#
#plt.scatter(myTarget[ratio:],preDara) 
#  
#plt.show()

   
   
plt.scatter(myDate,error,marker='.',alpha=0.7,)

zero_line=np.zeros((len(error),1),dtype=float)
plt.plot(myDate,zero_line,c='g')

plt.plot(myDate,zero_line+50,'-.',c='r',alpha=0.7)
plt.plot(myDate,zero_line-50,'-.',c='r',alpha=0.7)


plt.xlim(xmax=max(myDate),xmin=min(myDate))
plt.show()


#plt.scatter(myDate,error)
#plt.show()


# use shiyingsuanfa 
# dui 500 fen duan ,间隔为10
















