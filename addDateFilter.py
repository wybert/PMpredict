# -*- coding: utf-8 -*-
"""
Created on Tue May 13 08:44:42 2014

@author: zqh
"""

import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.ensemble import GradientBoostingRegressor
import pylab as plt
import datetime

def testTheModel(data,target):
    

    X_train, X_test, y_train, y_test = train_test_split(
        data, target, test_size=0.3, random_state=0)
     
    # Set the parameters by cross-validation
    tuned_parameters = [
                        {'n_estimators': [100,200], 'learning_rate': [1.0, 0.5,0.1],
                         'max_depth': [1,2,3]}
                    
#                        {'kernel': ['linear'], 'C': [1,2,3,4,5,6,7,8,9]}
                         ]
    
    #############################################################################
    print "# Tuning hyper-parameters for "
    print 
    
    clf = GridSearchCV(GradientBoostingRegressor(loss='ls'), tuned_parameters, cv=5 )
    clf.fit(X_train, y_train)
    
    print "Best parameters set found on development set:"
    print 
    print clf.best_estimator_
    print 
    print "Grid scores on development set:"
    print 
    for params, mean_score, scores in clf.grid_scores_:
        print("%0.3f (+/-%0.03f) for %r"
              % (mean_score, scores.std() / 2, params))
    print 
    
    print("Detailed classification report:")
    print 
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print 
 
def modelTheData(dataSet,draw=False):

    dataSet = np.random.permutation(dataSet) 
    myData,myTarget=dataSet[:,1:-1],dataSet[:,-1]
    
    
    date = dataSet[:,0]
    rat = 0.7
    ratio = int(len(myData)*rat)
    
    
    
    
    myMachine =  GradientBoostingRegressor(n_estimators=100, learning_rate=1.0,
               max_depth=1, random_state=0, loss='ls')
    
    myMachine.fit(myData[:ratio], myTarget[:ratio])
    
    
    
    preDara=myMachine.predict(myData[ratio:])
    
    
    myDate = date[ratio:]
    
    #  draw the wrong sssssampe

    error=preDara-myTarget[ratio:]
    
    if draw:
        print myMachine.score(myData[ratio:],myTarget[ratio:])
        plt.scatter(myDate,error)
        plt.show()
    
    careError=[]
    careMyDate=[]
    for i in range(len(error)):
        if abs(error[i])>=50:
            careError +=[error[i]]
            careMyDate += [myDate[i]]
#    print careMyDate
    
#    plt.scatter(careMyDate,careError)
#    plt.text()
#    plt.show()
    return careMyDate


       
   



def testModelBy_time(dataSet,therta):
    dateFilter=set()
    careDate={}
    for i in range(100):
        careMyDate = modelTheData(dataSet)
        for item in careMyDate:
#            print str(item)
            if str(item) not in careDate.keys():
                careDate[str(item)]=0
            careDate[str(item)] +=1
            
    sorted_careTime= sorted(careDate.iteritems(), key=lambda x:x[1], reverse = True)
    for (k,v) in sorted_careTime:
        if v>therta:
            aruList = [int(i) for i in k.split('-')]
            dateFilter.add(datetime.date(*aruList))
#            print k,':',v
            
    
    
    return dateFilter,sorted_careTime

    

therta=10

dateFilter,sorted_careTime=testModelBy_time(dataSet,therta)  

sorted_careTime=np.array(sorted_careTime,dtype=object)

x=range(len(sorted_careTime))
print len(x)
plt.scatter(x,sorted_careTime[:,1])

plt.show()


day_loss=day_loss.union(dateFilter)


print 'set theta=',therta,'we get:'
print 'almost',len(dateFilter),'days:'
for item in dateFilter:
    print item
print 'catched!'



#dataSet = np.random.permutation(dataSet) 
#myData,myTarget=dataSet[:,1:-1],dataSet[:,-1]      
#
#testTheModel(myData,myTarget)
    