# -*- coding: utf-8 -*-
"""
Created on Thu Jun 05 17:13:59 2014

@author: zqh
"""

import numpy as np
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.datasets import make_hastie_10_2
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
#dataSet = np.random.permutation(BJ_DataSet) 
#
#myData,myTarget=dataSet[:,1:-1],dataSet[:,-1]
#
##selectedFetureName=SELECTED_FETURE_NAME[1:-1]
#date = dataSet[:,0]
#rat = 0.8
#ratio = int(len(myData)*rat)
#
#X_train, y_train = myData[:ratio], myTarget[:ratio]
#X_test, y_test = myData[ratio:], myTarget[ratio:]



def testTheModel(data,target):
    

    X_train, X_test, y_train, y_test = train_test_split(
        data, target, test_size=0.3, random_state=0)
     
    # Set the parameters by cross-validation
    tuned_parameters = [
                        {'n_estimators': [100,200,300], 'learning_rate': [0.2,0.1,0.05],
                         'subsample':[0.5],
                         'max_depth': [1,2,3],
#                         'max_features':[10,11],
                         'min_samples_leaf':[10,5,2],
#                        'loss':['ls','lad','huber','quantile'],
#                        'alpha':[0.1,0.3,0.5,0.7,0.9]

#                         'min_samples_split':[2,3]
                             }
                    
                         ]
    
    #############################################################################
    print "# Tuning hyper-parameters for "
    print 
    
    clf = GridSearchCV(GradientBoostingClassifier(loss='deviance'), tuned_parameters, cv=5 )
    clf.fit(X_train, y_train)
    print  "Best scores:"
    print clf.best_score_    
    
    print "Best parameters set found on development set:"
    print 
    print clf.best_estimator_
    print 
#    print "Grid scores on development set:"
#    print 
#    for params, mean_score, scores in clf.grid_scores_:
#        print("%0.3f (+/-%0.03f) for %r"
#              % (mean_score, scores.std() / 2, params))
    print 
    
   
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print 
 



dataSet = np.random.permutation(BJ_DataSet) 
myData,myTarget=dataSet[:,1:-1],dataSet[:,-1]      

#n=15
#deX1 = my_Decomposing(myData,myTarget,n)
#testTheModel(deX1,myTarget)
    
testTheModel(myData,myTarget)   
    

    
    
    
    
    
    
    
    
    
    
    


#
#
#
#clf = RandomForestClassifier(n_estimators=10)
#clf = clf.fit(X_train, y_train)
#print clf.score(X_test, y_test)




#clf = GradientBoostingClassifier(n_estimators=10, learning_rate=1.0,
#     max_depth=1,loss='deviance', random_state=0).fit(X_train, y_train)
#clf.fit(X_train, y_train)     
#print clf.score(X_test, y_test)                 

#from sklearn.cross_validation import cross_val_score
#
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.ensemble import ExtraTreesClassifier


#X, y = myData,myTarget
#
#clf = RandomForestClassifier(n_estimators=100, max_depth=3,
#     min_samples_split=3, random_state=0)
#scores = cross_val_score(clf, X, y)
#print scores.mean()                             



                    